 --Weekly Version (Last 8 full weeks)
with
  start_date as (
    select
      date_trunc ('day', current_date - 30)
  ),
  end_date as (
    select
      dateadd (day, -1, date_trunc ('day', current_date))
  ), --(select dateadd (week,-1,date_trunc('week', current_date))),
  store_list as (
    select
        store_id,
        business_id,
        business_name,
        business_line,
        pick_model,
        org, 
        country_code
  from edw.cng.dimension_new_vertical_store_tags
    where business_line is not null
    and pick_model = 'DASHER_PICK'
--     and business_line in ('Grocery','3P Convenience')--,'AlcoholVert','Pets','Active & Office','Home & Wellness')
--    and COUNTRY_CODE = 'US'
    and business_id = '{{search_business_id}}'

          ),
          base_data AS (
            select
              pi.delivery_uuid,
              pi.iguazu_sent_at,
              pi.finish_pick_at,
              pi.dasher_id,
              pick.value: store_id:: float as store_id,
              pick.value: merchant_supplied_id:: varchar as merchant_supplied_id,
              pick.value: item_found_status:: varchar as item_found_status
            from
              IGUAZU.SERVER_EVENTS_PRODUCTION.cng_finish_pick_items_found_status pi,
              lateral flatten (input => parse_json (pi.item_statuses)) pick
            order by
              2 desc
          ),
          starting_points AS (
            SELECT DISTINCT
              STARTING_POINT_NAME,
              starting_point_id,
              submarket_name
            from
              PRODDB.PUBLIC.DIMENSION_STORE
          ) --WHERE  submarket_name  ilike '%philadelphia%')
        SELECT
          date_trunc (
            'hour',
            CONVERT_TIMEZONE ('UTC', 'America/New_York', iguazu_sent_at)
          ) as hour,
          business_line,
          SUM(
            CASE
              WHEN item_found_status = 'ITEM_NOT_FOUND' THEN 1
              ELSE 0
            END
          ) as inf_count,
          COUNT(*) as item_count,
          SUM(
            CASE
              WHEN item_found_status = 'ITEM_NOT_FOUND' THEN 1
              ELSE 0
            END
          ) / COUNT(*) as inf_rate
        FROM
          base_data bd
          JOIN PRODDB.PUBLIC.DIMENSION_DASHER dd ON TRY_CAST (dd.dasher_id AS NUMBER) = TRY_CAST (bd.dasher_id AS NUMBER)
          AND dd.LAST_STARTING_POINT_ID IN (
            SELECT
              starting_point_id
            FROM
              starting_points
          )
          join store_list s on bd.store_id = s.store_id
        WHERE
          iguazu_sent_at > current_timestamp - interval '384 hours'
        GROUP BY
          1,2
        ORDER BY
          1 DESC