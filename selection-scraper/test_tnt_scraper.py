"""
Test script for TNT Supermarket Scraper
Demonstrates scraper functionality with the TNT Supermarket website.
"""

import sys
from workflow_steps.tnt_supermarket_scraper import TNTSupermarketScraper


def test_tnt_scraper():
    """Test the TNT Supermarket scraper with the main page."""
    
    print("\n" + "=" * 70)
    print("TNT SUPERMARKET SCRAPER TEST")
    print("=" * 70)
    print("\nThis test will scrape products from TNT Supermarket")
    print("and verify that all required fields are extracted.\n")
    
    # Test URL
    test_url = "https://www.tntsupermarket.us/eng/"
    output_file = "tnt_test_output.csv"
    
    # Create scraper instance (headless mode for faster testing)
    scraper = TNTSupermarketScraper(headless=True)
    
    try:
        # Run scraper
        scraper.scrape(test_url, output_file)
        
        # Verify results
        print("\n" + "=" * 70)
        print("VERIFICATION")
        print("=" * 70)
        
        if not scraper.products_data:
            print("❌ FAILED: No products were extracted")
            return False
            
        print(f"✓ Total products extracted: {len(scraper.products_data)}")
        
        # Check data quality
        products_with_names = sum(1 for p in scraper.products_data if p['Name'] != 'N/A')
        products_with_prices = sum(1 for p in scraper.products_data if p['Price'] != 'N/A')
        products_with_images = sum(1 for p in scraper.products_data if p['Image_URL'] != 'N/A')
        
        print(f"✓ Products with valid names: {products_with_names}")
        print(f"✓ Products with valid prices: {products_with_prices}")
        print(f"✓ Products with valid images: {products_with_images}")
        
        # Display sample products
        print("\n" + "-" * 70)
        print("SAMPLE PRODUCTS (First 5)")
        print("-" * 70)
        
        for i, product in enumerate(scraper.products_data[:5]):
            print(f"\nProduct {i+1}:")
            print(f"  Name: {product['Name'][:60]}...")
            print(f"  Price: {product['Price']}")
            print(f"  Image: {product['Image_URL'][:70]}...")
            print(f"  Stock: {product['Stock_Status']}")
        
        # Success criteria
        success_threshold = 50  # At least 50 products should be extracted
        
        if len(scraper.products_data) >= success_threshold:
            print("\n" + "=" * 70)
            print("✅ TEST PASSED")
            print("=" * 70)
            print(f"\nThe scraper successfully extracted {len(scraper.products_data)} products")
            print(f"Output saved to: {output_file}")
            return True
        else:
            print("\n" + "=" * 70)
            print("⚠️  TEST WARNING")
            print("=" * 70)
            print(f"\nOnly {len(scraper.products_data)} products extracted")
            print(f"Expected at least {success_threshold}")
            return False
            
    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ TEST FAILED")
        print("=" * 70)
        print(f"\nError: {e}")
        return False


if __name__ == "__main__":
    success = test_tnt_scraper()
    sys.exit(0 if success else 1)

