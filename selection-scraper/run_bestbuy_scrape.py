"""
Best Buy Shipping-Only Scraper  (undetected-chromedriver, no API key)
=====================================================================
Collects Best Buy products that are NOT available for in-store pickup
at ZIP 98006 (Bellevue / Seattle area).

Run:  venv/bin/python run_bestbuy_scrape.py
"""

import csv
import json
import logging
import re
import time
from datetime import datetime
from typing import Dict, List, Optional

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchWindowException

# ── config ────────────────────────────────────────────────────────────────────
ZIP_CODE     = "98006"
TARGET_COUNT = 100
OUTPUT_FILE  = f"bestbuy_shipping_only_{ZIP_CODE}.csv"
CHROME_VER   = 145       # match installed Chrome major version

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# Categories to crawl  (name, Best Buy URL)
CATEGORIES = [
    ("Laptops",      "https://www.bestbuy.com/site/computers-pcs/laptops/abcat0502000.c"),
    ("Cameras",      "https://www.bestbuy.com/site/cameras-camcorders/digital-cameras/abcat0401001.c"),
    ("Video Games",  "https://www.bestbuy.com/site/video-games/all-video-games/abcat0700000.c"),
    ("TVs",          "https://www.bestbuy.com/site/tvs/all-flat-screen-tvs/abcat0101001.c"),
    ("Networking",   "https://www.bestbuy.com/site/computers-pcs/computer-networking/abcat0503000.c"),
    ("PC Accessories","https://www.bestbuy.com/site/computers-pcs/computer-accessories/abcat0516000.c"),
    ("Wearables",    "https://www.bestbuy.com/site/wearable-technology/all-wearable-tech/pcmcat333800050001.c"),
    ("Car Tech",     "https://www.bestbuy.com/site/car-electronics/all-car-electronics/abcat0200000.c"),
    ("Music",        "https://www.bestbuy.com/site/musical-instruments/all-instruments/abcat0900000.c"),
    ("Cell Phones",  "https://www.bestbuy.com/site/cell-phones/all-cell-phones/abcat0800000.c"),
    ("Tablets",      "https://www.bestbuy.com/site/computers-pcs/tablets-e-readers/abcat0500000.c"),
    ("Headphones",   "https://www.bestbuy.com/site/audio/headphones/abcat0204001.c"),
    ("Health",       "https://www.bestbuy.com/site/health-fitness/all-health-fitness/pcmcat350500050007.c"),
    ("Office",       "https://www.bestbuy.com/site/office-school-supplies/all-office-supplies/pcmcat420400050005.c"),
    ("Smart Home",   "https://www.bestbuy.com/site/smart-home/all-smart-home/pcmcat500300050001.c"),
]

# ── driver ────────────────────────────────────────────────────────────────────

def make_driver() -> uc.Chrome:
    opts = uc.ChromeOptions()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1400,900")
    driver = uc.Chrome(options=opts, version_main=CHROME_VER)
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)  # async price polling needs up to ~6 s
    return driver

# ── helpers ───────────────────────────────────────────────────────────────────

def dismiss_popups(driver):
    for sel in [
        "#onetrust-accept-btn-handler",
        "button[aria-label='Close']",
        ".c-modal-close",
        "button.c-close-icon",
        "[data-testid='close-button']",
    ]:
        try:
            driver.find_element(By.CSS_SELECTOR, sel).click()
            time.sleep(0.3)
        except Exception:
            pass


def _is_error_page(driver) -> bool:
    """Return True if the browser is showing a Chrome error / rate-limit page."""
    try:
        return (
            "chrome-error://" in driver.current_url
            or "be reached" in driver.title.lower()
            or "err_" in driver.title.lower()
        )
    except Exception:
        return False


def inject_zip(driver, zip_code: str):
    """Inject ZIP into localStorage keys Best Buy may read."""
    try:
        driver.execute_script(f"""
            localStorage.setItem('user_zip_code', '{zip_code}');
            localStorage.setItem('zip_code', '{zip_code}');
            localStorage.setItem('postalCode', '{zip_code}');
            localStorage.setItem('GeoLocation_postalCode', '{zip_code}');
        """)
    except Exception:
        pass  # window may have navigated; safe to ignore


def set_zip_code(driver, zip_code: str):
    """Try to set ZIP via the header store-locator UI; fallback to localStorage."""
    log.info("Setting ZIP code to %s…", zip_code)
    inject_zip(driver, zip_code)

    # Try UI approach (best effort — don't crash if it fails)
    try:
        btn = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,
            "button.store-locator-component-header-store, "
            "[data-testid='storeLocatorButton'], "
            "button[aria-label*='tore']"
        )))
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(1.0)
        inp = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,
            "input[placeholder*='ZIP'], input[placeholder*='zip'], "
            "input[aria-label*='ZIP'], input[placeholder*='postal']"
        )))
        inp.clear()
        inp.send_keys(zip_code)
        inp.send_keys(Keys.RETURN)
        time.sleep(2.0)
        log.info("ZIP set via header UI ✓")
    except Exception:
        log.info("Header UI not found — using localStorage injection only.")


# ── listing-page product URL extraction ──────────────────────────────────────

def _extract_product_urls_from_source(html: str, source_category: str = "") -> List[Dict]:
    """
    Pull product URLs + names from embedded page JSON / static HTML.
    Best Buy embeds product skuIds and basic data in inline JavaScript.
    """
    results: List[Dict] = []
    seen: set = set()

    # Pattern 1: /product/{slug}/{model}/sku/{skuId}  (new URL format)
    new_urls = re.findall(
        r'https?://www\.bestbuy\.com/product/([^/\"\'\\>]+)/([^/\"\'\\>]+)/sku/(\d+)',
        html,
    )
    for slug, model, sku in new_urls:
        url = f"https://www.bestbuy.com/product/{slug}/{model}/sku/{sku}"
        if sku not in seen:
            seen.add(sku)
            name = slug.replace("-", " ").title()
            results.append({"sku": sku, "name": name, "url": url, "price": "",
                            "source_category": source_category})

    # Pattern 2: old-style .p?skuId= URLs already present in the source
    for m in re.finditer(r'href="(https?://www\.bestbuy\.com/site/[^/]+/(\d+)\.p[^"]*)"', html):
        href, sku = m.group(1), m.group(2)
        if "placeholder" not in href and sku not in seen:
            seen.add(sku)
            results.append({"sku": sku, "name": "", "url": href, "price": "",
                            "source_category": source_category})

    return results


def collect_product_urls(driver, category_url: str, max_pages: int = 3,
                         source_category: str = "") -> List[Dict]:
    """Browse a Best Buy category page and return unique product info dicts."""
    all_items: List[Dict] = []
    seen_skus: set = set()

    driver.get(category_url)
    time.sleep(4)
    dismiss_popups(driver)

    for pg in range(1, max_pages + 1):
        log.info("    Listing page %d — extracting products…", pg)
        time.sleep(3)

        html = driver.page_source

        # --- DOM approach: Best Buy list items ---
        # Narrow the search to the main product grid to avoid sidebar/recommendation cards
        dom_items = []
        grid_ctx = driver
        for grid_sel in ["#main-results", "ol.sku-list", ".sr-list-content",
                         ".category-list", "[id='main-results']", "main"]:
            try:
                el = driver.find_element(By.CSS_SELECTOR, grid_sel)
                grid_ctx = el
                break
            except Exception:
                pass

        for card_sel in ["li.sku-item", ".shop-sku-list-item", "[data-sku-id]",
                         ".sr-list__item", "article.product-item"]:
            cards = grid_ctx.find_elements(By.CSS_SELECTOR, card_sel)
            if cards:
                log.info("    DOM cards found with '%s': %d", card_sel, len(cards))
                for card in cards:
                    try:
                        sku = (card.get_attribute("data-sku-id") or
                               card.get_attribute("data-sku") or "")
                        name, href = "", ""
                        for ns in ["h4.sku-header a", ".sku-title a", ".product-title a",
                                   "h4 a", "h3 a", ".nc-product-title a",
                                   "a[href*='/product/']", "a[href*='.p?']"]:
                            try:
                                el = card.find_element(By.CSS_SELECTOR, ns)
                                name = name or el.text.strip()
                                href = href or (el.get_attribute("href") or "")
                            except Exception:
                                pass
                        price = ""
                        for ps in [".priceView-customer-price span[aria-hidden='false']",
                                   ".priceView-customer-price span", ".sr-item__price",
                                   ".pb-purchase-price"]:
                            try:
                                price = card.find_element(By.CSS_SELECTOR, ps).text.strip()
                                if price:
                                    break
                            except Exception:
                                pass
                        # Only keep cards with a resolvable Best Buy product URL
                        valid_url = bool(href and ('/product/' in href or ('/site/' in href and 'placeholder' not in href)))
                        if valid_url and sku not in seen_skus:
                            seen_skus.add(sku)
                            dom_items.append({"sku": sku, "name": name, "url": href,
                                              "price": price, "source_category": source_category})
                    except (StaleElementReferenceException, Exception):
                        pass
                break  # found a working selector

        if dom_items:
            all_items.extend(dom_items)
            log.info("    DOM extraction: %d products", len(dom_items))
        else:
            # Fallback: parse embedded JSON/URLs from source
            source_items = _extract_product_urls_from_source(html, source_category)
            new_items = [i for i in source_items if i["sku"] not in seen_skus]
            for i in new_items:
                seen_skus.add(i["sku"])
            all_items.extend(new_items)
            log.info("    Source extraction: %d products (%d new)", len(source_items), len(new_items))

        # Try next page
        advanced = False
        for nxt_sel in ["a.sku-list-page-next", "[aria-label='Next Page']",
                        ".paging-next a", "button[aria-label='Next page']",
                        "a[rel='next']"]:
            try:
                el = driver.find_element(By.CSS_SELECTOR, nxt_sel)
                href = el.get_attribute("href")
                if href:
                    driver.get(href)
                    advanced = True
                    break
            except Exception:
                pass
        if not advanced:
            break

    return all_items


# ── per-product pickup check ──────────────────────────────────────────────────

def _pickup_status_from_source(html: str) -> Optional[bool]:
    """
    Parse Best Buy's embedded Apollo/GraphQL JSON for pickup availability.
    Returns True  → pickup available (SKIP)
            False → pickup NOT available / shipping-only (KEEP)
            None  → could not determine
    """
    # Find ispuAvailability blocks
    blocks = re.findall(r'"ispuAvailability"\s*:\s*\[(\{[^\]]+\})\]', html)
    if not blocks:
        return None

    any_available = False
    for block in blocks:
        eligible = re.search(r'"pickupEligible"\s*:\s*(true|false)', block)
        in_stock  = re.search(r'"instoreInventoryAvailable"\s*:\s*(true|false)', block)
        if eligible and eligible.group(1) == "false":
            continue  # this store/sku not eligible
        if in_stock and in_stock.group(1) == "true":
            any_available = True
            break

    return any_available  # True = has pickup somewhere; False = no pickup found


def _extract_enrichment_from_source(html: str) -> Dict:
    """
    Pull price, model, and category from the page's embedded JSON / structured data.
    Best Buy inlines Apollo cache and JSON-LD on every product page.
    """
    result: Dict = {"price": "", "model": "", "category": ""}

    # ── Price ──────────────────────────────────────────────────────────────────
    # 1. JSON-LD <script type="application/ld+json">
    for m in re.finditer(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html, re.DOTALL | re.IGNORECASE,
    ):
        try:
            ld = json.loads(m.group(1))
            if isinstance(ld, list):
                ld = ld[0]
            offers = ld.get("offers", {})
            if isinstance(offers, list):
                offers = offers[0]
            p = offers.get("price", "")
            if p and float(str(p).replace(",", "")) > 0:
                result["price"] = f"${p}"
                break
        except Exception:
            pass

    # 2. Inline JS / Apollo cache patterns
    if not result["price"]:
        for pat in [
            r'"customerPrice"\s*:\s*([\d.]+)',
            r'"currentPrice"\s*:\s*([\d.]+)',
            r'"salePrice"\s*:\s*([\d.]+)',
            r'"regularPrice"\s*:\s*([\d.]+)',
            r'"displayPrice"\s*:\s*"?\$?([\d,]+\.?\d*)"?',
        ]:
            m = re.search(pat, html)
            if m:
                try:
                    val = float(m.group(1).replace(",", ""))
                    if val > 0:
                        result["price"] = f"${val:,.2f}"
                        break
                except ValueError:
                    pass

    # ── Model ──────────────────────────────────────────────────────────────────
    for pat in [
        r'"modelNumber"\s*:\s*"([^"]{2,30})"',
        r'"model"\s*:\s*"([^"]{2,30})"',
        r'Model[:\s]+</[^>]+>\s*<[^>]+>([^<]{2,30})<',
    ]:
        m = re.search(pat, html)
        if m:
            result["model"] = m.group(1).strip()
            break

    # ── Category ───────────────────────────────────────────────────────────────
    for pat in [
        r'"categoryPath"\s*:\s*"([^"]+)"',
        r'"breadcrumb"\s*:\s*\[.*?"name"\s*:\s*"([^"]+)"[^\]]*\]',
    ]:
        m = re.search(pat, html)
        if m:
            # Use the last segment of a path like "TVs > All Flat-Screen TVs"
            parts = re.split(r'[>|/]', m.group(1))
            result["category"] = parts[-1].strip()
            break

    return result


# Phrases that definitively signal whether pickup is available
_PICKUP_YES = ["free store pickup", "pick up today", "ready for pickup",
               "pickup available", "pickup in store", "ready today",
               "same day pickup", "store pickup available"]
_PICKUP_NO  = ["not available for pickup", "pickup not available",
               "not available at", "not available in stores",
               "in-store pickup not available", "pickup unavailable"]


def check_and_enrich_product(driver, item: Dict, zip_code: str) -> Optional[Dict]:
    """
    Visit the product page; return enriched dict if shipping-only, else None.
    """
    url = item.get("url", "")
    if not url:
        return None
    try:
        driver.get(url)
        time.sleep(3.5)
        inject_zip(driver, zip_code)
        dismiss_popups(driver)

        # Redirect: update URL if page redirected
        current_url = driver.current_url
        title = driver.title

        # Chrome error pages have URL "chrome-error://..." or title starting with "ERR_"
        if "chrome-error://" in current_url or title.upper().startswith("ERR_"):
            log.debug("Chrome error page on %s", url[:80])
            return None

        if not title or "Page Not Found" in title or "404" in title \
                or "be reached" in title.lower() or "placeholder" in url:
            log.debug("404/error on %s", url[:80])
            return None

        html = driver.page_source

        # ── Pull enrichment from page source (JSON-LD + inline JS) ──
        enriched = _extract_enrichment_from_source(html)

        # ── Enrich: name ──
        data = dict(item)
        if not data.get("name") or len(data["name"]) < 4:
            try:
                data["name"] = driver.find_element(
                    By.CSS_SELECTOR,
                    "h1.heading-5, h1.product-title, .shop-product-title h1, h1"
                ).text.strip()
            except Exception:
                data["name"] = re.sub(r" - Best Buy$", "", title).strip()

        # Reject error pages that slipped past the title check
        if "be reached" in data["name"].lower() or "err_" in data["name"].lower():
            log.debug("Error page (via h1) on %s", url[:80])
            return None

        # ── Enrich: price — poll DOM until price element appears (handles async render) ──
        # NOTE: .standard-layout__middle-block_price can also appear in featured-product
        # carousels, so we use the first price value > $5 from a safe list of selectors.
        data["price"] = ""
        try:
            # execute_async_script: poll every 300 ms for up to ~9 s (30 attempts)
            price_js = driver.execute_async_script("""
                var done = arguments[arguments.length - 1];
                var attempts = 0;
                function dollarVal(txt) {
                    var m = txt && txt.match(/\\$([\\d,]+\\.?\\d*)/);
                    return m ? parseFloat(m[1].replace(/,/g, '')) : 0;
                }
                function firstGoodDollar(txt) {
                    var m = txt && txt.match(/\\$[\\d,]+\\.?\\d*/);
                    return (m && dollarVal(m[0]) > 5) ? m[0] : null;
                }
                function tryFind() {
                    var sels = [
                        '.price-container',
                        '[class*="priceView-customer-price"]',
                        '[class*="priceView-hero-price"]',
                        '.pb-purchase-price',
                        '[data-testid="customer-price"]',
                        '.standard-layout__middle-block_price',
                    ];
                    for (var s of sels) {
                        var els = document.querySelectorAll(s);
                        for (var i = 0; i < els.length; i++) {
                            var q = firstGoodDollar(els[i].textContent);
                            if (q) { done(q); return; }
                        }
                    }
                    // sr-only "Your price for this item is $X"
                    var srEls = document.querySelectorAll('.sr-only,[class*="visuallyHidden"]');
                    for (var i = 0; i < srEls.length; i++) {
                        var t = srEls[i].textContent;
                        if (t && t.includes('$') && t.toLowerCase().includes('price')) {
                            var r = firstGoodDollar(t); if (r) { done(r); return; }
                        }
                    }
                    attempts++;
                    if (attempts < 30) { setTimeout(tryFind, 300); } else { done(null); }
                }
                tryFind();
            """)
            if price_js and "$" in str(price_js):
                data["price"] = str(price_js).strip()
        except Exception:
            pass

        # ── Source-based price (fetch fresh page_source after React hydration) ──
        if not data["price"]:
            try:
                fresh_html = driver.page_source
                fresh_enriched = _extract_enrichment_from_source(fresh_html)
                data["price"] = fresh_enriched["price"]
            except Exception:
                pass

        # ── Final fallback: first meaningful price from rendered page text ──
        if not data["price"]:
            try:
                body_text = driver.execute_script("return document.body.innerText") or ""
                for m in re.finditer(r'\$(\d{2,4}(?:\.\d{2})?)', body_text):
                    val = float(m.group(1))
                    if val >= 9.99:
                        data["price"] = f"${val:.2f}"
                        break
            except Exception:
                pass

        # ── Original source fallback (in case none of the above worked) ──
        if not data["price"]:
            data["price"] = enriched["price"]

        # ── Enrich: model via JavaScript ──
        data["model"] = enriched["model"]
        if not data["model"]:
            try:
                model_js = driver.execute_script("""
                    var sels = ['[class*="modelNumber"]', '[data-testid*="model"]',
                                '.product-data-value', '[class*="ModelNumber"]'];
                    for (var s of sels) {
                        var el = document.querySelector(s);
                        if (el && el.textContent.trim().length >= 2) return el.textContent.trim();
                    }
                    // Scan for "Model: XXXX" in page text
                    var m = document.body.innerText.match(/Model[:\s]+([A-Z0-9][A-Z0-9\-]{2,29})/i);
                    return m ? m[1].trim() : null;
                """)
                if model_js:
                    data["model"] = str(model_js).strip()
            except Exception:
                pass

        # ── Enrich: category (breadcrumb JS, then source fallback, then collection label) ──
        data["category"] = enriched["category"]
        if not data["category"]:
            try:
                cat_js = driver.execute_script("""
                    var containers = [
                        'nav[aria-label*="readcrumb"]',
                        '[class*="readcrumb"]',
                        '[data-testid*="readcrumb"]'
                    ];
                    for (var sel of containers) {
                        var items = document.querySelectorAll(sel + ' li, ' + sel + ' a');
                        if (items.length > 1) {
                            return items[items.length - 2].textContent.trim();
                        }
                    }
                    return null;
                """)
                if cat_js:
                    data["category"] = str(cat_js).strip()
            except Exception:
                pass
        # Last resort: use the category from our scraping context
        if not data["category"]:
            data["category"] = item.get("source_category", "")

        # ── Determine pickup availability ──
        html_lower = html.lower()

        # 1. Check text signals
        pickup_yes = any(p in html_lower for p in _PICKUP_YES)
        pickup_no  = any(p in html_lower for p in _PICKUP_NO)

        # 2. Check embedded JSON  (most reliable)
        json_pickup = _pickup_status_from_source(html)

        # Decision: skip (pickup available) if any strong YES signal
        if json_pickup is True:
            log.debug("SKIP json-pickup=True: %s", data.get("name","")[:55])
            return None
        if pickup_yes and not pickup_no:
            log.debug("SKIP text-pickup=yes: %s", data.get("name","")[:55])
            return None

        # Keep this product (no clear pickup signal or explicit no-pickup)
        data["pickup_available"] = "No"
        data["zip_code_checked"] = zip_code
        data["product_url"]      = current_url
        data["scraped_at"]       = datetime.now().isoformat()

        log.info("  KEEP: %-55s  %s", data.get("name","?")[:55], data.get("price",""))
        return data

    except Exception as exc:
        log.warning("Error on %s: %s", url[:80], exc)
        return None


# ── CSV ────────────────────────────────────────────────────────────────────────

def save_csv(products: List[Dict], path: str):
    if not products:
        log.warning("No products to save.")
        return
    cols = ["sku", "name", "price", "model", "category",
            "pickup_available", "zip_code_checked", "scraped_at", "product_url"]
    extra = [k for p in products for k in p if k not in cols]
    cols.extend(dict.fromkeys(extra))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(products)
    log.info("Saved %d products → %s", len(products), path)


# ── main ───────────────────────────────────────────────────────────────────────

def main():
    log.info("=" * 60)
    log.info("Best Buy Shipping-Only Scraper (undetected-chromedriver)")
    log.info("ZIP: %s  |  Target: %d", ZIP_CODE, TARGET_COUNT)
    log.info("=" * 60)

    def _fresh_driver():
        d = make_driver()
        d.get("https://www.bestbuy.com")
        time.sleep(4)
        dismiss_popups(d)
        set_zip_code(d, ZIP_CODE)
        time.sleep(1)
        return d

    driver = _fresh_driver()
    shipping_only: List[Dict] = []
    skipped_items: List[Dict] = []   # items deferred due to rate limiting
    consecutive_fails = 0

    def _process_items(items_list: List[Dict], label: str) -> bool:
        """
        Process a list of product items. Returns True if rate-limited mid-way
        (caller should restart browser). Appends skipped remainder to skipped_items.
        """
        nonlocal driver, consecutive_fails
        for idx, item in enumerate(items_list):
            if len(shipping_only) >= TARGET_COUNT:
                return False

            # Save checkpoint every 25 products
            if len(shipping_only) > 0 and len(shipping_only) % 25 == 0:
                _checkpoint()

            try:
                result = check_and_enrich_product(driver, item, ZIP_CODE)
            except NoSuchWindowException:
                log.warning("Browser window lost during product check — restarting…")
                try: driver.quit()
                except Exception: pass
                time.sleep(15)
                driver = _fresh_driver()
                consecutive_fails = 0
                skipped_items.extend(items_list[idx:])
                return True
            except Exception as e:
                log.warning("Unexpected error on item: %s", e)
                result = None

            if result:
                name = result.get("name", "")
                if "be reached" in name.lower() or "err_" in name.lower() or not name:
                    consecutive_fails += 1
                else:
                    consecutive_fails = 0
                    shipping_only.append(result)
                    log.info("  [%d/%d] shipping-only found", len(shipping_only), TARGET_COUNT)
            else:
                if _is_error_page(driver):
                    consecutive_fails += 1
                    log.debug("Error page detected — consecutive_fails=%d", consecutive_fails)
                else:
                    consecutive_fails = 0

            if consecutive_fails >= 3:
                remaining = items_list[idx + 1:]
                if remaining:
                    log.warning(
                        "Rate limiting on '%s' — deferring %d remaining items for retry later",
                        label, len(remaining),
                    )
                    skipped_items.extend(remaining)
                log.warning("Restarting browser session (90s pause)…")
                try:
                    driver.quit()
                except Exception:
                    pass
                time.sleep(90)
                driver = _fresh_driver()
                consecutive_fails = 0
                log.info("Browser session restarted ✓")
                return True  # signal: was rate-limited
            else:
                time.sleep(3.0)
        return False

    checkpoint_at = 0  # track when we last saved a checkpoint

    def _checkpoint():
        nonlocal checkpoint_at
        if len(shipping_only) > checkpoint_at:
            save_csv(shipping_only, OUTPUT_FILE)
            checkpoint_at = len(shipping_only)

    def _safe_collect(cat_url, cat_name):
        """Collect product URLs, restarting driver on window crash."""
        nonlocal driver
        try:
            return collect_product_urls(driver, cat_url, max_pages=4,
                                        source_category=cat_name)
        except NoSuchWindowException:
            log.warning("Browser window lost during collection — restarting…")
            try: driver.quit()
            except Exception: pass
            time.sleep(15)
            driver = _fresh_driver()
            try:
                return collect_product_urls(driver, cat_url, max_pages=4,
                                            source_category=cat_name)
            except Exception:
                return []
        except Exception as e:
            log.warning("Collection error for %s: %s", cat_name, e)
            return []

    try:
        for cat_name, cat_url in CATEGORIES:
            if len(shipping_only) >= TARGET_COUNT:
                break

            log.info("\n── Category: %s ──", cat_name)
            items = _safe_collect(cat_url, cat_name)
            log.info("  Total product URLs collected: %d", len(items))
            _process_items(items, cat_name)
            _checkpoint()  # save after each category

        # ── Retry deferred (rate-limited) items ──────────────────────────────
        if skipped_items and len(shipping_only) < TARGET_COUNT:
            log.info("\n── Retrying %d deferred items from rate-limited sessions ──",
                     len(skipped_items))
            time.sleep(30)  # give Best Buy's rate limiter a head start
            retry_pass = list(skipped_items)
            skipped_items.clear()
            _process_items(retry_pass, "retry")

            # Second and third retries for persistent rate-limiting
            for retry_num in (2, 3):
                if not skipped_items or len(shipping_only) >= TARGET_COUNT:
                    break
                log.info("\n── Retry pass %d: %d items still pending ──",
                         retry_num, len(skipped_items))
                time.sleep(90)
                retry_batch = list(skipped_items)
                skipped_items.clear()
                _process_items(retry_batch, f"retry-{retry_num}")
                _checkpoint()

    finally:
        try:
            driver.quit()
        except Exception:
            pass

    log.info("\n" + "=" * 60)
    log.info("Done. %d shipping-only products found.", len(shipping_only))
    log.info("=" * 60)

    save_csv(shipping_only, OUTPUT_FILE)
    print(f"\nDone! {len(shipping_only)} products saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
