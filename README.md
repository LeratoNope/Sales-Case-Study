# 📊 Project Overview

Welcome to the **Elastic Edge Sales Case Study** project.

This project was developed as part of a Data Analyst case study and follows an end-to-end data analytics workflow — from raw transactional data through to cleaning, analysis, interactive dashboards, business insights, and executive recommendations.

The goal was to transform daily retail sales data into meaningful business intelligence that can help management understand how price changes affect demand, where profitability is being won or lost, and whether promotions are actually paying off.

### From Sales Data to Business Intelligence

`Raw Data` → `Clean Data` → `Analysis` → `Visualization` → `Insights` → `Recommendations`

---

## 🎯 Business Challenge

This case study explores the analysis of daily transactional sales data to answer key pricing and promotional questions, and provide data-driven recommendations.

The analysis focused on:

- 💰 What is the average unit sales price of this product?
- 📉 What is the daily percentage gross profit, and gross profit per unit?
- 🎯 How sensitive is demand to price during promotional periods? (Price Elasticity of Demand)
- 📆 Did the Black Friday, New Year, and Quarter-end promotions actually pay off?
- ⚠️ Is the product profitable overall, and has that changed over time?
- 🧭 What pricing or promotional strategy should management pursue next?

The project was designed to move beyond simply visualizing the data, and instead use it to support real business decision-making.

---

## 🗂️ The Data

The project used daily transactional sales data for a single retail product, covering **30 December 2013 – 16 November 2016** (1,053 days).

Key fields included:

- `Date`
- `Sales` (Rand)
- `Cost of Sales` (Rand)
- `Quantity Sold`

Additional analytical fields were created during the data transformation process to support time-based and pricing analysis.

---

## 🧹 From Raw Data to Clean Data

Before analysis could begin, the raw dataset required cleaning and transformation.

This stage was completed in **Databricks using SQL**.

### Data Cleaning & Transformation

The main preparation steps included:

**🔢 Standardising Data Types**

The original fields were cast into consistent types:

`sale_date` → `DATE`, `sales_rand` / `cost_of_sales_rand` → `DECIMAL(18,2)`, `quantity_sold` → `BIGINT`

Rows with missing dates or zero/blank quantity sold were removed to guard against bad data.

**💵 Calculating Price Metrics**

Daily sales price per unit was calculated using:

`sales_rand / quantity_sold`

This produced `price_per_unit`, along with a matching `cost_per_unit`.

**📊 Calculating Gross Profit Metrics**

Three separate profitability fields were created:

- `gross_profit_rand` — plain Rand profit (Sales − Cost of Sales)
- `gross_profit_per` — daily percentage gross profit
- `gross_profit_pct_per_unit` — daily percentage gross profit, calculated per unit

**🏷️ Tagging Promotional Periods**

Each day was labeled against three known promotional windows:

- Black Friday (Nov 2015)
- New Year (Dec 2015 / Jan 2016)
- Quarter-end (Sep/Oct 2016)

This became the `promo_period_label` field used throughout the elasticity analysis.

---

## 🧼 Clean Analytical Dataset

The cleaned dataset was stored in Databricks as:

`sales.sales_case.sales_metrics`

This table became the foundation for all subsequent analysis and dashboard development.

### SQL & Databricks

SQL was used extensively throughout the data preparation process.

Key SQL techniques included:

- `CAST` type conversion
- `CASE WHEN` conditional labeling
- `ROUND`, aggregate functions (`SUM`, `AVG`)
- `WITH` (CTEs) for elasticity comparisons
- `JOIN` between promo and baseline periods
- `GROUP BY` and `ORDER BY`
- Date functions (`DATE_SUB`, `DATE_ADD`, `date_format`)
- `CREATE OR REPLACE TABLE`

This stage demonstrated the importance of preparing reliable data before moving into visualization and business analysis.

---

## 💡 Turning Data Into Insights

Once the data had been cleaned and transformed, the next step was to explore it and identify meaningful patterns.

The analysis focused on four major areas:

**📈 Pricing & Elasticity**

Understanding how price and quantity moved together during:

- Promotional periods vs. baseline periods
- Different baseline methods (all non-promo days vs. a ±14-day local window)

**💰 Profitability**

Identifying:

- Overall average gross profit %
- Whether cost of sales consistently tracked sales revenue
- Which months had the weakest margins

**📆 Time-Based Performance**

Understanding how sales, cost, and margin performance changed:

- Month over month
- Across the full 3-year period

**🎯 Promotion Performance**

Using price elasticity of demand to understand:

- Which promotions genuinely drove profitable volume
- Which promotions had a negligible or unclear price effect

---

## 📊 Dashboard Development

To demonstrate the ability to communicate insights through different business intelligence platforms, the analysis was developed across multiple visualization platforms.

### 📗 Microsoft Excel *(in progress)*

Excel is being used for detailed exploratory analysis and pricing dashboard development.

The Excel workflow includes:

- Pivot tables
- Pivot charts
- Gross profit % verification
- Elasticity summary tables
- Dashboard design

### 📘 Power BI

Power BI was used to develop an interactive business intelligence version of the promo and elasticity analysis.

The Power BI dashboard focused on:

- KPI cards (Total Sales, Total Quantity Sold, Avg Gross Profit %)
- Interactive promo-period buttons
- Promo vs. baseline quantity comparison
- Sales uplift % by promotional period
- Business-focused visualizations with a footnote documenting methodology

### 📙 Databricks (Cost & Margin Deep Dive)

Databricks was also used to build an interactive dashboard exploring cost and profitability trends.

This dashboard focused on:

- Sales vs. Cost of Sales over time
- Gross Profit % over time
- Cost of Sales as a % of Sales, by month
- A date-range filter for exploring specific periods

### 📊 Google Looker Studio

Looker Studio was used as another reporting platform to explore the sales analysis through an interactive dashboard environment.

This provided additional experience in:

- Multi-page dashboard layout (trend, seasonality, quantity, promo spotlight)
- Interactive filtering
- Data visualization
- Business reporting and visual storytelling

---

## 🚀 Lovable Interactive Dashboard

The analysis was also transformed into a web-based interactive dashboard using **Lovable**.

The dashboard follows the same visual identity established throughout the project, using a charcoal-and-coral themed design.

### 🔗 Live Dashboard

Since the Lovable dashboard cannot be exported as a PDF, the live interactive version is available for review here:

**[Elastic Edge Analytics | Lovable](https://lovable.dev/projects/a35c4f72-035d-45e5-b28e-691564996027)**

---

## 🎨 Elastic Edge Visual Identity

A consistent design language was maintained throughout the project.

| Purpose | Colour | Hex |
|---|---|---|
| 🟦 Background | Charcoal | `#1F2A44` |
| 🟩 Primary | Teal | `#0E7C7B` |
| ⬜ Secondary | Slate Gray | `#8A93A6` |
| 🟧 Accent | Coral | `#E8734A` |

This colour palette was carried across every dashboard to create a consistent **Elastic Edge** identity.

---

## 🔑 Business Insights

The analysis provides a framework for understanding the key drivers of pricing, promotions, and profitability.

### 🎯 Promotion Performance

Black Friday and New Year promotions are strongly price-elastic — quantity sold rose far more than price fell, confirming these promotions successfully drove volume.

### 📆 Methodology Matters

Quarter-end's elasticity result depends entirely on the baseline method used. A 3-year non-promo average shows almost no price change, while a ±14-day local baseline shows a real, local price dip and a strong quantity lift. This was documented rather than "fixed," since both are analytically valid choices.

### 💰 Profitability

Average gross profit % sits around **-3.81%** overall, confirmed independently in both SQL and Power BI. This isn't evenly spread — margin was negative for most of the dataset's history (late 2013 through mid-2016), then turned and stayed positive in the final months of the dataset.

---

## ✅ Business Recommendations

Based on the analytical framework and findings from this case study, the following strategies could support improved business performance:

**1. 🎯 Continue High-Elasticity Promotions**
Black Friday and New Year promotions clearly drive profitable volume — prioritize these over less effective promotional windows.

**2. 🔍 Re-Evaluate the Quarter-end Promotion**
Its price effect is small and its results are highly sensitive to methodology — investigate whether it's worth running in its current form.

**3. 📉 Investigate the Cost Structure Behind the Negative Margin**
Before running further volume-driving promotions, understand what drove cost of sales to exceed sales revenue for most of the dataset's history.

**4. 📈 Investigate What Changed in Late 2016**
Margin turned positive in the final months of the dataset — understanding why could reveal a repeatable strategy.

**5. 📝 Standardize (or Clearly Document) Elasticity Methodology**
Ensure any future promo analysis states its baseline method explicitly, since it materially changes the conclusion.

---

## 🗓️ Project Planning

Project planning and analytical workflow were mapped out using a themed Gantt chart, covering:

- Planning
- Data Cleaning & SQL Setup (Databricks)
- Excel Analysis & Dashboard
- Dashboard Development (Looker Studio, Power BI, Databricks, Lovable)
- Documentation & GitHub Upload

This tool helped structure the project from the initial data cleaning stage through to final delivery.

---

## 🧩 Skills Demonstrated

This project demonstrates practical experience across the full data analytics lifecycle.

**📊 Data Analytics**
- Data cleaning
- Data transformation
- Exploratory data analysis
- Pricing & elasticity analysis
- Time-based analysis
- Business analysis & storytelling

**💻 SQL**
- Data type conversion
- String & date functions
- Conditional logic (`CASE WHEN`)
- Calculated fields
- CTEs and joins
- Table creation
- Data transformation

**🧱 Databricks**
- Data preparation
- SQL-based transformations
- Analytical dataset creation
- Interactive dashboard building
- Data cleaning workflow

**📗 Excel**
- Pivot tables
- Pivot charts
- Dashboard development

**📘 Power BI**
- Interactive dashboards
- DAX measures
- KPI cards
- Slicers/buttons
- Business intelligence & data visualization

**🎨 Data Visualization**
- Dashboard design
- Visual hierarchy
- Chart selection
- Interactive reporting
- Data storytelling

**📣 Business Communication**
- Business recommendations
- Translating data into business language
- Methodology documentation

**🗂️ Project Planning**
- Gantt chart
- Project workflow planning

---

## 📦 Project Deliverables

The project includes the following key deliverables:

- 📗 Excel Dashboard *(in progress)*
- 📘 Power BI Dashboard
- 📊 Looker Studio Dashboard
- 📙 Databricks Cost & Margin Dashboard
- 🚀 Lovable Interactive Dashboard
- 🧼 Cleaned Dataset
- 💻 SQL Code
- 🗓️ Project Gantt Chart

### 🔗 Live Lovable Dashboard

**[Open the Elastic Edge Interactive Dashboard](https://lovable.dev/projects/a35c4f72-035d-45e5-b28e-691564996027)**

> Note: The Lovable dashboard is provided as a live interactive application because the platform does not provide a PDF export of the dashboard.

---

## 🏆 Project Outcome

The Elastic Edge Sales Case Study demonstrates how raw transactional data can be transformed into meaningful business intelligence through a structured analytics process.

The project brings together:

**SQL + Databricks → Data Preparation → Excel + Power BI + Looker Studio + Databricks → Lovable → Insights → Recommendations**

The key objective was not simply to create dashboards, but to demonstrate the complete process of cleaning the data, understanding the data, finding patterns, communicating insights, and recommending action.

This project demonstrates the ability to work across multiple analytics platforms while maintaining a consistent business objective and visual identity.

---

## 🔮 Future Improvements

Future enhancements could include:

- 🤖 Automating monthly gross profit % reporting
- 📈 Developing predictive sales/demand forecasting
- 🧮 Expanding elasticity analysis to additional products
- 🔗 Connecting cost-driver data to explain the margin recovery in late 2016
- 📊 Standardizing elasticity baseline methodology across all tools
- 🗓️ Automated monthly KPI monitoring
- 🌐 Further enhancing the web-based Lovable analytics application

---

## ✍️ Project Author

**Lerato Legodi**

Data Analytics Portfolio Project
Elastic Edge Sales Case Study — 2026

> From Transactions to Insights
> Turning retail sales data into pricing decisions
