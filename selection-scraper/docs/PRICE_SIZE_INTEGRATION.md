# Price and Size Integration

## Overview

Added price and size information to the product comparison pipeline to improve match accuracy. The LLM now considers price and size as additional signals when comparing products.

## Changes Made

### 1. Snowflake Query Update
**File**: `workflow_steps/refresh_qdrant_collection.py`

Added `SIZE` and `PRICE_USD` fields to the Snowflake query:

```sql
SELECT
    rif.MERCHANT_SUPPLIED_ITEM_ID as MSID, 
    ctlg.UMP_ITEM_NAME as ITEM_NAME,
    ctlg.PHOTO_URL as PHOTO_URL,
    ctlg.SIZE as SIZE,
    ctlg.PRICE_USD as PRICE_USD
FROM RETAIL_INVENTORY_SERVICE.PUBLIC.RAW_INVENTORY_FEED rif
JOIN edw.cng.merchant_catalog_dlcopy ctlg
    ON rif.business_id = ctlg.business_id
    AND rif.MERCHANT_SUPPLIED_ITEM_ID = ctlg.item_merchant_supplied_id
WHERE IS_ACTIVE=true AND rif.STORE_ID={store_id}
```

### 2. Qdrant Index Update
**File**: `clients/dd_selection_qdrant_client.py`

Updated `_convert_to_qdrant_record()` to include size and price in the payload:

```python
def _convert_to_qdrant_record(self, row: pd.Series, embedding: List[float] = None) -> dict:
    record = {
        "id": str(uuid.uuid5(namespace=uuid.UUID(CollectionConfig.UUID_NAMESPACE), name=str(row["msid"]))),
        "sentence_embedding": embedding,
        "msid": row["msid"],
        "item_name": row["item_name"],
        "photo_url": row["photo_url"],
        "size": row.get("size", None),          # NEW
        "price_usd": row.get("price_usd", None) # NEW
    }
    return record
```

### 3. Comparison Workflow Update
**File**: `workflow_steps/compare_products.py`

#### Extract Size and Price from Qdrant Results
```python
result_item = {
    'item_name': point.payload.get('item_name', 'Unknown'),
    'msid': point.payload.get('msid', 'N/A'),
    'photo_url': point.payload.get('photo_url', None),
    'size': point.payload.get('size', None),            # NEW
    'price_usd': point.payload.get('price_usd', None),  # NEW
    'similarity_score': f"{point.score:.4f}" if hasattr(point, 'score') else 'N/A'
}
```

#### Pass Price and Size to LLM
```python
comparison = openai_client.compare_products(
    search_term, 
    result_item['item_name'],
    photo_url_1=scraped_photo_url,
    photo_url_2=result_item['photo_url'],
    price_1=scraped_price,              # NEW
    price_2=result_item['price_usd'],   # NEW
    size_2=result_item['size']          # NEW
)
```

#### Display Size and Price
```python
# Print size and price if available
if catalog_size:
    logger.info(f"     Size: {catalog_size}")
if catalog_price is not None:
    logger.info(f"     Price: ${catalog_price:.2f}")
```

### 4. OpenAI Client Update
**File**: `clients/openai_client.py`

#### Updated Method Signature
```python
def compare_products(
    self,
    item_name_1: str,
    item_name_2: str,
    photo_url_1: Optional[str] = None,
    photo_url_2: Optional[str] = None,
    price_1: Optional[float] = None,    # NEW
    price_2: Optional[float] = None,    # NEW
    size_1: Optional[str] = None,       # NEW
    size_2: Optional[str] = None,       # NEW
    model: str = DEFAULT_LLM_MODEL,
    **kwargs
) -> Dict[str, Any]:
```

#### Enhanced Prompt
Added comprehensive guidance for considering price:

**Price Consideration Rules:**
- Prices within ~20% variance → supports products being the same
- Prices >50% different → be cautious, may be different products/sizes
- Price alone should not be determining factor, but supports/weakens other evidence

**Updated Factors:**
- Size/Quantity is now marked as CRITICAL for matching
- Price added as factor #7 with clear usage guidelines
- Examples of size mismatches added (e.g., "12 oz" ≠ "24 oz")

#### Updated JSON Response
```json
{
    "key_factors": {
        "product_type": "match/different/uncertain",
        "brand": "match/different/uncertain",
        "size": "match/different/uncertain",
        "variant": "match/different/uncertain",
        "organic_status": "match/different/uncertain",
        "price": "similar/different/uncertain"  // NEW
    }
}
```

## Benefits

### 1. **Improved Match Accuracy**
   - Size information helps distinguish between different package sizes (e.g., 12 oz vs 24 oz)
   - Price serves as additional validation signal

### 2. **Better Differentiation**
   - Can now identify when products appear similar but have different sizes
   - Price variance helps flag potential mismatches

### 3. **Enhanced Context**
   - Provides more complete product information for comparison
   - LLM has richer context for decision-making

### 4. **Transparent Reasoning**
   - Price factor explicitly included in comparison output
   - Size displayed in formatted results

## Example Output

### Before (without price/size):
```
🔍 Result #1:
   Catalog Item: "Safeway Halloween Skeleton Flute Glass"
   MSID: 79351087 | Vector Similarity: 0.8523
   Search Photo: https://...
   Catalog Photo: https://...
   ✅ MATCH (Confidence: HIGH)
   Reasoning: Same product name and category
```

### After (with price/size):
```
🔍 Result #1:
   Catalog Item: "Safeway Halloween Skeleton Flute Glass"
   MSID: 79351087 | Vector Similarity: 0.8523
   Size: 3.1 oz
   Price: $6.17
   Search Photo: https://...
   Catalog Photo: https://...
   ✅ MATCH (Confidence: HIGH)
   Reasoning: Same product, brand, and size. Price is similar ($6.17 vs $6.17)
   Factors: ✓ product_type, ✓ brand, ✓ size, ✓ variant, ✓ organic_status, ✓ price
```

## Usage

### Refresh Collection with New Fields
```bash
python test_refresh.py
```

This will:
1. Query Snowflake with SIZE and PRICE_USD fields
2. Create/update Qdrant collection with these fields
3. Index all products with complete information

### Run Comparison Pipeline
```bash
python end_to_end_pipeline.py --skip-scraping --num-items 5
```

The pipeline will now:
1. Search Qdrant for matches
2. Extract size and price from results
3. Pass them to LLM for comparison
4. Display comprehensive comparison results

## Data Flow

```
Snowflake (SIZE, PRICE_USD)
    ↓
Qdrant Collection (indexed in payload)
    ↓
Search Results (retrieved with each point)
    ↓
Comparison Workflow (extracted from payload)
    ↓
OpenAI LLM (considers in comparison)
    ↓
Formatted Output (displayed to user)
    ↓
CSV Export (available for analysis)
```

## Testing

### Verify Data in Qdrant
```python
from clients import DDSelectionQdrantClient
from config import CollectionConfig

client = DDSelectionQdrantClient()
collection_name = CollectionConfig.get_collection_name(1741819)
results = client.search(collection_name, ["Safeway Halloween"], limit=1)

# Check payload includes size and price_usd
print(results[0].points[0].payload)
# Expected: {'msid': ..., 'item_name': ..., 'photo_url': ..., 'size': '...', 'price_usd': ...}
```

### Test Price Comparison Logic
The LLM will now evaluate:
- Similar prices (within 20%) → positive signal
- Very different prices (>50%) → caution flag
- Price + size mismatch → strong negative signal

## Notes

- Size and price are **optional** fields - comparison works even if missing
- Price variance thresholds (~20%, >50%) are guidelines for the LLM
- Size is **critical** for matching - different sizes = different products
- Price is a **supporting** factor - shouldn't be sole determining factor

## Migration

Existing collections should be refreshed to include the new fields:
```bash
python test_refresh.py  # Recreates collection with all fields
```

Old collections without size/price will continue to work but won't have these fields in comparisons.

