#!/usr/bin/env python3
"""
End-to-End Product Matching Pipeline
Performs scraping, search, and LLM-based comparison in one shot.
"""

import argparse
import sys
import pandas as pd
from datetime import datetime
from workflow_steps.uber_eats_scraper import UberEatsScraper
from workflow_steps.search_against_qdrant import search_against_qdrant
from workflow_steps.compare_products import compare_products_with_llm
from clients import OpenAIClient
from config import CollectionConfig
from utils import print_metrics, get_app_logger, verify_prod_connection


def print_section_header(title, logger):
    """Print a formatted section header"""
    logger.info("\n" + "=" * 100)
    logger.info(f"  {title}")
    logger.info("=" * 100)


def main():
    """Main pipeline function"""
    parser = argparse.ArgumentParser(
        description='End-to-End Product Matching Pipeline: Scrape → Search → Compare'
    )
    parser.add_argument('--url', type=str,
                       default='https://www.ubereats.com/store/safeway-6911-coal-creek-pkwy-ses/xNI-v9wZW7ijmryiKtxh4Q?diningMode=DELIVERY&storeSearchQuery=halloween',
                       help='Uber Eats store URL to scrape')
    parser.add_argument('--store-id', type=int, default=1741819,
                       help='Qdrant store ID to search (default: 1741819)')
    parser.add_argument('--num-items', type=int, default=3,
                       help='Number of items to process (default: 3)')
    parser.add_argument('--headless', action='store_true',
                       help='Run browser in headless mode')
    parser.add_argument('--metrics', action='store_true',
                       help='Print performance metrics at the end')
    parser.add_argument('--skip-scraping', action='store_true',
                       help='Skip scraping and use existing scraped data')
    
    args = parser.parse_args()
    
    # Verify production connection
    verify_prod_connection()
    
    # Initialize logger and clients
    logger = get_app_logger()
    openai_client = OpenAIClient()
    store_id = args.store_id
    collection_name = CollectionConfig.get_collection_name(store_id)
    
    print_section_header("🚀 END-TO-END PRODUCT MATCHING PIPELINE", logger)
    logger.info(f"\n  Configuration:")
    logger.info(f"    • Uber Eats URL: {args.url[:80]}...")
    logger.info(f"    • Store ID: {store_id}")
    logger.info(f"    • Collection: {collection_name}")
    logger.info(f"    • Items to process: {args.num_items}")
    logger.info(f"    • Headless mode: {args.headless}")
    
    # ========================================================================
    # STEP 1: SCRAPING
    # ========================================================================
    scraping_output_file = 'tnt_products_final.csv'
    if not args.skip_scraping:
        print_section_header("STEP 1: SCRAPING UBER EATS", logger)
        
        scraper = UberEatsScraper(headless=args.headless)
        
        try:
            scraper.scrape(args.url, scraping_output_file)
        except Exception as e:
            logger.error(f"\n❌ Scraping failed: {e}")
            return 1
    else:
        print_section_header("STEP 1: USING EXISTING SCRAPED DATA", logger)
        logger.info(f"  Loading products from {scraping_output_file}...")
    
    # Load scraped products
    try:
        df = pd.read_csv(scraping_output_file)
        logger.info(f"\n  ✓ Loaded {len(df)} products from {scraping_output_file}")
    except Exception as e:
        logger.error(f"\n  ❌ Failed to load CSV: {e}")
        return 1
    
    # Get first N items
    items_to_process = df.head(args.num_items)
    if len(items_to_process) == 0:
        logger.error("\n  ❌ No products found in CSV")
        return 1
    
    logger.info(f"\n  📋 Processing first {len(items_to_process)} items:")
    for idx, row in items_to_process.iterrows():
        logger.info(f"     {idx+1}. {row['Name']}")
    
    # ========================================================================
    # STEP 2: SEARCHING
    # ========================================================================
    print_section_header("STEP 2: SEARCHING IN QDRANT", logger)
    
    search_terms = items_to_process['Name'].tolist()
    logger.info(f"\n  Searching for {len(search_terms)} products in collection '{collection_name}'...")
    
    try:
        search_results_list = search_against_qdrant(
            search_terms=search_terms,
            store_id=store_id,
            collection_name=collection_name,
            logger=logger
        )
        logger.info(f"  ✓ Search completed successfully")
    except Exception as e:
        logger.error(f"\n  ❌ Search failed: {e}")
        return 1
    
    # ========================================================================
    # STEP 3: COMPARISON
    # ========================================================================
    print_section_header("STEP 3: LLM-BASED PRODUCT COMPARISON", logger)
    
    try:
        csv_results, overall_stats = compare_products_with_llm(
            items_to_process=items_to_process,
            search_results_list=search_results_list,
            store_id=store_id,
            openai_client=openai_client,
            logger=logger
        )
    except Exception as e:
        logger.error(f"\n  ❌ Comparison failed: {e}")
        return 1
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print_section_header("📊 PIPELINE SUMMARY", logger)
    
    logger.info(f"\n  Scraping:")
    logger.info(f"    • Total products scraped: {len(df)}")
    logger.info(f"    • Products processed: {len(items_to_process)}")
    
    logger.info(f"\n  Searching:")
    logger.info(f"    • Search queries: {len(search_terms)}")
    logger.info(f"    • Average results per query: {sum(len(r.points) for r in search_results_list) / len(search_results_list):.1f}")
    
    logger.info(f"\n  Comparison:")
    logger.info(f"    • Total comparisons: {overall_stats['total_comparisons']}")
    logger.info(f"    • Matches found: {overall_stats['total_matches']}")
    logger.info(f"    • High confidence matches: {overall_stats['high_confidence_matches']}")
    logger.info(f"    • No matches: {overall_stats['no_matches']}")
    
    match_rate = (overall_stats['total_matches'] / overall_stats['total_comparisons'] * 100) if overall_stats['total_comparisons'] > 0 else 0
    logger.info(f"    • Match rate: {match_rate:.1f}%")
    
    # ========================================================================
    # STEP 4: EXPORT RESULTS TO CSV
    # ========================================================================
    if csv_results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"comparison_results_{store_id}_{timestamp}.csv"
        
        results_df = pd.DataFrame(csv_results)
        results_df.to_csv(csv_filename, index=False)
        
        logger.info(f"\n  Export:")
        logger.info(f"    • CSV file: {csv_filename}")
        logger.info(f"    • Total rows: {len(csv_results)}")
        logger.info(f"    • Items found in DD: {sum(row['item_found_in_dd'] for row in csv_results)}")
    
    logger.info("\n" + "=" * 100)
    logger.info("  ✅ PIPELINE COMPLETED SUCCESSFULLY")
    logger.info("=" * 100 + "\n")
    
    # Print metrics if requested
    if args.metrics:
        print_metrics()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

