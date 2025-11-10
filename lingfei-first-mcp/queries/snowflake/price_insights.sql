WITH mid AS (
    SELECT submarket_id
    FROM edw.merchant.dimension_store
    WHERE store_id = :storeId
),
mid_agg AS (
    SELECT
    gpi.dd_sic                          AS dd_sic,
    ROUND(AVG(rpi.item_price) / 100.0, 2) AS aggregatePrice
    FROM edw.cng.fact_non_rx_order_item_details AS rpi
    JOIN edw.merchant.dimension_store AS mds
    ON TRY_TO_DECIMAL(rpi.store_id) = mds.store_id
    JOIN catalog_service_prod.public.product_item AS gpi
    ON rpi.business_id               = gpi.dd_business_id
    AND LOWER(rpi.item_merchant_supplied_id::VARCHAR)
        = LOWER(gpi.merchant_supplied_id::VARCHAR)
    WHERE mds.submarket_id IN (SELECT submarket_id FROM mid)
    AND rpi.delivery_created_timestamp_utc >= TO_TIMESTAMP_NTZ(:startTimeStr)
    AND rpi.delivery_created_timestamp_utc <= TO_TIMESTAMP_NTZ(:endTimeStr)
    GROUP BY gpi.dd_sic
),
RankedItems AS (
    SELECT
    gpi.dd_sic                          AS dd_sic,
    ROUND(AVG(rpi.item_price) / 100.0, 2) AS aggregatePrice,
    MIN(gpi.item_name)                  AS item_name,
    COUNT(*)                            AS order_count,
    ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS row_num
    FROM edw.cng.fact_non_rx_order_item_details AS rpi
    LEFT JOIN catalog_service_prod.public.product_item AS gpi
    ON rpi.business_id               = gpi.dd_business_id
    AND LOWER(rpi.item_merchant_supplied_id::VARCHAR)
        = LOWER(gpi.merchant_supplied_id::VARCHAR)
    WHERE rpi.store_id = :storeId
    AND rpi.delivery_created_timestamp_utc >= TO_TIMESTAMP_NTZ(:startTimeStr)
    AND rpi.delivery_created_timestamp_utc <= TO_TIMESTAMP_NTZ(:endTimeStr)
    GROUP BY gpi.dd_sic
)
SELECT
    ri.item_name        AS itemName,
    ri.aggregatePrice   AS itemPrice,
    ma.aggregatePrice   AS aggregatePrice
FROM RankedItems ri
JOIN mid_agg ma
    ON ri.dd_sic = ma.dd_sic
--WHERE ri.row_num > :offset
ORDER BY ri.row_num
LIMIT :limit;