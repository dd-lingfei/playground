"""
Best Buy Shipping-Only Product Scraper
=======================================
Crawls Best Buy using the official Best Buy Developer API and collects products
that are available for online shipping but NOT available for in-store pickup
at the specified ZIP code.

Requirements:
    Free API key: https://developer.bestbuy.com
    pip install requests

Usage:
    python bestbuy_scraper.py --api-key YOUR_KEY
    python bestbuy_scraper.py --api-key YOUR_KEY --zip-code 98006 --radius 30
    python bestbuy_scraper.py --api-key YOUR_KEY --max-pages 50 --output-dir ./results
    python bestbuy_scraper.py --api-key YOUR_KEY --checkpoint ./progress.json  # resume interrupted run
"""

import argparse
import csv
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

import requests

logger = logging.getLogger(__name__)


class BestBuyScraper:
    """
    Scrapes Best Buy for products available via shipping but NOT for pickup
    at the given ZIP code, using the official Best Buy Developer API.

    API reference: https://developer.bestbuy.com/documentation
    """

    BASE_URL = "https://api.bestbuy.com/v1"

    # Fields to retrieve per product
    PRODUCT_FIELDS = ",".join([
        "sku",
        "name",
        "regularPrice",
        "salePrice",
        "onSale",
        "url",
        "addToCartUrl",
        "manufacturer",
        "modelNumber",
        "categoryPath",
        "onlineAvailability",
        "onlineAvailabilityText",
        "inStoreAvailability",
        "inStoreAvailabilityText",
        "shippingCost",
        "freeShipping",
        "freeShippingEligible",
        "thumbnailImage",
        "shortDescription",
        "longDescription",
    ])

    def __init__(
        self,
        api_key: str,
        zip_code: str = "98006",
        radius_miles: int = 25,
        output_dir: str = ".",
        request_delay: float = 0.5,
        batch_size: int = 100,
        checkpoint_file: Optional[str] = None,
    ):
        """
        Args:
            api_key:          Best Buy Developer API key (developer.bestbuy.com)
            zip_code:         ZIP code used to check in-store pickup availability
            radius_miles:     Miles around zip_code to search for nearby stores
            output_dir:       Directory for CSV output
            request_delay:    Seconds to wait between API calls (respect rate limits)
            batch_size:       Products per page request (API max is 100)
            checkpoint_file:  JSON file to save/restore progress for long runs
        """
        self.api_key = api_key
        self.zip_code = zip_code
        self.radius_miles = radius_miles
        self.output_dir = Path(output_dir)
        self.request_delay = request_delay
        self.batch_size = min(batch_size, 100)
        self.checkpoint_file = Path(checkpoint_file) if checkpoint_file else None

        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

        self.nearby_store_ids: List[str] = []
        self.stats: Dict[str, int] = {
            "total_fetched": 0,
            "pickup_available": 0,
            "shipping_only": 0,
            "api_calls": 0,
        }

    # ------------------------------------------------------------------
    # Internal HTTP helpers
    # ------------------------------------------------------------------

    def _get(self, path: str, params: Optional[dict] = None) -> Optional[dict]:
        """
        Authenticated GET to the Best Buy API with exponential-backoff retries.
        `path` is appended directly to BASE_URL (include leading slash + filter).
        """
        if params is None:
            params = {}
        params["apiKey"] = self.api_key
        params.setdefault("format", "json")

        url = f"{self.BASE_URL}{path}"

        for attempt in range(4):
            try:
                resp = self.session.get(url, params=params, timeout=30)
                self.stats["api_calls"] += 1

                if resp.status_code == 200:
                    return resp.json()

                if resp.status_code == 429:
                    wait = 30 * (attempt + 1)
                    logger.warning("Rate limited — waiting %ds before retry %d…", wait, attempt + 1)
                    time.sleep(wait)
                    continue

                if resp.status_code == 401:
                    raise ValueError(
                        "Invalid or expired API key. "
                        "Get a free key at https://developer.bestbuy.com"
                    )

                logger.warning("HTTP %d on attempt %d: %s", resp.status_code, attempt + 1, resp.text[:300])

            except requests.ConnectionError as exc:
                logger.warning("Connection error on attempt %d: %s", attempt + 1, exc)
            except requests.Timeout:
                logger.warning("Request timed out on attempt %d", attempt + 1)

            if attempt < 3:
                time.sleep(2 ** attempt)

        logger.error("Giving up on %s after 4 attempts", url)
        return None

    # ------------------------------------------------------------------
    # Store discovery
    # ------------------------------------------------------------------

    def get_nearby_stores(self) -> List[Dict]:
        """
        Find Best Buy stores within `radius_miles` of `zip_code`.
        Populates self.nearby_store_ids and returns the raw store list.
        """
        logger.info(
            "Finding Best Buy stores within %d miles of %s…",
            self.radius_miles, self.zip_code,
        )

        data = self._get(
            f"/stores(area({self.zip_code},{self.radius_miles}))",
            {
                "show": "storeId,name,city,state,postalCode,distance,storeType",
                "pageSize": 100,
            },
        )

        if not data or "stores" not in data:
            logger.warning(
                "No stores returned near %s. "
                "Products cannot be filtered by pickup — all online products treated as shipping-only.",
                self.zip_code,
            )
            return []

        stores = data["stores"]
        self.nearby_store_ids = [str(s["storeId"]) for s in stores]

        logger.info("Found %d store(s):", len(stores))
        for s in stores:
            dist = s.get("distance")
            dist_str = f"{float(dist):.1f} mi" if dist is not None else "? mi"
            logger.info(
                "  [%s] %s — %s, %s  (%s)",
                s["storeId"], s.get("name", "Best Buy"),
                s.get("city", ""), s.get("state", ""), dist_str,
            )

        return stores

    # ------------------------------------------------------------------
    # Product pagination
    # ------------------------------------------------------------------

    def _fetch_product_page(self, page: int) -> Optional[dict]:
        """Fetch one page of products with onlineAvailability=true."""
        return self._get(
            "/products(onlineAvailability=true)",
            {
                "show": self.PRODUCT_FIELDS,
                "sort": "sku.asc",
                "page": page,
                "pageSize": self.batch_size,
            },
        )

    # ------------------------------------------------------------------
    # Pickup availability check
    # ------------------------------------------------------------------

    def _pickup_skus_for_batch(self, skus: List[str]) -> Set[str]:
        """
        Given a batch of SKU strings, return the subset that IS available
        for in-store pickup at any of the nearby stores.

        Products NOT in the returned set are shipping-only at this ZIP code.
        """
        if not skus or not self.nearby_store_ids:
            return set()

        sku_filter = ",".join(skus)
        store_filter = ",".join(self.nearby_store_ids)

        data = self._get(
            f"/products(sku in ({sku_filter}))/stores(storeId in ({store_filter}))",
            {
                "show": "sku,storeId,pickup",
                "pageSize": 1000,
            },
        )

        pickup_skus: Set[str] = set()
        if data and "stores" in data:
            for entry in data["stores"]:
                if entry.get("pickup") is True:
                    pickup_skus.add(str(entry["sku"]))

        return pickup_skus

    # ------------------------------------------------------------------
    # Checkpoint helpers
    # ------------------------------------------------------------------

    def _load_checkpoint(self) -> dict:
        if self.checkpoint_file and self.checkpoint_file.exists():
            try:
                with open(self.checkpoint_file) as f:
                    data = json.load(f)
                logger.info(
                    "Loaded checkpoint: resuming from page %d (%d products so far)",
                    data.get("last_page", 0), len(data.get("products", [])),
                )
                return data
            except Exception as exc:
                logger.warning("Could not load checkpoint (%s) — starting fresh.", exc)
        return {"last_page": 0, "products": []}

    def _save_checkpoint(self, page: int, products: List[dict]) -> None:
        if self.checkpoint_file:
            try:
                with open(self.checkpoint_file, "w") as f:
                    json.dump({"last_page": page, "products": products}, f)
            except Exception as exc:
                logger.warning("Could not save checkpoint: %s", exc)

    # ------------------------------------------------------------------
    # Main crawl
    # ------------------------------------------------------------------

    def run(self, max_pages: Optional[int] = None) -> List[Dict]:
        """
        Full crawl: paginate through all online products, filter by pickup
        availability at zip_code, and return shipping-only products.

        Args:
            max_pages: Limit crawl to N pages (handy for testing).

        Returns:
            List of product dicts with no in-store pickup near zip_code.
        """
        logger.info("=" * 60)
        logger.info("Best Buy Shipping-Only Scraper")
        logger.info("  ZIP code : %s", self.zip_code)
        logger.info("  Radius   : %d miles", self.radius_miles)
        logger.info("=" * 60)

        # 1. Discover nearby stores
        self.get_nearby_stores()
        if not self.nearby_store_ids:
            logger.warning(
                "Proceeding without nearby-store filter — "
                "all online products will be reported as shipping-only."
            )

        # 2. Resume or start fresh
        checkpoint = self._load_checkpoint()
        start_page = checkpoint["last_page"] + 1
        shipping_only: List[Dict] = checkpoint.get("products", [])

        # 3. Paginate
        page = start_page
        total_pages: Optional[int] = None

        while True:
            if max_pages and page > max_pages:
                logger.info("Reached --max-pages limit (%d).", max_pages)
                break

            if total_pages:
                logger.info(
                    "Page %d/%d | Shipping-only so far: %d",
                    page, total_pages, len(shipping_only),
                )
            else:
                logger.info("Page %d | Fetching first batch…", page)

            data = self._fetch_product_page(page)
            if not data:
                logger.error("Failed to fetch page %d — stopping.", page)
                break

            page_products = data.get("products", [])
            if not page_products:
                logger.info("No products on page %d — done.", page)
                break

            # Set total_pages from first response metadata
            if total_pages is None:
                total_results = data.get("total", 0)
                total_pages = max(1, (total_results + self.batch_size - 1) // self.batch_size)
                logger.info(
                    "Total online products: %d across ~%d pages",
                    total_results, total_pages,
                )

            self.stats["total_fetched"] += len(page_products)

            # 4. Check which SKUs in this batch have nearby pickup
            skus = [str(p["sku"]) for p in page_products]
            pickup_skus = self._pickup_skus_for_batch(skus)
            self.stats["pickup_available"] += len(pickup_skus)

            # 5. Keep shipping-only products
            batch_shipping_only = 0
            for product in page_products:
                if str(product["sku"]) not in pickup_skus:
                    # Flatten categoryPath list → readable string
                    if isinstance(product.get("categoryPath"), list):
                        product["categoryPath"] = " > ".join(
                            c.get("name", "") for c in product["categoryPath"]
                        )
                    product["zip_code_checked"] = self.zip_code
                    product["scraped_at"] = datetime.now().isoformat()
                    shipping_only.append(product)
                    self.stats["shipping_only"] += 1
                    batch_shipping_only += 1

            logger.info(
                "  Batch: %d products | Pickup-available: %d | Shipping-only: %d",
                len(page_products), len(pickup_skus), batch_shipping_only,
            )

            # Save checkpoint every 10 pages
            if page % 10 == 0:
                self._save_checkpoint(page, shipping_only)

            if page >= total_pages:
                break

            page += 1
            time.sleep(self.request_delay)

        # Summary
        logger.info("=" * 60)
        logger.info("Crawl complete.")
        logger.info("  Products checked  : %d", self.stats["total_fetched"])
        logger.info("  Pickup available  : %d", self.stats["pickup_available"])
        logger.info("  Shipping-only     : %d", self.stats["shipping_only"])
        logger.info("  Total API calls   : %d", self.stats["api_calls"])
        logger.info("=" * 60)

        return shipping_only

    # ------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------

    def save_to_csv(self, products: List[Dict], filename: Optional[str] = None) -> str:
        """Save the products list to a CSV file. Returns the file path."""
        if not filename:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bestbuy_shipping_only_{self.zip_code}_{ts}.csv"

        self.output_dir.mkdir(parents=True, exist_ok=True)
        filepath = self.output_dir / filename

        if not products:
            logger.warning("No products to write — empty CSV will not be created.")
            return str(filepath)

        # Union of all keys preserving insertion order of first product
        fieldnames = list(products[0].keys())
        extra_keys = [k for p in products for k in p if k not in fieldnames]
        fieldnames.extend(dict.fromkeys(extra_keys))  # dedup while preserving order

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(products)

        logger.info("Saved %d products → %s", len(products), filepath)
        return str(filepath)


# ----------------------------------------------------------------------
# CLI entry point
# ----------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Crawl Best Buy and collect products available for shipping "
            "but NOT for in-store pickup at a given ZIP code."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bestbuy_scraper.py --api-key YOUR_KEY
  python bestbuy_scraper.py --api-key YOUR_KEY --zip-code 98006 --radius 30
  python bestbuy_scraper.py --api-key YOUR_KEY --max-pages 10 --output-dir ./results
  python bestbuy_scraper.py --api-key YOUR_KEY --checkpoint ./run.json   # resume

Get your FREE API key at: https://developer.bestbuy.com
        """,
    )
    parser.add_argument(
        "--api-key", required=True,
        help="Best Buy Developer API key (https://developer.bestbuy.com)",
    )
    parser.add_argument(
        "--zip-code", default="98006",
        help="ZIP code to check for in-store pickup availability (default: 98006)",
    )
    parser.add_argument(
        "--radius", default=25, type=int,
        help="Radius in miles for nearby-store lookup (default: 25)",
    )
    parser.add_argument(
        "--max-pages", type=int, default=None,
        help="Stop after N pages — useful for testing (default: crawl all pages)",
    )
    parser.add_argument(
        "--output-dir", default=".",
        help="Directory to write the output CSV (default: current directory)",
    )
    parser.add_argument(
        "--delay", default=0.5, type=float,
        help="Seconds between API requests (default: 0.5)",
    )
    parser.add_argument(
        "--batch-size", default=100, type=int,
        help="Products per API request, max 100 (default: 100)",
    )
    parser.add_argument(
        "--checkpoint",
        help="Path to a JSON checkpoint file; saves progress so long runs can be resumed",
    )
    parser.add_argument(
        "--log-level", default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity (default: INFO)",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    scraper = BestBuyScraper(
        api_key=args.api_key,
        zip_code=args.zip_code,
        radius_miles=args.radius,
        output_dir=args.output_dir,
        request_delay=args.delay,
        batch_size=args.batch_size,
        checkpoint_file=args.checkpoint,
    )

    products = scraper.run(max_pages=args.max_pages)
    output_path = scraper.save_to_csv(products)

    print(f"\nDone! Found {len(products):,} shipping-only products.")
    print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    main()
