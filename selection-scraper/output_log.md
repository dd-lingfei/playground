✓ OpenAIClient singleton initialized

====================================================================================================
  🚀 END-TO-END PRODUCT MATCHING PIPELINE
====================================================================================================

  Configuration:
    • Uber Eats URL: https://www.ubereats.com/store/safeway-6911-coal-creek-pkwy-ses/xNI-v9wZW7ijmryi...
    • Store ID: 1741819
    • Collection: selection_1741819_2025-11-01
    • Items to process: 3
    • Headless mode: False

====================================================================================================
  STEP 1: USING EXISTING SCRAPED DATA
====================================================================================================
  Loading products from ubereats_products.csv...

  ✓ Loaded 141 products from ubereats_products.csv

  📋 Processing first 3 items:
     1. Safeway Halloween Skeleton Flute Glass (3.1 oz)
     2. IG Design Group Halloween Spooky Eyes Suction Window Decoration, Purple
     3. Crazy Bonez Halloween Decor

====================================================================================================
  STEP 2: SEARCHING IN QDRANT
====================================================================================================

  Searching for 3 products in collection 'selection_1741819_2025-11-01'...
✓ DDSelectionQdrantClient singleton initialized
Searching for 3 terms in collection: selection_1741819_2025-11-01
  ✓ Search completed successfully

====================================================================================================
  STEP 3: LLM-BASED PRODUCT COMPARISON
====================================================================================================

----------------------------------------------------------------------------------------------------
  Item 1: "Safeway Halloween Skeleton Flute Glass (3.1 oz)"
----------------------------------------------------------------------------------------------------

  Found 5 potential matches in catalog
  Scraped from: Uber Eats
  Price: $6.17

  🔍 Result #1:
     Catalog Item: "Safeway Skeleton Hand Flute Halloween Party Decor"
     MSID: 79351087 | Vector Similarity: 0.8432
     Search Photo: https://tb-static.uber.com/prod/image-proc/processed_images/8c8bef142b867304dc260686b2a4952c/b4665c191b34baf3d0e0fa45dfdd3d1d.jpeg
     Catalog Photo: https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3.amazonaws.com/media/photosV2/31faa118-cd39-4ac4-b985-dd668f3e2a4a-retina-large.jpg
     [92m✅ MATCH[0m (Confidence: MEDIUM)
     Reasoning: Both are Safeway-branded Halloween skeleton-themed champagne flute glasses. One listing specifies capacity (3.1 oz) while the other emphasizes party decor and 'skeleton hand' styling, which is consistent with the same novelty flute. No conflicting size/pack or variant details are present.
     Factors: ✓ product type, ✓ brand, ? size, ✓ variant, ✓ organic status

  🔍 Result #2:
     Catalog Item: "Safeway Skeleton Hand Flute Halloween Party Decor"
     MSID: 79354242 | Vector Similarity: 0.8431
     Search Photo: https://tb-static.uber.com/prod/image-proc/processed_images/8c8bef142b867304dc260686b2a4952c/b4665c191b34baf3d0e0fa45dfdd3d1d.jpeg
     Catalog Photo: https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3.amazonaws.com/media/photosV2/31faa118-cd39-4ac4-b985-dd668f3e2a4a-retina-large.jpg
     [92m✅ MATCH[0m (Confidence: MEDIUM)
     Reasoning: Both listings are Safeway-branded Halloween skeleton-themed flute glasses; names strongly indicate the same novelty champagne flute. Product 2 lacks size details, so size/variant specifics are uncertain but no conflicting info is present.
     Factors: ✓ product type, ✓ brand, ? size, ? variant, ✓ organic status

  🔍 Result #3:
     Catalog Item: "Safeway Table Top 3D Halloween"
     MSID: 79354339 | Vector Similarity: 0.6861
     Search Photo: https://tb-static.uber.com/prod/image-proc/processed_images/8c8bef142b867304dc260686b2a4952c/b4665c191b34baf3d0e0fa45dfdd3d1d.jpeg
     Catalog Photo: https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3.amazonaws.com/media/photosV2/20175ab7-82e5-48da-b9ff-5f2872546e49-retina-large.jpg
     [91m❌ NO MATCH[0m (Confidence: HIGH)
     Reasoning: Product 1 is a 3.1 oz skeleton flute glass (drinkware), while Product 2 is a table-top 3D Halloween decoration. Different product types and variants; size is only provided for Product 1.
     Factors: ✗ product type, ✓ brand, ? size, ✗ variant, ✓ organic status
     Differences: Product type: drinkware (flute glass) vs table-top 3D decoration; Variant/design: skeleton flute vs unspecified 3D table-top decor; Size provided for Product 1 (3.1 oz); none for Product 2; Intended use: beverage glass vs decorative item

  ✅ Best Match: Result #1
     MSID: 79351087 - Safeway Skeleton Hand Flute Halloween Party Decor...

----------------------------------------------------------------------------------------------------
  Item 2: "IG Design Group Halloween Spooky Eyes Suction Window Decoration, Purple"
----------------------------------------------------------------------------------------------------

  Found 5 potential matches in catalog
  Scraped from: Uber Eats
  Price: $16.30

  🔍 Result #1:
     Catalog Item: "IG Design Group Light Up Shimmer Eyes Decor Purple"
     MSID: 79352581 | Vector Similarity: 0.7403
     Search Photo: https://tb-static.uber.com/prod/image-proc/processed_images/2c2f860983409f08f84df0b8c7271905/b4665c191b34baf3d0e0fa45dfdd3d1d.jpeg
     Catalog Photo: https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3.amazonaws.com/media/photosV2/1d1ec83b-a687-426d-8ec5-0e038238d60b-retina-large.jpg
     [91m❌ NO MATCH[0m (Confidence: MEDIUM)
     Reasoning: Although both are IG Design Group purple Halloween eye-themed decor, one specifies a light-up 'Shimmer' feature while the other is a 'Suction Window' decoration without mention of lighting, indicating different variants/functions.
     Factors: ✓ product type, ✓ brand, ? size, ✗ variant, ✓ organic status
     Differences: Product 2 specifies light-up 'Shimmer' feature; Product 1 does not mention lighting; Product 1 specifies 'Suction Window' installation; Product 2 does not mention suction; Different variant names: 'Spooky Eyes' vs 'Shimmer Eyes'

  🔍 Result #2:
     Catalog Item: "IG Design Group Light Up Shimmer Eyes Decor Orange"
     MSID: 79352582 | Vector Similarity: 0.6506
     Search Photo: https://tb-static.uber.com/prod/image-proc/processed_images/2c2f860983409f08f84df0b8c7271905/b4665c191b34baf3d0e0fa45dfdd3d1d.jpeg
     Catalog Photo: https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3.amazonaws.com/media/photos/39688139-99ad-4863-9b9a-5be170cd7c72-retina-large-jpeg
     [91m❌ NO MATCH[0m (Confidence: HIGH)
     Reasoning: Both are IG Design Group Halloween eye decorations, but they differ in color (purple vs orange) and features (suction window decoration vs light-up shimmer decor). These variant differences indicate different products.
     Factors: ✓ product type, ✓ brand, ? size, ✗ variant, ✓ organic status
     Differences: Color: Purple vs Orange; Feature: Suction window decoration vs Light-up shimmer decor; Mounting/Use: Suction window-specific vs general decor

  🔍 Result #3:
     Catalog Item: "Fun World Pumpkin Pro 8 Plus Decoration Red Flashing Eyeballs"
     MSID: 79354283 | Vector Similarity: 0.5770
     Search Photo: https://tb-static.uber.com/prod/image-proc/processed_images/2c2f860983409f08f84df0b8c7271905/b4665c191b34baf3d0e0fa45dfdd3d1d.jpeg
     Catalog Photo: https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3.amazonaws.com/media/photosV2/2302fde1-94ff-4f87-8949-ea8d9a3ec655-retina-large.jpg
     [91m❌ NO MATCH[0m (Confidence: HIGH)
     Reasoning: Different brands and distinct variants/features: one is a purple suction window spooky eyes decoration by IG Design Group, the other is a Fun World Pumpkin Pro 8 Plus with red flashing eyeballs. These are not the same product.
     Factors: ✓ product type, ✗ brand, ? size, ✗ variant, ✓ organic status
     Differences: Brand: IG Design Group vs Fun World; Variant/features: Purple suction window spooky eyes vs Red flashing eyeballs (Pumpkin Pro 8 Plus); Format/usage: Window suction decoration vs electronic flashing eyeball decoration; Product line: IG Design Group Halloween vs Fun World Pumpkin Pro 8 Plus

  ⚠️  No confident matches found in top 3 results

----------------------------------------------------------------------------------------------------
  Item 3: "Crazy Bonez Halloween Decor"
----------------------------------------------------------------------------------------------------

  Found 5 potential matches in catalog
  Scraped from: Uber Eats
  Price: $17.98

  🔍 Result #1:
     Catalog Item: "Crazy Bonez Buddy Puppy Bonez"
     MSID: 79354353 | Vector Similarity: 0.7004
     Search Photo: https://tb-static.uber.com/prod/image-proc/processed_images/4817fbe161ab69c172f60613c6ae6c90/b4665c191b34baf3d0e0fa45dfdd3d1d.jpeg
     Catalog Photo: https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3.amazonaws.com/media/photosV2/e7d16019-4ff4-43aa-b9d4-0c3151de38e2-retina-large.jpg
     [91m❌ NO MATCH[0m (Confidence: MEDIUM)
     Reasoning: Product 1 is a generic Crazy Bonez Halloween decor item with no specific model indicated, while Product 2 is a specific variant: Buddy Puppy Bonez (skeleton puppy). Without explicit confirmation that Product 1 is the same puppy variant, they should be treated as different.
     Factors: ? product type, ✓ brand, ? size, ✗ variant, ✓ organic status
     Differences: Product 1 is a generic 'Halloween Decor' listing; Product 2 specifies 'Buddy Puppy Bonez' (skeleton dog); Variant/model specificity differs (unspecified vs Buddy Puppy); Size/quantity not provided for Product 1; Product 2 implies a specific sized figure

  🔍 Result #2:
     Catalog Item: "Seasons Puppy Bonez Skeleton Decoration"
     MSID: 79352392 | Vector Similarity: 0.6206
     Search Photo: https://tb-static.uber.com/prod/image-proc/processed_images/4817fbe161ab69c172f60613c6ae6c90/b4665c191b34baf3d0e0fa45dfdd3d1d.jpeg
     Catalog Photo: https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3.amazonaws.com/media/photosV2/4544f032-bbaf-484a-b304-309d83d5ab46-retina-large
     [91m❌ NO MATCH[0m (Confidence: HIGH)
     Reasoning: Different brands and one title specifies a 'Puppy Bonez' skeleton while the other is a generic Crazy Bonez Halloween decor. Brand difference alone makes them different products.
     Factors: ✓ product type, ✗ brand, ? size, ? variant, ✓ organic status
     Differences: Brand: Crazy Bonez vs Seasons; Specificity: generic Halloween decor vs 'Puppy Bonez' skeleton decoration; Possible model/size differences not specified

  🔍 Result #3:
     Catalog Item: "Safeway Skeleton Hand Flute Halloween Party Decor"
     MSID: 79351087 | Vector Similarity: 0.6023
     Search Photo: https://tb-static.uber.com/prod/image-proc/processed_images/4817fbe161ab69c172f60613c6ae6c90/b4665c191b34baf3d0e0fa45dfdd3d1d.jpeg
     Catalog Photo: https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3.amazonaws.com/media/photosV2/31faa118-cd39-4ac4-b985-dd668f3e2a4a-retina-large.jpg
     [91m❌ NO MATCH[0m (Confidence: MEDIUM)
     Reasoning: Product 1 is a generic 'Crazy Bonez' Halloween decor item with no specified type, while Product 2 is a specific 'Skeleton Hand Flute' listed under Safeway. The brands differ and the second item indicates a specific decor/drinkware piece, suggesting different products.
     Factors: ✓ product type, ✗ brand, ? size, ✗ variant, ✓ organic status
     Differences: Brand: Crazy Bonez vs Safeway; Specific item type: generic Halloween decor vs Skeleton Hand Flute (glass/drinkware decor); Variant/details unspecified for Product 1

  ⚠️  No confident matches found in top 3 results

====================================================================================================
  📊 PIPELINE SUMMARY
====================================================================================================

  Scraping:
    • Total products scraped: 141
    • Products processed: 3

  Searching:
    • Search queries: 3
    • Average results per query: 5.0

  Comparison:
    • Total comparisons: 9
    • Matches found: 2
    • High confidence matches: 0
    • No matches: 7
    • Match rate: 22.2%

  Export:
    • CSV file: comparison_results_1741819_20251101_222233.csv
    • Total rows: 3
    • Items found in DD: 1

====================================================================================================
  ✅ PIPELINE COMPLETED SUCCESSFULLY
====================================================================================================

