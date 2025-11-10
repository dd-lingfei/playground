-- Data source: Snowflake
with store_items as (
SELECT
  dmi.MERCHANT_SUPPLIED_ID,
  dmi.ITEM_ID as item_id,
  dmi.store_id 
FROM
  edw.merchant.dimension_menu_item dmi join 
  PRODDB.PUBLIC.DIMENSION_STORE ds on
  dmi.store_id=ds.store_id
WHERE
  1=1
  -- case when m.business_vertical_id in (166,167) 
  -- BUSINESS_ID in ('11116009','979026','331358')
  -- UPPER('%{{ search_text }}%')
  and dmi.merchant_supplied_id = '{{search_item_msid}}'
  -- PLACEHOLDER FOR BUSINESS_ID FILTER --
)

SELECT
  mi.store_id,
  mi.item_title AS item_name,
  category_id,
  mi.item_created_at,
  menu_id,
  mi.MERCHANT_SUPPLIED_ID,
  mi.ddsic,
  mi.ITEM_ID,
  mi.SCD_START_DATE AS suspension_start,
  mi.SCD_END_DATE AS suspension_end,
  mi.ITEM_SUSPENSION_REASON AS suspension_reason,
  mi.ITEM_SUSPENSION_TYPE as suspension_type,
  mi.IS_ITEM_SUSPENDED as is_suspended,
  mi.IS_MENU_ACTIVE,
  is_alcohol,
  price / 100 AS price
FROM
  PRODDB.PUBLIC.AUDIT_MENU_ITEM AS mi JOIN
  store_items on mi.MERCHANT_SUPPLIED_ID=store_items.MERCHANT_SUPPLIED_ID
  and mi.store_id=store_items.store_id 
  and mi.item_id=store_items.ITEM_ID
WHERE
  1=1
  and mi.ITEM_CREATED_AT >= dateadd('DAY',-3,GETDATE())
  limit 50 