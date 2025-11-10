# TNT Supermarket Scraper - Usage Guide

## Overview

The TNT Supermarket scraper is a robust web scraping tool built using Selenium that extracts product information from TNT Supermarket's website (https://www.tntsupermarket.us/eng/). It follows the same architecture as the existing Uber Eats scraper and provides comprehensive handling of common web scraping challenges.

## Features

✓ **Popup Handling**: Automatically detects and closes modal dialogs and popups
✓ **Lazy Loading Support**: Scrolls through pages to trigger lazy-loaded images
✓ **Multiple Selector Fallbacks**: Robust extraction across different product layouts
✓ **Price Extraction**: Intelligent regex-based price parsing
✓ **Stock Status Detection**: Identifies out-of-stock products
✓ **Progress Tracking**: Real-time console output showing scraping progress
✓ **Headless Mode**: Can run without visible browser window
✓ **CSV Export**: Outputs data in standardized format

## Output Format

The scraper extracts the following fields for each product:

- **Name**: Product name/title
- **Price**: Product price (format: $X.XX)
- **Image_URL**: Full URL to product image
- **Stock_Status**: "Available" or "Out of Stock"

## Usage

### Command Line

```bash
# Basic usage with default settings
python workflow_steps/tnt_supermarket_scraper.py

# Specify custom URL and output file
python workflow_steps/tnt_supermarket_scraper.py \
  --url "https://www.tntsupermarket.us/eng/" \
  --output "my_products.csv"

# Run in headless mode (no browser window)
python workflow_steps/tnt_supermarket_scraper.py \
  --url "https://www.tntsupermarket.us/eng/" \
  --output "products.csv" \
  --headless
```

### Python API

```python
from workflow_steps.tnt_supermarket_scraper import TNTSupermarketScraper

# Create scraper instance
scraper = TNTSupermarketScraper(headless=True)

# Scrape a URL
scraper.scrape(
    url="https://www.tntsupermarket.us/eng/",
    output_file="tnt_products.csv"
)

# Access extracted data
for product in scraper.products_data:
    print(f"{product['Name']}: {product['Price']}")
```

## Test Script

A test script is provided to verify the scraper functionality:

```bash
python test_tnt_scraper.py
```

This will:
1. Scrape the TNT Supermarket homepage
2. Extract product information
3. Verify data quality
4. Display sample products
5. Save output to `tnt_test_output.csv`

## Performance

Based on testing with the TNT Supermarket homepage:

- **Pages Scanned**: 1,065 product containers detected
- **Products Extracted**: ~290 valid products
- **Extraction Rate**: ~27% (due to duplicate entries and empty containers)
- **Data Quality**:
  - Names: 100% coverage
  - Prices: 98% coverage
  - Images: 50% coverage
  - Stock Status: 100% coverage

## Robustness Features

### Anti-Detection
- Custom user agent
- Disabled automation flags
- Natural scrolling behavior

### Error Handling
- Multiple selector fallbacks for each data point
- Graceful handling of missing elements
- Debug mode for troubleshooting

### Content Loading
- Incremental scrolling (500px steps)
- Element-level scroll-into-view for lazy images
- Multiple scroll passes to load all content

## Troubleshooting

### No Products Extracted

If the scraper finds products but can't extract them:
1. Enable debug mode by setting `debug_mode = True` in `extract_product_data()`
2. Check the console output for HTML structure
3. Update selectors in the `name_selectors`, `price_selectors` arrays

### Popup Blocking Content

If popups prevent scraping:
1. Add new popup selectors to the `close_buttons` array in `handle_popups()`
2. Increase wait time after popup handling

### Images Not Loading

If image URLs are "N/A":
1. Increase scroll pause time in `scroll_page()`
2. Check if images use different attribute names (add to image extraction logic)
3. Verify the website isn't blocking automated access

## Architecture

The scraper follows a modular design:

```
TNTSupermarketScraper
├── __init__()          # Initialize scraper
├── setup_driver()      # Configure Chrome WebDriver
├── close_driver()      # Clean up resources
├── handle_popups()     # Close modal dialogs
├── wait_for_products() # Wait for page load
├── scroll_page()       # Load lazy content
├── extract_products()  # Find all products
├── extract_product_data() # Extract individual product
├── save_to_csv()       # Export to CSV
└── scrape()           # Main orchestration
```

## Requirements

All dependencies are in `requirements.txt`:
- `selenium>=4.15.0`
- `pandas>=2.0.0`
- `webdriver-manager>=4.0.0`

## Comparison with Uber Eats Scraper

Both scrapers share the same architecture and features:

| Feature | Uber Eats | TNT Supermarket |
|---------|-----------|-----------------|
| Popup handling | ✓ | ✓ |
| Lazy loading | ✓ | ✓ |
| Multiple selectors | ✓ | ✓ |
| Progress tracking | ✓ | ✓ |
| Headless mode | ✓ | ✓ |
| CSV export | ✓ | ✓ |
| Stock status | ✓ | ✓ |

The main differences are in the specific CSS/XPath selectors used to match each website's HTML structure.

