-- 1. submarket store_id list
WITH target_submarket AS (
  SELECT submarket_id
  FROM edw.merchant.dimension_store
  WHERE store_id = {{input_store_id}}
),
target_bvid AS (
  SELECT BUSINESS_VERTICAL_ID 
  FROM edw.cng.dimension_new_vertical_store_tags 
  where STORE_ID = {{input_store_id}}
),
stores_same_bvid AS (
  SELECT STORE_ID 
  FROM edw.cng.dimension_new_vertical_store_tags 
  WHERE BUSINESS_VERTICAL_ID IN (SELECT BUSINESS_VERTICAL_ID FROM target_bvid)
),
filtered_stores AS (
  SELECT store_id
  FROM edw.merchant.dimension_store
  WHERE submarket_id IN (SELECT submarket_id FROM target_submarket)
  AND STORE_ID IN (SELECT STORE_ID FROM stores_same_bvid)
),

-- 2. aggregated by dd_sic: dd_sic, order_number, sample_item
submarket_stats AS (
  SELECT
    ctlg.dd_sic,
    COUNT(*) AS order_number,
    COUNT(DISTINCT rpi.STORE_ID) as store_number,
    ANY_VALUE(rpi.item_name) AS sample_item,
    ROUND(AVG(rpi.item_price) / 100.0, 2) AS aggregate_price
  FROM edw.cng.fact_non_rx_order_item_details rpi
  JOIN filtered_stores fs
    ON TRY_TO_DECIMAL(rpi.store_id) = fs.store_id
  JOIN edw.cng.merchant_catalog_dlcopy ctlg
    ON rpi.business_id = ctlg.business_id
    AND rpi.item_merchant_supplied_id = ctlg.item_merchant_supplied_id
  WHERE rpi.delivery_created_at::date > DATEADD(day, -365, current_date)
    AND ctlg.DD_SIC IS NOT NULL
  GROUP BY ctlg.dd_sic
),

-- 3. Top 1000 dd_sic
top_x AS (
  SELECT
    dd_sic,
    sample_item,
    order_number,
    store_number,
    aggregate_price
  FROM submarket_stats
  ORDER BY order_number DESC
  LIMIT {{input_limit}}
),

-- 4. dd_sic list of THE store
store_covered AS (
  SELECT DISTINCT
    ctlg.dd_sic
  FROM edw.merchant.dimension_menu_item dmi
  JOIN edw.merchant.dimension_menu dm
    ON dmi.MENU_ID = dm.MENU_ID
  JOIN edw.cng.merchant_catalog_dlcopy ctlg
    ON dm.business_id = ctlg.business_id
    AND dmi.merchant_supplied_id = ctlg.item_merchant_supplied_id
  WHERE TRY_TO_DECIMAL(dmi.store_id) = {{input_store_id}}
  AND ctlg.DD_SIC IS NOT NULL
  AND dmi.IS_MENU_ACTIVE = 1
  AND dmi.IS_ITEM_ACTIVE = 1
  AND dm.IS_ACTIVE = 1
),

-- 5. dd_sic not covered by Top1000 in THE store
missing_cover AS (
  SELECT
    t.dd_sic,
    t.sample_item AS item_name,
    t.order_number,
    t.store_number,
    t.aggregate_price
  FROM top_x t
  LEFT JOIN store_covered sc
    ON t.dd_sic = sc.dd_sic
  WHERE sc.dd_sic IS NULL
)

-- Final result
SELECT 
  mc.dd_sic as ddSic,
  mc.item_name as itemName,
  mc.order_number as orderNumber,
  mc.store_number as storeNumber,
  mc.aggregate_price as aggregatePrice,
  (SELECT count(*) from filtered_stores) as storeCountSubmarket
FROM missing_cover mc
ORDER BY order_number DESC