-- Databricks notebook source
-----------------------------------------------------
--1. CHECKING OVERVIEW OF THE TABLE 
-----------------------------------------------------
SELECT * FROM `sales`.`sales_case`.`sales_case_study`;

DESCRIBE sales.sales_case.sales_case_study;

--------------------------------------------------------------------
--2. CLEAN: standardise types, column names, guard against bad rows
-- CAST converts value from one data type to another
---------------------------------------------------------------------
CREATE OR REPLACE TABLE sales.sales_case.sales_clean AS
SELECT 
    CAST(`Date` AS DATE) AS sale_date,                             -- the day of the sale
    CAST(`Sales` AS DECIMAL(18,2)) AS sales_rand,                  -- the rand value of sale
    CAST(`Cost Of Sales` AS DECIMAL(18,2)) AS cost_of_sales_rand,  -- what it costs the store that day
    CAST(`Quantity Sold` AS BIGINT) AS quantity_sold              -- number of units sold on that day
FROM sales.sales_case.sales_case_study
WHERE `Date` IS NOT NULL                -- throws out any row where the Date is blank/missing
    AND `Quantity Sold` IS NOT NULL     -- throws out any row where Quantity Sold is blank/missing
    AND `Quantity Sold` > 0;            -- throws out any row where Quantity Sold is exactly zero (or negative)

---------------------------------------------------------------------------
--3. Adding metric columns
---------------------------------------------------------------------------
CREATE OR REPLACE TABLE sales.sales_case.sales_metrics AS
SELECT
    sale_date,
    sales_rand,
    cost_of_sales_rand,
    quantity_sold,

    -- What is daily sales price per unit?
    ROUND(sales_rand / quantity_sold, 2) AS price_per_unit,

    -- Working out gross profit per unit
    ROUND(cost_of_sales_rand / quantity_sold, 2) AS cost_per_unit,

    -- What is the daily percentage gross profit?
    ROUND((sales_rand - cost_of_sales_rand) / sales_rand, 4) AS gross_profit_per,

    -- Gross profit in plain Rand (not a %), useful for other insights
    ROUND(sales_rand - cost_of_sales_rand, 2) AS gross_profit_rand,

    -- What is the daily percentage gross profit per unit?
    ROUND(
        ((sales_rand / quantity_sold) - (cost_of_sales_rand / quantity_sold))
        / (sales_rand / quantity_sold)
    , 4) AS gross_profit_pct_per_unit,

    -- The periods during which this product was on promotion/special
    CASE
        WHEN sale_date BETWEEN '2015-11-26' AND '2015-11-28' THEN 'Black Friday Nov 2015'
        WHEN sale_date BETWEEN '2015-12-31' AND '2016-01-05' THEN 'New Year 2015/16'
        WHEN sale_date BETWEEN '2016-09-30' AND '2016-10-02' THEN 'Quarter-end Sep/Oct 2016'
        ELSE NULL
    END AS promo_period_label
FROM sales.sales_case.sales_clean
ORDER BY sale_date;

-------------------------------------------------------------------------
--4. The average unit sales price of this product
-------------------------------------------------------------------------
SELECT
    ROUND(AVG(price_per_unit), 2) AS avg_unit_price_simple,
    ROUND(SUM(sales_rand) / SUM(quantity_sold), 2) AS avg_unit_price_volume_weighted
FROM sales.sales_case.sales_metrics;

-------------------------------------------------------------------------
--4b. Overall gross profit % (sum-then-divide — the correct KPI figure)
-------------------------------------------------------------------------
SELECT
    ROUND(SUM(sales_rand), 2) AS total_sales,
    ROUND(SUM(cost_of_sales_rand), 2) AS total_cost_of_sales,
    ROUND((SUM(sales_rand) - SUM(cost_of_sales_rand)) / SUM(sales_rand) * 100, 2) AS avg_gross_profit_pct
FROM sales.sales_case.sales_metrics;

-------------------------------------------------------------------------
--4c. Worst margin months (for a KPI card / callout)
-------------------------------------------------------------------------
SELECT
    date_format(sale_date, 'yyyy-MM') AS month,
    ROUND((SUM(sales_rand) - SUM(cost_of_sales_rand)) / SUM(sales_rand) * 100, 2) AS gross_profit_pct
FROM sales.sales_case.sales_metrics
GROUP BY date_format(sale_date, 'yyyy-MM')
ORDER BY gross_profit_pct ASC
LIMIT 5;

----------------------------------------------------------------------------
--5. Price Elasticity of Demand during each promo period
-- Price elasticity of demand answers: "If I change the price, how much
-- does the quantity people buy change?"
-- Promo = what price and quantity looked like during the promotional days
-- Baseline = the 14 days immediately before AND the 14 days immediately
--            after each promo (local baseline, controls for seasonality)
----------------------------------------------------------------------------
WITH promo_avg AS (
    SELECT
        promo_period_label,
        MIN(sale_date) AS promo_start,
        MAX(sale_date) AS promo_end,
        AVG(price_per_unit) AS promo_price,
        AVG(quantity_sold)  AS promo_qty
    FROM sales.sales_case.sales_metrics
    WHERE promo_period_label IS NOT NULL
    GROUP BY promo_period_label
),

baseline_avg AS (
    SELECT
        p.promo_period_label,
        AVG(m.price_per_unit) AS baseline_price,
        AVG(m.quantity_sold)  AS baseline_qty
    FROM promo_avg p
    JOIN sales.sales_case.sales_metrics m
      ON m.sale_date BETWEEN DATE_SUB(p.promo_start, 14) AND DATE_SUB(p.promo_start, 1)
      OR m.sale_date BETWEEN DATE_ADD(p.promo_end, 1) AND DATE_ADD(p.promo_end, 14)
    GROUP BY p.promo_period_label
)

SELECT
    p.promo_period_label,
    p.promo_start,
    p.promo_end,
    ROUND(b.baseline_price, 2) AS baseline_avg_price,
    ROUND(p.promo_price, 2)    AS promo_avg_price,
    ROUND((p.promo_price - b.baseline_price) / b.baseline_price, 4) AS pct_change_price,
    ROUND(b.baseline_qty, 0)   AS baseline_avg_qty,
    ROUND(p.promo_qty, 0)      AS promo_avg_qty,
    ROUND((p.promo_qty - b.baseline_qty) / b.baseline_qty, 4)       AS pct_change_qty,
    ROUND(
        ((p.promo_qty - b.baseline_qty) / b.baseline_qty)
        / ((p.promo_price - b.baseline_price) / b.baseline_price)
    , 2) AS price_elasticity_of_demand
FROM promo_avg p
JOIN baseline_avg b USING (promo_period_label)
ORDER BY promo_start;

SELECT * FROM sales.sales_case.sales_clean;

SELECT * FROM sales.sales_case.sales_metrics
ORDER BY sale_date;