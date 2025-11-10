# End-to-End Product Matching Pipeline

Comprehensive pipeline that performs web scraping, vector search, and LLM-based product comparison in a single execution.

## Overview

The `end_to_end_pipeline.py` script automates the complete product matching workflow:

1. **🕷️ Scraping**: Extracts product information from Uber Eats store pages
2. **🔍 Searching**: Performs vector similarity search against Qdrant collection
3. **🤖 Comparing**: Uses LLM to intelligently compare products and determine matches

## Quick Start

### Basic Usage (Default Settings)
```bash
python end_to_end_pipeline.py
```

This will:
- Scrape the default Uber Eats store
- Process the first 3 items
- Search in the default Qdrant collection (store 1741819)
- Compare each item with top 3 catalog matches
- Display formatted results

### With Custom URL
```bash
python end_to_end_pipeline.py \
  --url "https://www.ubereats.com/store/safeway-..."
```

### Process More Items
```bash
python end_to_end_pipeline.py --num-items 10
```

### Skip Scraping (Use Existing Data)
```bash
python end_to_end_pipeline.py --skip-scraping
```

### Headless Mode (No Browser Window)
```bash
python end_to_end_pipeline.py --headless
```

### With Performance Metrics
```bash
python end_to_end_pipeline.py --metrics
```

## Command-Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--url` | string | Safeway store URL | Uber Eats store URL to scrape |
| `--store-id` | int | 1741819 | Qdrant collection store ID |
| `--num-items` | int | 3 | Number of items to process |
| `--headless` | flag | False | Run browser in headless mode |
| `--metrics` | flag | False | Print performance metrics |
| `--skip-scraping` | flag | False | Use existing CSV instead of scraping |

## Example Output

```
================================================================================
  🚀 END-TO-END PRODUCT MATCHING PIPELINE
================================================================================

  Configuration:
    • Uber Eats URL: https://www.ubereats.com/store/safeway-6911-coal-creek...
    • Store ID: 1741819
    • Collection: selection_1741819_2025-11-01
    • Items to process: 3
    • Headless mode: False

================================================================================
  STEP 1: SCRAPING UBER EATS
================================================================================

⚙️  Setting up Chrome WebDriver...
✓ WebDriver ready

🌐 Loading page...
✓ Page loaded

📦 Extracting product data...
✓ Successfully extracted 127 products

  ✓ Loaded 127 products from ubereats_products.csv

  📋 Processing first 3 items:
     1. Gatorade Zero Sugar Thirst Quencher Grape Sports Drink Bottles
     2. Coca-Cola Classic Soda (12 fl oz x 12 ct)
     3. Lay's Classic Potato Chips (10 oz)

================================================================================
  STEP 2: SEARCHING IN QDRANT
================================================================================

  Searching for 3 products in collection 'selection_1741819_2025-11-01'...
  ✓ Search completed successfully

================================================================================
  STEP 3: LLM-BASED PRODUCT COMPARISON
================================================================================

--------------------------------------------------------------------------------
  Item 1: "Gatorade Zero Sugar Thirst Quencher Grape Sports Drink Bottles"
--------------------------------------------------------------------------------

  Found 5 potential matches in catalog
  Scraped from: Uber Eats
  Price: $12.99

  🔍 Result #1:
     Catalog Item: "Gatorade Zero Sugar Thirst Quencher Grape Sports Drink Bottles (20 fl oz x 8 ct)"
     MSID: 3300361 | Vector Similarity: 0.9534
     ✅ MATCH (Confidence: HIGH)
     Reasoning: Both products are Gatorade Zero Sugar Grape. Scraped version is missing size info.
     Factors: ✓ product_type, ✓ brand, ✓ size, ✓ variant

  🔍 Result #2:
     Catalog Item: "Gatorade Zero Sugar Thirst Quencher Lemon Lime Sports Drink (20 fl oz x 8 ct)"
     MSID: 3300362 | Vector Similarity: 0.8923
     ❌ NO MATCH (Confidence: HIGH)
     Reasoning: Different flavors - Grape vs Lemon Lime
     Factors: ✓ product_type, ✓ brand, ✓ size, ✗ variant
     Differences: Flavor: Grape vs Lemon Lime

  ✅ Best Match: Result #1
     MSID: 3300361 - Gatorade Zero Sugar Thirst Quencher Grape Sports Drink...

[... results for items 2 and 3 ...]

================================================================================
  📊 PIPELINE SUMMARY
================================================================================

  Scraping:
    • Total products scraped: 127
    • Products processed: 3

  Searching:
    • Search queries: 3
    • Average results per query: 5.0

  Comparison:
    • Total comparisons: 9
    • Matches found: 5
    • High confidence matches: 4
    • No matches: 4
    • Match rate: 55.6%

================================================================================
  ✅ PIPELINE COMPLETED SUCCESSFULLY
================================================================================
```

## Use Cases

### 1. Product Catalog Matching
Match products from external sources (Uber Eats) to your internal catalog:
```bash
python end_to_end_pipeline.py --num-items 20 --headless
```

### 2. Quality Assurance
Verify that vector search returns correct products:
```bash
python end_to_end_pipeline.py --num-items 5 --metrics
```

### 3. Catalog Coverage Analysis
Identify products that don't have good matches in your catalog:
```bash
python end_to_end_pipeline.py --num-items 50 --headless --metrics
```

### 4. Testing Different Stores
Compare catalog coverage across different stores:
```bash
python end_to_end_pipeline.py --store-id 12345 --num-items 10
```

## Pipeline Stages

### Stage 1: Scraping
- Opens Uber Eats store page in Chrome
- Handles popups and lazy loading
- Extracts product names, prices, images, stock status
- Saves to `ubereats_products.csv`

### Stage 2: Searching
- Takes product names from scraped data
- Generates embeddings for each product
- Performs vector similarity search in Qdrant
- Returns top 5 matches per product

### Stage 3: Comparison
- Compares each scraped product with top 3 search results
- Uses LLM to determine if products are the same
- Analyzes brand, size, variant, and other factors
- Provides confidence scores and detailed reasoning

## Performance Metrics

With `--metrics` flag, the pipeline reports:
- Function call counts
- Average response times
- Total execution time
- Breakdown by client (OpenAI, Qdrant)

## Error Handling

The pipeline includes comprehensive error handling:
- Graceful failure if scraping fails
- Continues processing even if some items fail
- Reports errors without stopping entire pipeline
- Always closes browser resources

## Best Practices

1. **Use headless mode** for production runs to save resources
2. **Start with small batches** (--num-items 3-5) for testing
3. **Skip scraping** if you already have fresh data
4. **Enable metrics** to identify performance bottlenecks
5. **Review match rates** to tune your vector search parameters

## Troubleshooting

### No search results found
- Ensure Qdrant collection exists and has data
- Verify store ID matches your collection
- Run `python test_refresh.py` to populate collection

### Scraping fails
- Check internet connection
- Verify URL is accessible
- Try with `--headless` flag disabled to see browser
- Update Chrome driver if needed

### Low match rates
- May indicate products not in your catalog
- Could suggest poor product naming on source
- Consider adjusting vector search parameters

## Integration

This pipeline can be integrated into:
- Scheduled jobs for regular catalog sync
- CI/CD pipelines for quality checks
- Data validation workflows
- Catalog gap analysis tools

