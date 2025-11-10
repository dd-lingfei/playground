"""
Uber Eats Product Scraper
Scrapes product information from Uber Eats store pages and exports to CSV.
"""

import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import argparse


class UberEatsScraper:
    """Scraper for Uber Eats product information."""
    
    def __init__(self, headless=False):
        """Initialize the scraper with Chrome WebDriver."""
        self.driver = None
        self.headless = headless
        self.products_data = []
        
    def setup_driver(self):
        """Set up Chrome WebDriver with appropriate options."""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        # Additional options for stability
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Initialize WebDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        
    def close_driver(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            
    def handle_popups(self):
        """Handle potential popups and modals."""
        try:
            # Wait a bit for any popups to appear
            time.sleep(2)
            
            # Try to close cookie consent or other modals
            close_buttons = [
                "//button[contains(text(), 'Close')]",
                "//button[contains(@aria-label, 'Close')]",
                "//button[contains(@aria-label, 'close')]",
                "//div[contains(@class, 'close')]",
            ]
            
            for xpath in close_buttons:
                try:
                    close_btn = self.driver.find_element(By.XPATH, xpath)
                    close_btn.click()
                    time.sleep(1)
                    print("Closed popup/modal")
                except:
                    continue
                    
        except Exception as e:
            print(f"No popups to handle or error handling them: {e}")
            
    def wait_for_products(self, timeout=15):
        """Wait for product elements to load on the page."""
        try:
            # Wait for product containers to be present
            wait = WebDriverWait(self.driver, timeout)
            
            # Multiple possible selectors for product containers
            selectors = [
                (By.CSS_SELECTOR, "div[data-testid*='store-item']"),
                (By.CSS_SELECTOR, "div[class*='item-card']"),
                (By.CSS_SELECTOR, "div[class*='product']"),
                (By.XPATH, "//div[contains(@class, 'item') or contains(@class, 'product')]"),
            ]
            
            for by, selector in selectors:
                try:
                    wait.until(EC.presence_of_element_located((by, selector)))
                    return True
                except TimeoutException:
                    continue
                    
            print("⚠️  Warning: Could not confirm products loaded with known selectors")
            return False
            
        except Exception as e:
            print(f"Error waiting for products: {e}")
            return False
            
    def scroll_page(self):
        """Scroll the page to load lazy-loaded content."""
        try:
            # Get initial height
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Scroll down slowly to trigger lazy loading of images
            scroll_pause_time = 2
            scroll_increment = 500  # pixels
            
            # First, scroll through the page in increments
            current_position = 0
            for i in range(10):  # Scroll in small increments
                current_position += scroll_increment
                self.driver.execute_script(f"window.scrollTo(0, {current_position});")
                time.sleep(0.5)  # Short pause to load images
                
            # Then scroll to bottom
            for i in range(3):  # Scroll 3 times to load more content
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(scroll_pause_time)
                
                # Calculate new height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                
            # Scroll back to top slowly to ensure all images are loaded
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            print("✓ Finished scrolling\n")
            
        except Exception as e:
            print(f"⚠️  Error scrolling page: {e}")
            
    def extract_products(self):
        """Extract product information from the page."""
        try:
            # Find all product containers - try multiple selectors
            product_containers = []
            
            selectors = [
                "div[data-testid*='store-item']",
                "div[class*='item-card']",
                "li[data-testid*='store-item']",
                "div[role='listitem']",
            ]
            
            for selector in selectors:
                try:
                    containers = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if containers:
                        product_containers = containers
                        break
                except:
                    continue
                    
            if not product_containers:
                # Fallback: try to find any div that looks like a product card
                print("⚠️  Using fallback selector...")
                product_containers = self.driver.find_elements(By.XPATH, 
                    "//div[.//img and (.//span[contains(text(), '$')] or .//div[contains(text(), '$')])]")
            
            # Extract data from each product, scrolling into view to load lazy images
            total_products = len(product_containers)
            print(f"✓ Found {total_products} products")
            print()
            
            for idx, product in enumerate(product_containers):
                try:
                    # Scroll product into view to trigger lazy loading
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", product)
                    time.sleep(0.1)  # Short pause to let image load
                    
                    product_data = self.extract_product_data(product, idx)
                    if product_data:
                        self.products_data.append(product_data)
                        
                        # Show progress every 10 products or at the end
                        if (idx + 1) % 10 == 0 or (idx + 1) == total_products:
                            percentage = ((idx + 1) / total_products) * 100
                            print(f"Progress: {idx + 1}/{total_products} ({percentage:.1f}%) - Last: {product_data['Name'][:50]}...")
                except Exception as e:
                    print(f"Error extracting product {idx}: {e}")
                    continue
                    
            print(f"\n✓ Successfully extracted {len(self.products_data)} products")
            
        except Exception as e:
            print(f"Error in extract_products: {e}")
            raise
            
    def extract_product_data(self, product_element, idx):
        """Extract individual product data."""
        product_data = {
            'Name': 'N/A',
            'Price': 'N/A',
            'Image_URL': 'N/A',
            'Stock_Status': 'Available'
        }
        
        debug_mode = False  # Set to True to see debug info for first 3 products
        
        try:
            # Get the full HTML for debugging if needed
            if debug_mode and idx < 3:
                print(f"\n--- Product {idx} ---")
                print(product_element.get_attribute('outerHTML')[:800])
            
            # Extract Name - try multiple approaches
            name_found = False
            
            # Try different name selectors
            name_selectors = [
                ".//h3",
                ".//h4",
                ".//h2",
                ".//div[contains(@class, 'title')]",
                ".//span[contains(@class, 'title')]",
                ".//div[contains(@class, 'name')]",
                ".//a//div[not(contains(text(), '$'))]",
            ]
            
            discount_patterns = [r'\d+%\s*off', r'sale', r'deal']
            
            for selector in name_selectors:
                try:
                    elements = product_element.find_elements(By.XPATH, selector)
                    for elem in elements:
                        text = elem.text.strip()
                        if text and '$' not in text and len(text) > 3:
                            # Skip discount/sale labels
                            is_discount = any(re.search(pattern, text, re.IGNORECASE) for pattern in discount_patterns)
                            if not is_discount:
                                product_data['Name'] = text
                                name_found = True
                                break
                    if name_found:
                        break
                except:
                    continue
            
            # If still no name, try getting all text and parsing
            if not name_found:
                try:
                    all_text = product_element.text.strip()
                    lines = [line.strip() for line in all_text.split('\n') if line.strip()]
                    # First non-empty line that's not a price or discount label is usually the name
                    for line in lines:
                        if line and '$' not in line and len(line) > 3:
                            # Skip discount/sale labels
                            is_discount = any(re.search(pattern, line, re.IGNORECASE) for pattern in discount_patterns)
                            if not is_discount:
                                product_data['Name'] = line
                                break
                except:
                    pass
                    
            # Extract Price - try multiple approaches
            price_selectors = [
                ".//span[contains(text(), '$')]",
                ".//div[contains(text(), '$')]",
                ".//*[contains(text(), '$')]",
                ".//*[contains(@class, 'price')]",
            ]
            
            for selector in price_selectors:
                try:
                    elements = product_element.find_elements(By.XPATH, selector)
                    for elem in elements:
                        text = elem.text.strip()
                        if '$' in text:
                            # Clean up the price - take just the first price if multiple
                            prices = re.findall(r'\$[\d,.]+', text)
                            if prices:
                                product_data['Price'] = prices[0]
                                break
                    if product_data['Price'] != 'N/A':
                        break
                except:
                    continue
                    
            # Extract Image URL - try multiple approaches
            try:
                img_elements = product_element.find_elements(By.TAG_NAME, "img")
                
                if debug_mode and idx < 3:
                    print(f"  Found {len(img_elements)} img elements")
                
                for img_elem in img_elements:
                    # Try all possible image attributes
                    img_url = (img_elem.get_attribute("src") or 
                              img_elem.get_attribute("data-src") or 
                              img_elem.get_attribute("data-lazy-src") or
                              img_elem.get_attribute("data-original") or
                              img_elem.get_attribute("srcset") or
                              img_elem.get_attribute("data-srcset"))
                    
                    if debug_mode and idx < 3:
                        print(f"  Img src: {img_elem.get_attribute('src')}")
                        print(f"  Img srcset: {img_elem.get_attribute('srcset')}")
                    
                    if img_url:
                        # Skip placeholder or data URIs
                        if img_url.startswith('data:'):
                            continue
                            
                        # Clean up the URL
                        if 'http' in img_url:
                            # Handle srcset format (multiple URLs with sizes)
                            if ',' in img_url or ' ' in img_url:
                                product_data['Image_URL'] = img_url.split(',')[0].split(' ')[0].strip()
                            else:
                                product_data['Image_URL'] = img_url
                            break
                        elif img_url.startswith('//'):
                            product_data['Image_URL'] = 'https:' + img_url
                            break
                        elif img_url.startswith('/'):
                            product_data['Image_URL'] = 'https://www.ubereats.com' + img_url
                            break
            except Exception as e:
                if debug_mode and idx < 3:
                    print(f"  Error extracting image: {e}")
                pass
            
            # Fallback: Try to find images in nested elements
            if product_data['Image_URL'] == 'N/A':
                try:
                    # Look for picture elements or other image containers
                    picture_elements = product_element.find_elements(By.TAG_NAME, "picture")
                    for picture in picture_elements:
                        sources = picture.find_elements(By.TAG_NAME, "source")
                        for source in sources:
                            img_url = source.get_attribute("srcset") or source.get_attribute("src")
                            if img_url and 'http' in img_url:
                                product_data['Image_URL'] = img_url.split(',')[0].split(' ')[0].strip()
                                break
                        if product_data['Image_URL'] != 'N/A':
                            break
                except:
                    pass
                
            # Check Stock Status
            try:
                # Look for out of stock indicators
                out_of_stock_texts = ['out of stock', 'unavailable', 'sold out', 'currently unavailable', 'not available']
                element_text = product_element.text.lower()
                
                for out_text in out_of_stock_texts:
                    if out_text in element_text:
                        product_data['Stock_Status'] = 'Out of Stock'
                        break
                        
                # Check for disabled state or overlay
                class_attr = product_element.get_attribute("class") or ""
                if 'disabled' in class_attr.lower() or 'unavailable' in class_attr.lower():
                    product_data['Stock_Status'] = 'Out of Stock'
                    
            except:
                pass
                
            # Only return if we got at least a name
            if product_data['Name'] != 'N/A':
                return product_data
            else:
                # Debug: print what we couldn't extract
                if idx < 3:  # Only print first 3 for debugging
                    print(f"  Debug: Could not extract name from product {idx}")
                    try:
                        print(f"  Text content: {product_element.text[:100]}")
                    except:
                        pass
                return None
                
        except Exception as e:
            print(f"Error extracting data from product element {idx}: {e}")
            return None
            
    def save_to_csv(self, filename):
        """Save extracted data to CSV file."""
        try:
            if not self.products_data:
                print("⚠️  No product data to save!")
                return False
                
            df = pd.DataFrame(self.products_data)
            df.to_csv(filename, index=False, encoding='utf-8')
            
            # Calculate some stats
            products_with_images = sum(1 for p in self.products_data if p['Image_URL'] != 'N/A')
            products_in_stock = sum(1 for p in self.products_data if p['Stock_Status'] == 'Available')
            
            print(f"✓ Data saved successfully to {filename}")
            print(f"  • Total products: {len(self.products_data)}")
            print(f"  • With images: {products_with_images}")
            print(f"  • In stock: {products_in_stock}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving to CSV: {e}")
            return False
            
    def scrape(self, url, output_file):
        """Main scraping method."""
        try:
            print("=" * 60)
            print(f"🚀 Starting Uber Eats Scraper")
            print("=" * 60)
            print(f"📍 URL: {url}")
            print(f"📄 Output: {output_file}")
            print()
            
            # Setup driver
            print("⚙️  Setting up Chrome WebDriver...")
            self.setup_driver()
            print("✓ WebDriver ready\n")
            
            # Navigate to URL
            print("🌐 Loading page...")
            self.driver.get(url)
            print("✓ Page loaded\n")
            
            # Handle popups
            print("🔍 Checking for popups...")
            self.handle_popups()
            
            # Wait for products to load
            print("⏳ Waiting for products to load...")
            self.wait_for_products()
            print("✓ Products detected\n")
            
            # Scroll to load lazy content
            print("📜 Scrolling to load all content...")
            self.scroll_page()
            
            # Extract products
            print("📦 Extracting product data...")
            self.extract_products()
            
            # Save to CSV
            print(f"\n💾 Saving to {output_file}...")
            self.save_to_csv(output_file)
            
            print("\n" + "=" * 60)
            print("✅ Scraping completed successfully!")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ Error during scraping: {e}")
            raise
            
        finally:
            # Always close the driver
            print("\n🔒 Closing browser...")
            self.close_driver()


def main():
    """Main function to run the scraper."""
    parser = argparse.ArgumentParser(description='Scrape Uber Eats product information')
    parser.add_argument('--url', type=str, 
                       default='https://www.ubereats.com/store/safeway-6911-coal-creek-pkwy-ses/xNI-v9wZW7ijmryiKtxh4Q?diningMode=DELIVERY&storeSearchQuery=halloween',
                       help='Uber Eats store URL to scrape')
    parser.add_argument('--output', type=str, 
                       default='ubereats_products.csv',
                       help='Output CSV filename')
    parser.add_argument('--headless', action='store_true',
                       help='Run browser in headless mode')
    
    args = parser.parse_args()
    
    # Create scraper instance
    scraper = UberEatsScraper(headless=args.headless)
    
    # Run scraper
    scraper.scrape(args.url, args.output)


if __name__ == "__main__":
    main()


