# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %sql
# MAGIC -----------------------------------------------------
# MAGIC --1. CHECKING OVERVIEW OF THE TABLE 
# MAGIC -----------------------------------------------------
# MAGIC SELECT * FROM `sales`.`sales_case`.`sales_case_study`;
# MAGIC
# MAGIC DESCRIBE sales.sales_case.sales_case_study;
# MAGIC
# MAGIC --------------------------------------------------------------------
# MAGIC --2. CLEAN: standardise types, column names, guard against bad rows
# MAGIC -- CAST converts value from one data type to another
# MAGIC ---------------------------------------------------------------------
# MAGIC CREATE OR REPLACE TABLE sales.sales_case.sales_clean AS
# MAGIC SELECT 
# MAGIC     CAST(`Date` AS DATE) AS sale_date,                             -- the day of the sale
# MAGIC     CAST(`Sales` AS DECIMAL(18,2)) AS sales_rand,                  -- the rand value of sale
# MAGIC     CAST(`Cost Of Sales` AS DECIMAL(18,2)) AS cost_of_sales_rand,  -- what it costs the store that day
# MAGIC     CAST(`Quantity Sold` AS BIGINT) AS quantity_sold              -- number of units sold on that day
# MAGIC FROM sales.sales_case.sales_case_study
# MAGIC WHERE `Date` IS NOT NULL                -- throws out any row where the Date is blank/missing
# MAGIC     AND `Quantity Sold` IS NOT NULL     -- throws out any row where Quantity Sold is blank/missing
# MAGIC     AND `Quantity Sold` > 0;            -- throws out any row where Quantity Sold is exactly zero (or negative)
# MAGIC
# MAGIC ---------------------------------------------------------------------------
# MAGIC --3. Adding metric columns
# MAGIC ---------------------------------------------------------------------------
# MAGIC CREATE OR REPLACE TABLE sales.sales_case.sales_metrics AS
# MAGIC SELECT
# MAGIC     sale_date,
# MAGIC     sales_rand,
# MAGIC     cost_of_sales_rand,
# MAGIC     quantity_sold,
# MAGIC
# MAGIC     -- What is daily sales price per unit?
# MAGIC     ROUND(sales_rand / quantity_sold, 2) AS price_per_unit,
# MAGIC
# MAGIC     -- Working out gross profit per unit
# MAGIC     ROUND(cost_of_sales_rand / quantity_sold, 2) AS cost_per_unit,
# MAGIC
# MAGIC     -- What is the daily percentage gross profit?
# MAGIC     ROUND((sales_rand - cost_of_sales_rand) / sales_rand, 4) AS gross_profit_per,
# MAGIC
# MAGIC     -- Gross profit in plain Rand (not a %), useful for other insights
# MAGIC     ROUND(sales_rand - cost_of_sales_rand, 2) AS gross_profit_rand,
# MAGIC
# MAGIC     -- What is the daily percentage gross profit per unit?
# MAGIC     ROUND(
# MAGIC         ((sales_rand / quantity_sold) - (cost_of_sales_rand / quantity_sold))
# MAGIC         / (sales_rand / quantity_sold)
# MAGIC     , 4) AS gross_profit_pct_per_unit,
# MAGIC
# MAGIC     -- The periods during which this product was on promotion/special
# MAGIC     CASE
# MAGIC         WHEN sale_date BETWEEN '2015-11-26' AND '2015-11-28' THEN 'Black Friday Nov 2015'
# MAGIC         WHEN sale_date BETWEEN '2015-12-31' AND '2016-01-05' THEN 'New Year 2015/16'
# MAGIC         WHEN sale_date BETWEEN '2016-09-30' AND '2016-10-02' THEN 'Quarter-end Sep/Oct 2016'
# MAGIC         ELSE NULL
# MAGIC     END AS promo_period_label
# MAGIC FROM sales.sales_case.sales_clean
# MAGIC ORDER BY sale_date;
# MAGIC
# MAGIC -------------------------------------------------------------------------
# MAGIC --4. The average unit sales price of this product
# MAGIC -------------------------------------------------------------------------
# MAGIC SELECT
# MAGIC     ROUND(AVG(price_per_unit), 2) AS avg_unit_price_simple,
# MAGIC     ROUND(SUM(sales_rand) / SUM(quantity_sold), 2) AS avg_unit_price_volume_weighted
# MAGIC FROM sales.sales_case.sales_metrics;
# MAGIC
# MAGIC -------------------------------------------------------------------------
# MAGIC --4b. Overall gross profit % (sum-then-divide — the correct KPI figure)
# MAGIC -------------------------------------------------------------------------
# MAGIC SELECT
# MAGIC     ROUND(SUM(sales_rand), 2) AS total_sales,
# MAGIC     ROUND(SUM(cost_of_sales_rand), 2) AS total_cost_of_sales,
# MAGIC     ROUND((SUM(sales_rand) - SUM(cost_of_sales_rand)) / SUM(sales_rand) * 100, 2) AS avg_gross_profit_pct
# MAGIC FROM sales.sales_case.sales_metrics;
# MAGIC
# MAGIC -------------------------------------------------------------------------
# MAGIC --4c. Worst margin months (for a KPI card / callout)
# MAGIC -------------------------------------------------------------------------
# MAGIC SELECT
# MAGIC     date_format(sale_date, 'yyyy-MM') AS month,
# MAGIC     ROUND((SUM(sales_rand) - SUM(cost_of_sales_rand)) / SUM(sales_rand) * 100, 2) AS gross_profit_pct
# MAGIC FROM sales.sales_case.sales_metrics
# MAGIC GROUP BY date_format(sale_date, 'yyyy-MM')
# MAGIC ORDER BY gross_profit_pct ASC
# MAGIC LIMIT 5;
# MAGIC
# MAGIC ----------------------------------------------------------------------------
# MAGIC --5. Price Elasticity of Demand during each promo period
# MAGIC -- Price elasticity of demand answers: "If I change the price, how much
# MAGIC -- does the quantity people buy change?"
# MAGIC -- Promo = what price and quantity looked like during the promotional days
# MAGIC -- Baseline = the 14 days immediately before AND the 14 days immediately
# MAGIC --            after each promo (local baseline, controls for seasonality)
# MAGIC ----------------------------------------------------------------------------
# MAGIC WITH promo_avg AS (
# MAGIC     SELECT
# MAGIC         promo_period_label,
# MAGIC         MIN(sale_date) AS promo_start,
# MAGIC         MAX(sale_date) AS promo_end,
# MAGIC         AVG(price_per_unit) AS promo_price,
# MAGIC         AVG(quantity_sold)  AS promo_qty
# MAGIC     FROM sales.sales_case.sales_metrics
# MAGIC     WHERE promo_period_label IS NOT NULL
# MAGIC     GROUP BY promo_period_label
# MAGIC ),
# MAGIC
# MAGIC baseline_avg AS (
# MAGIC     SELECT
# MAGIC         p.promo_period_label,
# MAGIC         AVG(m.price_per_unit) AS baseline_price,
# MAGIC         AVG(m.quantity_sold)  AS baseline_qty
# MAGIC     FROM promo_avg p
# MAGIC     JOIN sales.sales_case.sales_metrics m
# MAGIC       ON m.sale_date BETWEEN DATE_SUB(p.promo_start, 14) AND DATE_SUB(p.promo_start, 1)
# MAGIC       OR m.sale_date BETWEEN DATE_ADD(p.promo_end, 1) AND DATE_ADD(p.promo_end, 14)
# MAGIC     GROUP BY p.promo_period_label
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     p.promo_period_label,
# MAGIC     p.promo_start,
# MAGIC     p.promo_end,
# MAGIC     ROUND(b.baseline_price, 2) AS baseline_avg_price,
# MAGIC     ROUND(p.promo_price, 2)    AS promo_avg_price,
# MAGIC     ROUND((p.promo_price - b.baseline_price) / b.baseline_price, 4) AS pct_change_price,
# MAGIC     ROUND(b.baseline_qty, 0)   AS baseline_avg_qty,
# MAGIC     ROUND(p.promo_qty, 0)      AS promo_avg_qty,
# MAGIC     ROUND((p.promo_qty - b.baseline_qty) / b.baseline_qty, 4)       AS pct_change_qty,
# MAGIC     ROUND(
# MAGIC         ((p.promo_qty - b.baseline_qty) / b.baseline_qty)
# MAGIC         / ((p.promo_price - b.baseline_price) / b.baseline_price)
# MAGIC     , 2) AS price_elasticity_of_demand
# MAGIC FROM promo_avg p
# MAGIC JOIN baseline_avg b USING (promo_period_label)
# MAGIC ORDER BY promo_start;
# MAGIC
# MAGIC SELECT * FROM sales.sales_case.sales_clean;