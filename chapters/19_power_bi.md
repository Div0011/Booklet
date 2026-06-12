# 19. Power BI & Data Analysis

## 1. Introduction
### What it is
Power BI is a proprietary business intelligence and data analytics platform developed by Microsoft in 2015. It combines a columnar database engine (VertiPaq), a data transformation tool (Power Query), a metadata relationships schema, and an interactive visualizations canvas to ingest, model, analyze, and present corporate data.

### Why it exists
Modern corporate data is fragmented across various repositories: SQL databases, Excel spreadsheets, Salesforce instances, and cloud log stores. Manually writing custom reporting tools or scripts to join, clean, and visualize this data is slow and error-prone. Power BI exists to provide a centralized semantic modeling layers that can consolidate data, run high-performance calculations over millions of rows in milliseconds, and distribute interactive dashboards securely across an organization.

### Problems it solves
- **Data Integration Silos**: Unifies structured and unstructured data sources into a single, cohesive semantic data model.
- **Reporting Stale Latency**: Automates data updates using secure local or cloud data refresh gateways.
- **Advanced Calculation Limits**: Replaces slow spreadsheet processing with high-performance, complex formulas using the Data Analysis Expressions (DAX) query language.
- **Security Compliance Access**: Restricts row-level visibility (e.g., region-specific sales views) using Row-Level Security (RLS).

### Industry Use Cases
- **Executive Performance Portals**: Real-time sales, revenue, and operation tracking dashboards for C-suite executives.
- **Financial Reconciliation**: Dynamic profit and loss statements supporting date-range drill downs.
- **Supply Chain Analytics**: Inventory turn rates, warehouse capacity maps, and logistics performance analytics.
- **Marketing Automation**: Multi-channel conversion tracking, user acquisition cohorts, and customer lifetime value (LTV) reports.

### Analogy
If Microsoft Excel is like a single workbench where you manually copy, paste, and format data tables, Power BI is an automated assembly line: raw materials (data sources) are ingested, cleaned and stamped by machines (Power Query), stored in standardized bins (VertiPaq), and assembled into final products (visual dashboards) that are delivered automatically to clients.

---

## 2. Core Concepts

### Beginner Concepts
- **Power Query (M Language)**: The ETL (Extract, Transform, Load) engine of Power BI used to connect, clean, pivot, merge, and load data tables into the model.
- **Visuals Canvas**: The drag-and-drop workspace containing charts (bar, line, scatter), slicers, cards, and maps.
- **Relationships**: Linking tables together using keys (e.g. connecting the `CustomerID` in a Sales table to the `ID` in a Customer table).
- **Star Schema**: The recommended modeling layout containing central **Fact Tables** (transactions/metrics) linked to surrounding **Dimension Tables** (attributes/lookup descriptions) in a star shape.

### Intermediate Concepts
- **DAX (Data Analysis Expressions)**: The formula language used to create custom calculations in Power BI, containing statistical, date, and aggregation functions.
- **Calculated Columns vs. Measures**:
  - **Calculated Columns**: Computed row-by-row during data refresh, stored in RAM, and evaluated in a **Row Context**.
  - **Measures**: Computed dynamically at query time based on the active filters, consuming CPU, and evaluated in a **Filter Context**.
- **Filter Context**: The active filters acting on a cell in a visual, defined by row/column headers, page filters, slicers, and cross-filters.
- **Row Context**: The concept of the "current row" during iteration. It exists in calculated columns and iterator functions (like `SUMX`).

### Advanced Concepts
- **VertiPaq Engine**: The in-memory, columnar database engine behind Power BI that compresses and stores data in RAM.
- **Context Transition**: The process of converting a Row Context into a Filter Context. This is triggered exclusively by calling the `CALCULATE` function.
- **Row-Level Security (RLS)**: Setting up data-access roles using DAX filter expressions to restrict data rows based on user authentication profiles.
- **DirectQuery vs. Import Mode**:
  - **Import Mode**: Loads a copy of the data into the in-memory VertiPaq engine (fastest query speeds).
  - **DirectQuery**: Queries the target database directly at runtime (slower, but supports real-time data and large volumes).

---

## 3. Internal Working

### Columnar Databases and VertiPaq Compression
The Power BI VertiPaq engine stores data in columns rather than rows, which is highly efficient for analytical queries:

```text
Row-Oriented Layout (Traditional DB):
[Row 1: ID, Name, Sales] -> [Row 2: ID, Name, Sales] -> [Row 3: ID, Name, Sales]

Column-Oriented Layout (VertiPaq):
[Column ID: 1, 2, 3]
[Column Name: Alice, Bob, Charlie]
[Column Sales: 100, 200, 150]
```

Analytical queries typically aggregate single columns (e.g., summing total sales) rather than reading full rows. Columnar storage allows VertiPaq to scan only the requested column, bypassing all other data.

#### VertiPaq Compression Steps
1. **Value Encoding**: Converts integers into smaller mathematical representation spaces.
2. **Dictionary Encoding**: Replaces text strings with integer index keys, storing the actual strings once in a lookup dictionary.
3. **Run-Length Encoding (RLE)**: Compresses repeating consecutive values in a column by storing the value and its count (e.g., storing `(10, 5x)` instead of `10, 10, 10, 10, 10`).

---

## 4. Important Terminology
- **VertiPaq**: In-memory columnar engine compressing and querying Power BI data.
- **DAX (Data Analysis Expressions)**: Formula language for custom analytics.
- **M Language**: The functional language powering Power Query transformations.
- **Fact Table**: A table containing quantitative measurements or metrics (e.g. sales amount, quantity).
- **Dimension Table**: A table containing descriptive attributes (e.g. customer name, product category).
- **Row Context**: Row-by-row evaluation context.
- **Filter Context**: The active filters acting on a query.
- **RLS (Row-Level Security)**: Restricting data rows based on user authentication.
- **Context Transition**: Conversion of Row Context to Filter Context using `CALCULATE`.
- **DirectQuery**: Direct database connection bypassing VertiPaq memory loads.

---

## 5. Beginner Examples

### Example 1: Data Cleaning Step in Power Query (M Language)
```powerquery
// Clean product names: trim whitespace and capitalize first letter
let
    Source = Odbc.DataSource("dsn=Warehouse", [ConfigFile=""]),
    Products_Table = Source{[Schema="dbo", Item="Products"]}[Data],
    CleanedText = Table.TransformColumns(Products_Table, {{"ProductName", Text.Trim, type text}}),
    UpperText = Table.TransformColumns(CleanedText, {{"ProductName", Text.Upper, type text}})
in
    UpperText
```

### Example 2: Simple DAX Column vs. Measure
```dax
-- Calculated Column: evaluated row-by-row in the table
ProfitColumn = Sales[Revenue] - Sales[Cost]

-- Measure: evaluated dynamically based on active filter contexts
TotalSalesMeasure = SUM(Sales[Revenue])
```

---

## 6. Intermediate Examples

### Example 1: Year-over-Year (YoY) Sales Comparison (DAX)
```dax
-- Measure: Calculate Total Sales
TotalSales = SUM(Sales[Amount])

-- Measure: Calculate Sales for the Same Period Last Year
SalesLY = CALCULATE(
    [TotalSales],
    SAMEPERIODLASTYEAR('Calendar'[Date])
)

-- Measure: Calculate YoY Sales Growth Percentage
SalesYoYGrowth % = 
VAR CurrentSales = [TotalSales]
VAR PriorSales = [SalesLY]
RETURN
    DIVIDE(CurrentSales - PriorSales, PriorSales, 0)
```

### Example 2: Iterator SUMX for Weighted Profit Calculations
```dax
-- SUMX evaluates the expression row-by-row and then sums the results
TotalWeightedProfit = SUMX(
    Sales,
    (Sales[Quantity] * Sales[UnitPrice]) - Sales[CostAmount]
)
```

---

## 7. Advanced Concepts

### Context Transition in DAX Calculated Columns
Context transition converts a Row Context into a Filter Context. When evaluating a calculated column, wrapping an aggregation in `CALCULATE` forces a context transition, filtering the table based on the current row values:

```dax
-- Without CALCULATE: Sums the entire Sales table, returning the total sum on every row
TotalSalesNoTransition = SUM(Sales[Revenue])

-- With CALCULATE: The current Row Context (e.g. CustomerID=12) transitions into a Filter Context.
-- It filters the Sales table for CustomerID=12, calculating the sum for that specific customer only.
TotalCustomerSales = CALCULATE(SUM(Sales[Revenue]))
```

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers look for understanding of evaluation context state engines. They evaluate your ability to design clean star schemas, write optimized DAX, and resolve security filter requirements.

### Red Flags
- Creating many-to-many bidirectional relationships between tables, causing ambiguous path filtering.
- Writing calculated columns for calculations that should be measures, wasting memory.
- Using `CALCULATE` without understanding context transition, leading to incorrect calculations.
- Hardcoding user credentials or embedding sensitive logic in reports instead of using RLS.

### Green Flags
- Modeling data strictly using a clean Star Schema with 1-to-many relationships.
- Using variables (`VAR` / `RETURN`) in DAX to improve readability and cache intermediate results.
- Relying on DAX Studio to analyze query performance and index compression.

### Answers Matrix
| Level | Question: "What is the difference between calculated columns and measures?" |
|---|---|
| **Rejected** | "Calculated columns are for numbers, measures are for text." |
| **Shortlisted** | "Calculated columns are pre-calculated and stored in the table. Measures are calculated dynamically when you look at the chart." |
| **Selected** | "Calculated columns are evaluated during data refresh and stored in-memory, consuming RAM. They operate in a Row Context. Measures are computed at query time dynamically based on the visual's Filter Context, consuming CPU. Measures should be preferred for aggregates." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. Explain the difference between Row Context and Filter Context in DAX.
- **Detailed Answer**: Row Context is the concept of the current row; it exists when you write a calculated column or use an iterator function (like `SUMX`). It allows DAX to scan columns of the active row. Filter Context is the set of filters applied to a visual (slicers, row coordinates, visual filters). It defines which subset of rows from the data model are visible to the calculations.
- **Follow-up Questions**: How do you transition a Row Context into a Filter Context? (Answer: Wrap the expression in the `CALCULATE` function).
- **Interviewer's Expectations**: Distinguish row iteration from filter coordinates.

#### 2. What is a Star Schema, and why is it preferred in Power BI?
- **Detailed Answer**: A Star Schema is a data modeling structure containing a central **Fact Table** (storing metrics like Sales) surrounded by **Dimension Tables** (storing descriptive keys like Customer, Product, Date). It is preferred because it optimizes the VertiPaq engine's dictionary lookups, reduces redundant column values, and ensures predictable, performant relationship filtering.
- **Follow-up Questions**: What is a Snowflake Schema? (Answer: A variation where dimension tables are normalized, branching into sub-dimensions, which increases relationship depth and slows query performance).
- **Interviewer's Expectations**: Highlight Star Schema query speeds over flat tables or normalized Snowflake shapes.

#### 3. How does the VertiPaq engine compress data in Power BI?
- **Detailed Answer**: VertiPaq uses three primary columnar compression methods:
  - **Value Encoding**: Converts integers into smaller mathematical representation spaces.
  - **Dictionary Encoding**: Replaces text strings with numeric index keys.
  - **Run-Length Encoding (RLE)**: Compresses repeating consecutive index values (e.g., storing `(10, 5x)` instead of `10, 10, 10, 10, 10`).
- **Follow-up Questions**: How does column cardinality affect compression? (Answer: Columns with high cardinality (many unique values) compress poorly, consuming more RAM).
- **Interviewer's Expectations**: Detail columnar storage benefits and compression algorithms.

#### 4. Explain the difference between SUM and SUMX in DAX.
- **Detailed Answer**:
  - `SUM` is an aggregation function. It operates directly on a single column within the active Filter Context, summing the values.
  - `SUMX` is an iterator function. It takes a table as its first argument and evaluates an expression row-by-row (Row Context) before summing the evaluated outputs.
- **Follow-up Questions**: Which is faster? (Answer: `SUM` is faster because it operates directly on column storage without row-by-row iteration loops).
- **Interviewer's Expectations**: Contrast aggregation with iteration.

#### 5. What is Row-Level Security (RLS) in Power BI, and how is it implemented?
- **Detailed Answer**: RLS restricts data access at the row level based on the logged-in user. It is implemented by creating security roles in Power BI Desktop and writing DAX filter expressions on tables (e.g. `[Region] = "West"`). At runtime, the user's login principal is checked using `USERPRINCIPALNAME()`, and the matching role filter is applied.
- **Follow-up Questions**: What is the difference between Static and Dynamic RLS? (Answer: Static RLS uses hardcoded values in role rules. Dynamic RLS maps the user login name to a security mapping table in the data model).
- **Interviewer's Expectations**: Show role filter configurations and mention `USERPRINCIPALNAME()`.

#### 6. What is Context Transition, and how does it happen?
- **Detailed Answer**: Context Transition is the process of converting a Row Context into a Filter Context. It is triggered exclusively by wrapping an expression in the `CALCULATE` function. During transition, the values of all columns in the current row are added to the filter context, restricting subsequent evaluations to only the matching records.
- **Follow-up Questions**: Does context transition occur automatically? (Answer: Yes, when calling reference measures inside an iterator, since all measures are implicitly wrapped in `CALCULATE`).
- **Interviewer's Expectations**: Explain row-to-filter conversions and the implicit `CALCULATE` wrapping of measures.

#### 7. Compare Import Mode, DirectQuery, and Dual Mode.
- **Detailed Answer**:
  - **Import Mode**: Loads data into Power BI in-memory VertiPaq engine. Fastest performance, but limited to file size limits and requires scheduled refreshes.
  - **DirectQuery**: Queries the backend database in real time. Slower performance, but supports unlimited data sizes and instant updates.
  - **Dual Mode**: Tables can act as either Import or DirectQuery depending on query contexts, optimizing compound visuals.
- **Follow-up Questions**: What is a Composite Model? (Answer: A model that mixes Import Mode and DirectQuery tables in the same report).
- **Interviewer's Expectations**: Detail performance, storage, and refresh differences.

#### 8. What is the difference between active and inactive relationships?
- **Detailed Answer**: An active relationship is the default path through which filters propagate between two tables. An inactive relationship exists when there are multiple paths between tables (e.g. Sales table with both `OrderDate` and `ShipDate` linked to the Date table). Only one relationship path can be active at a time.
- **Follow-up Questions**: How do you activate an inactive relationship in a measure? (Answer: Wrap the calculation in `CALCULATE` and use the `USERELATIONSHIP` function).
- **Interviewer's Expectations**: Describe filter propagation paths and `USERELATIONSHIP`.

#### 9. What is the difference between the CALCULATE and CALCULATETABLE functions?
- **Detailed Answer**:
  - `CALCULATE` evaluates a scalar expression (like a sum or count) in a modified filter context.
  - `CALCULATETABLE` evaluates a table expression (returning a filtered table) in a modified filter context.
- **Follow-up Questions**: Can `CALCULATETABLE` be nested inside `CALCULATE`? (Answer: Yes, to provide a filtered table context for aggregations).
- **Interviewer's Expectations**: Contrast scalar return types with table return types.

#### 10. Explain what a Power BI Gateway is and differentiate Personal vs Enterprise.
- **Detailed Answer**: A gateway acts as a bridge, securing data transfers between cloud Power BI services and on-premises data sources.
  - **Personal Gateway**: Runs as an application under a single user account on a local computer.
  - **Enterprise Gateway**: Runs as a Windows service, supports multiple users, allows scheduled refreshes, and supports DirectQuery access.
- **Follow-up Questions**: Does the Gateway store data? (Answer: No, it acts purely as a secure network proxy tunnel).
- **Interviewer's Expectations**: Detail security bridges and user access configurations.

#### 11. What is the purpose of the ALL function in DAX?
- **Detailed Answer**: The `ALL` function returns all rows in a table or all values in a column, ignoring any active filter context. It is commonly used as a denominator in percentage-of-total calculations or to clear specific filters inside `CALCULATE`.
- **Follow-up Questions**: What are `ALLEXCEPT` and `ALLSELECTED`? (Answer: `ALLEXCEPT` clears all filters except on specified columns. `ALLSELECTED` respects filters coming from outside the visual while ignoring internal visual grouping filters).
- **Interviewer's Expectations**: Describe how `ALL` manipulates the filter context.

#### 12. Explain how relationships propagate filters in Power BI.
- **Detailed Answer**: Filters propagate from the "one" side of a relationship to the "many" side. If a relationship has single cross-filter direction, filtering a dimension table (the one side) will filter the fact table (the many side), but filtering the fact table will not affect the dimension table.
- **Follow-up Questions**: When should you set cross-filter direction to Both? (Answer: Very rarely, typically only to filter bridging tables, as it can degrade performance and create ambiguous filtering paths).
- **Interviewer's Expectations**: Explain direction paths and warnings regarding bidirectional filtering.

#### 13. What is the difference between calculated tables and standard imported tables?
- **Detailed Answer**: Standard imported tables are loaded from external data sources during refresh. Calculated tables are created using DAX formulas within the model itself, using functions like `UNION` or `FILTER` on existing tables. They are calculated during data refresh and stored in memory.
- **Follow-up Questions**: Can you use calculated tables in DirectQuery mode? (Answer: No, calculated tables are evaluated inside the VertiPaq engine and stored in memory).
- **Interviewer's Expectations**: Detail source differences and runtime behaviors.

### Scenario-Based Questions

#### 14. Implement a DAX measure to calculate Cumulative Year-to-Date (YTD) Sales manually.
- **Detailed Answer**:
  ```dax
  SalesYTD = CALCULATE(
      [TotalSales],
      FILTER(
          ALL('Calendar'),
          'Calendar'[Year] = MAX('Calendar'[Year]) &&
          'Calendar'[Date] <= MAX('Calendar'[Date])
      )
  )
  ```
- **Follow-up Questions**: What built-in DAX function simplifies this? (Answer: `TOTALYTD([TotalSales], 'Calendar'[Date])`).
- **Interviewer's Expectations**: Explain how `ALL` clears dates while `FILTER` restricts the range.

#### 15. Write an M query step to split a consolidated column and remove duplicates.
- **Detailed Answer**:
  ```powerquery
  // Split column by comma delimiter and remove duplicate records
  SplitStep = Table.SplitColumn(Source, "Tags", Splitter.SplitTextByDelimiter(","), {"Tag1", "Tag2"}),
  DistinctStep = Table.Distinct(SplitStep)
  ```
- **Follow-up Questions**: Where are M queries executed? (Answer: In the Power Query editor, during the data loading/refresh phase).
- **Interviewer's Expectations**: Show M query syntax flow and list transformation APIs.

#### 16. You have a DAX query that takes 15 seconds to load. How do you profile and optimize it?
- **Detailed Answer**:
  - Connect **DAX Studio** to the Power BI model.
  - Run the query with Server Timings enabled to see if CPU time is spent in the Formula Engine (FE) or Storage Engine (SE).
  - Optimize the DAX code by reducing the number of iterator functions (like `FILTER` or `SUMX`) over high-cardinality tables.
  - Replace complex filters with simple column checks where possible.
- **Follow-up Questions**: What is the difference between Formula Engine and Storage Engine? (Answer: Storage Engine is multi-threaded and fast (VertiPaq). Formula Engine is single-threaded and handles complex calculations).
- **Interviewer's Expectations**: Mention DAX Studio, FE/SE differences, and iterator reduction.

#### 17. How do you design a database modeling structure to handle many-to-many relationships safely?
- **Detailed Answer**:
  - Do not use direct many-to-many relationship settings, as they cause ambiguous filter directions.
  - Introduce a **Bridge Table** (or Junction Table) between the two target tables.
  - Configure 1-to-many relationships pointing from the target tables to the Bridge Table.
  - Set the filter direction to propagate from the bridge to the facts, maintaining unidirectional paths.
- **Follow-up Questions**: What is a downside of bidirectional relationships? (Answer: They can cause circular reference paths and degrade query performance).
- **Interviewer's Expectations**: Recommend bridge tables to resolve many-to-many relationships.

#### 18. How do you implement dynamic currency conversion in a Power BI sales report?
- **Detailed Answer**:
  - Create a `CurrencyRates` table containing daily exchange rates.
  - Create a disconnected `CurrencySelection` slicer table for the UI.
  - Write a DAX measure that captures the selected currency from the slicer, looks up the corresponding rate from the rate table, and multiplies the base sales measure:
    ```dax
    ConvertedSales = 
    VAR SelectedRate = SELECTEDVALUE(CurrencyRates[Rate], 1)
    RETURN [TotalSales] * SelectedRate
    ```
- **Follow-up Questions**: What happens if multiple currencies are selected in the slicer? (Answer: The fallback parameter in `SELECTEDVALUE` returns 1, or you can use `IF(HASONEVALUE(..))` to force a selection).
- **Interviewer's Expectations**: Use disconnected tables and variable-driven lookups.

### Debugging Questions

#### 19. Debug why a visual is displaying blank values for Time Intelligence measures.
- **Detailed Answer**:
  - Verify if a dedicated **Calendar Table** exists in the data model.
  - Ensure the Calendar Table date column is marked as the official Date Table in Power BI.
  - Verify if there are missing dates in the Calendar Table; it must contain a continuous, unbroken range of dates.
- **Follow-up Questions**: What happens to time intelligence if dates have gaps? (Answer: The DAX time functions fail to compute shifts, returning blank values).
- **Interviewer's Expectations**: Check Calendar continuity and model markings.

#### 20. Debug why dynamic RLS is not working for a user who sees all data rows.
- **Detailed Answer**:
  - Check if the user is assigned to the Workspace as an Admin, Member, or Contributor. Workspace edit permissions override RLS rules; users must be assigned as **Viewer** for RLS to apply.
  - Verify if the DAX rule utilizes `USERPRINCIPALNAME()` and check if the email value matches the security table.
- **Follow-up Questions**: How can you test RLS roles in Power BI Desktop? (Answer: Use the "View as" feature and enter a target email).
- **Interviewer's Expectations**: Distinguish Workspace permissions from RLS viewer constraints.

#### 21. Why is a bidirectional relationship causing circular reference errors in my model?
- **Detailed Answer**: Circular references occur when there are multiple active filtering paths between tables. Setting relationships to bidirectional allows filters to flow both ways, creating loops.
- **Fix**: Change relationships back to Single direction, and activate paths dynamically in measures using `USERELATIONSHIP`.
- **Follow-up Questions**: What tool detects relationship loops? (Answer: The Relationship Model view displays active paths as solid lines and inactive as dotted lines).
- **Interviewer's Expectations**: Spot filter loops and recommend single-direction paths.

#### 22. Why does my custom calculated column crash during data refreshes with an "Out of Memory" error?
- **Detailed Answer**: Calculated columns are computed during data refresh and stored in memory. If the calculated column uses complex iterators (like `FILTER` over millions of rows), it runs out of memory.
- **Fix**: Re-write the logic as a Measure so it is calculated on-demand, or push the transformation upstream into SQL or Power Query.
- **Follow-up Questions**: Which storage mode uses less memory? (Answer: DirectQuery, since it does not load data into RAM).
- **Interviewer's Expectations**: Identify refresh memory constraints.

#### 23. Debug why this measure is returning the total sales instead of the customer-specific sales in a table visual:
```dax
CustomerSales = SUMX(Customer, SUM(Sales[Revenue]))
```
- **Detailed Answer**: The expression `SUM(Sales[Revenue])` is evaluated inside the Row Context of the `Customer` table iterator. However, a Row Context does not filter other tables automatically. Because there is no context transition, the calculation returns the total sales sum for every customer.
- **Fix**: Wrap the expression in `CALCULATE` to trigger context transition:
  ```dax
  CustomerSales = SUMX(Customer, CALCULATE(SUM(Sales[Revenue])))
  ```
- **Follow-up Questions**: What is the implicit equivalent? (Answer: Referencing a pre-written measure: `CustomerSales = SUMX(Customer, [TotalSales])`).
- **Interviewer's Expectations**: Recognize when context transition is required.\n\n#### 24. What is the difference between calculated columns and calculated tables?
- **Detailed Answer**: Calculated columns are evaluated row-by-row and stored as additional fields within an existing table. Calculated tables are created using DAX formulas (like `FILTER` or `UNION`) to generate an entirely new table. Both are evaluated during data refresh and stored in memory.
- **Follow-up Questions**: Can calculated tables use relationships? (Answer: Yes, but only relationships that exist before the table is evaluated).
- **Interviewer's Expectations**: Contrast row fields with entire table generation.

#### 25. Explain the difference between active and inactive relationships in Power BI.
- **Detailed Answer**: An active relationship is the default path through which filters propagate between two tables. An inactive relationship exists when there are multiple paths between tables (e.g. Sales table with both `OrderDate` and `ShipDate` linked to the Date table). Only one relationship path can be active at a time.
- **Follow-up Questions**: How do you activate an inactive relationship in a measure? (Answer: Wrap the calculation in `CALCULATE` and use the `USERELATIONSHIP` function).
- **Interviewer's Expectations**: Describe filter propagation paths and `USERELATIONSHIP`.

#### 26. What is the purpose of the USERELATIONSHIP function in DAX?
- **Detailed Answer**: `USERELATIONSHIP` is a filter modifier function that activates an inactive relationship for the duration of a `CALCULATE` evaluation, overriding the default active relationship path.
- **Follow-up Questions**: Can `USERELATIONSHIP` be used if no relationship exists between the tables? (Answer: No, the relationship must be defined in the model first as an inactive relationship).
- **Interviewer's Expectations**: Explain relationship overrides.

#### 27. How does the VertiPaq engine dictate table sorting for optimization?
- **Detailed Answer**: VertiPaq uses Run-Length Encoding (RLE) to compress data. RLE works best on columns with repeating consecutive values. To optimize, VertiPaq sorts tables internally to cluster repeating values in columns, reducing memory footprint.
- **Follow-up Questions**: Can developers control the internal sorting? (Answer: No, VertiPaq determines the optimal sort order automatically during compression).
- **Interviewer's Expectations**: Connect RLE compression to table sorting.

#### 28. What is the difference between ALL and ALLSELECTED in DAX?
- **Detailed Answer**: `ALL` clears all filters on a table, returning all rows regardless of visuals or slicers. `ALLSELECTED` clears filters coming from inside the current visual (like groupings) but respects filters coming from outside (like page slicers).
- **Follow-up Questions**: Why use `ALLSELECTED` in running totals? (Answer: To ensure the running total respects the user's active slicer filters on the report page).
- **Interviewer's Expectations**: Contrast global filter clearing with local visual clearing.

#### 29. Explain how to implement dynamic row-level security (RLS) in Power BI.
- **Detailed Answer**: Dynamic RLS maps logged-in users to data rows. Create a mapping table linking user email addresses to attributes (like regions). In the security role settings, write a DAX filter: `[UserEmail] = USERPRINCIPALNAME()`. Enable cross-filtering to propagate this filter to the fact table.
- **Follow-up Questions**: What does `USERPRINCIPALNAME()` return in Power BI Desktop? (Answer: The local domain username, but in the Power BI Service, it returns the user's email address).
- **Interviewer's Expectations**: Show mapping configurations and mention `USERPRINCIPALNAME()`.

#### 30. What are variables (VAR / RETURN) and how do they impact performance?
- **Detailed Answer**: Variables (`VAR` keyword) store the result of an expression within a DAX measure. They are evaluated once and cached, improving performance by avoiding duplicate calculations, and making the code easier to read.
- **Follow-up Questions**: Are variables evaluated in the context where they are defined or where they are read? (Answer: They are evaluated in the context where they are defined).
- **Interviewer's Expectations**: Explain caching behaviors and context evaluation.

#### 31. Explain the difference between TREATAS and standard relationships.
- **Detailed Answer**: `TREATAS` applies the result of a table expression as filters to columns of an unrelated table, creating a virtual relationship at query time. Standard relationships are defined statically in the model schema.
- **Follow-up Questions**: When should you use `TREATAS`? (Answer: When linking tables on dynamic keys where static relationships are not possible or create circular reference paths).
- **Interviewer's Expectations**: Contrast virtual filtering with static model relationships.

#### 32. What is the purpose of the Power BI Gateway and how does it route queries?
- **Detailed Answer**: The gateway acts as a secure reverse proxy bridge, transferring data between the cloud Power BI service and local on-premises databases. It decrypts queries, executes them against local data sources, and pushes results back to the cloud.
- **Follow-up Questions**: Does the Gateway store data? (Answer: No, it acts purely as a secure network proxy tunnel).
- **Interviewer's Expectations**: Detail security bridges and user access configurations.

#### 33. Explain the difference between SUM and SUMX evaluation.
- **Detailed Answer**: `SUM` is an aggregation function operating directly on a column within the active Filter Context. `SUMX` is an iterator function that evaluates an expression row-by-row (Row Context) before summing the results.
- **Follow-up Questions**: Which is faster? (Answer: `SUM` is faster because it operates directly on column storage without row-by-row iteration loops).
- **Interviewer's Expectations**: Contrast aggregation with iteration.

#### 34. What is context transition and how is it triggered?
- **Detailed Answer**: Context Transition is the process of converting a Row Context into a Filter Context. It is triggered exclusively by wrapping an expression in the `CALCULATE` function. During transition, the values of all columns in the current row are added to the filter context, restricting subsequent evaluations to only the matching records.
- **Follow-up Questions**: Does context transition occur automatically? (Answer: Yes, when calling reference measures inside an iterator, since all measures are implicitly wrapped in `CALCULATE`).
- **Interviewer's Expectations**: Explain row-to-filter conversions and the implicit `CALCULATE` wrapping of measures.

#### 35. Explain the difference between CROSSFILTER and standard joins.
- **Detailed Answer**: `CROSSFILTER` is a DAX filter modifier used to change the filtering direction (Single, Both, or None) of an existing relationship for the duration of a `CALCULATE` evaluation. Standard joins are static relationships defined in the model.
- **Follow-up Questions**: Why set cross-filtering direction to None? (Answer: To disable a relationship temporarily during specific calculations without deleting it from the model).
- **Interviewer's Expectations**: Explain dynamic filtering direction overrides.

#### 36. What is the difference between calculated measures and implicit measures?
- **Detailed Answer**:
  - **Implicit Measures**: Created automatically when you drag a numeric column directly onto a visual (e.g. Power BI sums the column).
  - **Calculated Measures**: Explicitly written using DAX formulas. They are preferred because they are reusable, support complex filter modifications, and are easier to manage.
- **Follow-up Questions**: Can you use implicit measures in custom DAX formulas? (Answer: No, you can only reference explicit calculated measures).
- **Interviewer's Expectations**: Contrast drag-and-drop aggregates with explicit code formulas.

#### 37. Explain the purpose of HASONEVALUE and SELECTEDVALUE in DAX.
- **Detailed Answer**:
  - `HASONEVALUE`: Returns `TRUE` if the specified column has exactly one unique value in the current filter context.
  - `SELECTEDVALUE`: A shortcut that returns the single value if `HASONEVALUE` is true, otherwise returns a fallback default.
- **Follow-up Questions**: Why use `HASONEVALUE`? (Answer: To prevent visuals from displaying incorrect aggregates on subtotal or total rows).
- **Interviewer's Expectations**: Detail total-row calculations handling.

#### 38. What is incremental refresh and how is it configured?
- **Detailed Answer**: Incremental refresh loads only new or updated data during refreshes, instead of reloading the entire dataset. Configure it by creating `RangeStart` and `RangeEnd` datetime parameters in Power Query, filtering the fact table, and defining retention policies in Desktop.
- **Follow-up Questions**: What is a requirement for data sources to support incremental refresh? (Answer: The data source must support query folding to delegate date filtering to the database).
- **Interviewer's Expectations**: Detail range parameters and query folding requirements.

#### 39. Explain the difference between Star Schema and Snowflake Schema.
- **Detailed Answer**:
  - **Star Schema**: Direct 1-to-many relationships between a central Fact table and Dimension tables. Optimized for VertiPaq.
  - **Snowflake Schema**: Normalized dimension tables branching into sub-dimensions. Increases relationship depth, slowing down query filtering.
- **Follow-up Questions**: Why normalize dimensions in Snowflake? (Answer: To reduce data redundancy, but it is not recommended for Power BI models due to query latency).
- **Interviewer's Expectations**: Contrast query speeds and schema normalization.

#### 40. What is the purpose of KEEPFILTERS in DAX?
- **Detailed Answer**: By default, `CALCULATE` overrides existing filters on a column with new values. Wrapping the filter in `KEEPFILTERS` tells DAX to keep the existing filters and intersect them with the new filter instead of overwriting, preserving visual context.
- **Follow-up Questions**: Give a common use case of `KEEPFILTERS`. (Answer: Showing only specific product sales in a table visual without clearing other row filter contexts).
- **Interviewer's Expectations**: Explain filter intersection behaviors.\n\n\n\n#### 41. What is the difference between calculated columns and measures?
- **Detailed Answer**: Calculated columns are evaluated during refresh, stored in RAM, and operate in a Row Context. Measures are computed dynamically at query time based on active Filter Context, consuming CPU.
- **Follow-up Questions**: Which should be preferred for aggregates? (Answer: Measures, to save memory and ensure responsiveness to visual filters).
- **Interviewer's Expectations**: Differentiate evaluation contexts and memory footprints.

#### 42. Explain calculated tables in Power BI.
- **Detailed Answer**: Tables generated using DAX formulas within the model itself. They are computed during data refresh and stored in memory.
- **Follow-up Questions**: Can they use relationships? (Answer: Yes, but only relationships that exist before the table is evaluated).
- **Interviewer's Expectations**: Contrast calculated tables with standard imported tables.

#### 43. Explain active and inactive relationships in Power BI.
- **Detailed Answer**: Active relationships are the default filter propagation paths. Inactive relationships exist when there are multiple paths between tables.
- **Follow-up Questions**: How do you activate an inactive relationship? (Answer: Wrap the calculation in `CALCULATE` and use `USERELATIONSHIP`).
- **Interviewer's Expectations**: Describe filter propagation paths.

#### 44. What is the purpose of USERELATIONSHIP?
- **Detailed Answer**: `USERELATIONSHIP` is a filter modifier that activates an inactive relationship for the duration of a `CALCULATE` evaluation.
- **Follow-up Questions**: Can it be used if no relationship exists? (Answer: No, the relationship must be defined in the model first).
- **Interviewer's Expectations**: Explain relationship overrides.

#### 45. How does VertiPaq sorting optimize compression?
- **Detailed Answer**: VertiPaq uses Run-Length Encoding (RLE) to compress data. RLE works best on repeating consecutive values, so VertiPaq sorts tables internally to cluster repeating values, reducing memory size.
- **Follow-up Questions**: Can developers control sorting? (Answer: No, VertiPaq determines sort order automatically during compression).
- **Interviewer's Expectations**: Connect RLE compression to table sorting.

#### 46. What is the difference between ALL and ALLSELECTED?
- **Detailed Answer**: `ALL` clears all filters on a table, returning all rows. `ALLSELECTED` clears filters coming from inside the visual (like groupings) but respects filters coming from outside (like page slicers).
- **Follow-up Questions**: Why use `ALLSELECTED` in running totals? (Answer: To ensure the running total respects active page slicers).
- **Interviewer's Expectations**: Contrast global filter clearing with local visual clearing.

#### 47. Explain how to implement dynamic row-level security (RLS).
- **Detailed Answer**: Map logged-in users to data rows. Create a mapping table linking user email addresses to attributes. In the security role settings, write a DAX filter: `[UserEmail] = USERPRINCIPALNAME()`.
- **Follow-up Questions**: What does `USERPRINCIPALNAME()` return in Desktop? (Answer: The local domain username, but in the Service, it returns the user's email address).
- **Interviewer's Expectations**: Show mapping configurations and mention `USERPRINCIPALNAME()`.

#### 48. What are variables (VAR / RETURN) and how do they impact performance?
- **Detailed Answer**: Variables (`VAR` keyword) store the result of an expression within a DAX measure, evaluating once and caching the result to avoid duplicate calculations.
- **Follow-up Questions**: Are variables evaluated in the context where they are defined or read? (Answer: In the context where they are defined).
- **Interviewer's Expectations**: Explain caching behaviors.

#### 49. Explain the difference between TREATAS and standard relationships.
- **Detailed Answer**: `TREATAS` applies the result of a table expression as filters to columns of an unrelated table, creating a virtual relationship at query time. Standard relationships are defined statically.
- **Follow-up Questions**: When should you use `TREATAS`? (Answer: When linking tables on dynamic keys where static relationships are not possible).
- **Interviewer's Expectations**: Contrast virtual filtering with static model relationships.

#### 50. What is the purpose of the Power BI Gateway?
- **Detailed Answer**: The gateway acts as a secure reverse proxy bridge, transferring data between the cloud Power BI service and local on-premises databases, executing queries and returning results.
- **Follow-up Questions**: Does the Gateway store data? (Answer: No, it acts purely as a secure network proxy tunnel).
- **Interviewer's Expectations**: Detail security bridges.

#### 51. Explain the difference between SUM and SUMX.
- **Detailed Answer**: `SUM` is an aggregation function operating directly on a column. `SUMX` is an iterator function that evaluates an expression row-by-row before summing the results.
- **Follow-up Questions**: Which is faster? (Answer: `SUM` is faster because it operates directly on column storage without row-by-row iteration).
- **Interviewer's Expectations**: Contrast aggregation with iteration.

#### 52. What is context transition?
- **Detailed Answer**: Context Transition is the process of converting a Row Context into a Filter Context. It is triggered exclusively by wrapping an expression in the `CALCULATE` function.
- **Follow-up Questions**: Does context transition occur automatically? (Answer: Yes, when calling reference measures inside an iterator, since all measures are implicitly wrapped in `CALCULATE`).
- **Interviewer's Expectations**: Explain row-to-filter conversions.

#### 53. Explain the difference between CROSSFILTER and standard joins.
- **Detailed Answer**: `CROSSFILTER` is a DAX filter modifier used to change the filtering direction of an existing relationship for the duration of a `CALCULATE` evaluation.
- **Follow-up Questions**: Why set cross-filtering to None? (Answer: To disable a relationship temporarily during specific calculations).
- **Interviewer's Expectations**: Explain dynamic filtering direction overrides.

#### 54. What is the difference between calculated measures and implicit measures?
- **Detailed Answer**: Implicit measures are created automatically when you drag a numeric column directly onto a visual. Explicit calculated measures are written using DAX formulas and are preferred for reusability.
- **Follow-up Questions**: Can you use implicit measures in custom DAX formulas? (Answer: No, you can only reference explicit calculated measures).
- **Interviewer's Expectations**: Contrast drag-and-drop aggregates with explicit code.

#### 55. Explain HASONEVALUE and SELECTEDVALUE.
- **Detailed Answer**: `HASONEVALUE` returns `TRUE` if the specified column has exactly one unique value in the current filter context. `SELECTEDVALUE` is a shortcut returning the single value if `HASONEVALUE` is true, otherwise returning a fallback.
- **Follow-up Questions**: Why use `HASONEVALUE`? (Answer: To prevent incorrect aggregates on subtotal or total rows).
- **Interviewer's Expectations**: Detail total-row calculations handling.

#### 56. What is incremental refresh?
- **Detailed Answer**: Incremental refresh loads only new or updated data during refreshes, configured using `RangeStart` and `RangeEnd` datetime parameters in Power Query.
- **Follow-up Questions**: What is a requirement for data sources to support incremental refresh? (Answer: The data source must support query folding).
- **Interviewer's Expectations**: Detail range parameters and query folding.

#### 57. Explain Star Schema vs Snowflake Schema.
- **Detailed Answer**: Star Schema uses direct 1-to-many relationships between a central Fact table and Dimension tables. Snowflake Schema normalizes dimension tables, increasing relationship depth and slowing query performance.
- **Follow-up Questions**: Why normalize dimensions in Snowflake? (Answer: To reduce data redundancy, but it is not recommended for Power BI due to query latency).
- **Interviewer's Expectations**: Contrast query speeds and schema normalization.

#### 58. What is the purpose of KEEPFILTERS?
- **Detailed Answer**: Wrapping a filter in `KEEPFILTERS` tells DAX to keep the existing filters and intersect them with the new filter instead of overwriting, preserving visual context.
- **Follow-up Questions**: Give a common use case. (Answer: Showing only specific product sales in a table visual without clearing other row filter contexts).
- **Interviewer's Expectations**: Explain filter intersection behaviors.

#### 59. Explain VertiPaq compression methods.
- **Detailed Answer**: VertiPaq compresses columnar data using Value Encoding (mathematical maps), Dictionary Encoding (replaces text with integer indices), and Run-Length Encoding (compresses repeating consecutive values).
- **Follow-up Questions**: How does column cardinality affect compression? (Answer: High cardinality columns compress poorly, consuming more memory).
- **Interviewer's Expectations**: Detail the three compression methods.

#### 60. How do relationships propagate filters?
- **Detailed Answer**: Filters propagate from the "one" side of a relationship to the "many" side. If single direction, filtering a dimension table filters the fact table, but not vice versa.
- **Follow-up Questions**: When should you use bidirectional filtering? (Answer: Very rarely, as it can degrade performance and cause circular reference paths).
- **Interviewer's Expectations**: Explain direction paths and warnings.\n\n

#### 61. What is the difference between KEEPFILTERS and standard CALCULATE filter overrides?
- **Detailed Answer**: By default, `CALCULATE` replaces existing filters on a column with any new filters specified in its arguments. `KEEPFILTERS` overrides this behavior. It intersects the new filter with the existing filter instead of replacing it, ensuring that visual filters and measure filters are both respected.
- **Follow-up Questions**: When is `KEEPFILTERS` useful? (Answer: When displaying calculations in a matrix visual, preventing the visual from displaying blank rows for out-of-filter values).
- **Interviewer's Expectations**: Contrast filter replacements with intersection behaviors.

#### 62. Explain the use of EARLIER in row context nesting.
- **Detailed Answer**: `EARLIER` is used in calculated columns to refer to the value of a column in an outer row context during nested iterations. It tells the engine to step back one level of row context. In modern DAX, `EARLIER` is obsolete; variables (`VAR`) should be used to store the outer value before entering the inner loop, which is cleaner and faster.
- **Follow-up Questions**: Why is `EARLIER` obsolete? (Answer: Because using `VAR` captures the value and context cleanly, improving readability and performance).
- **Interviewer's Expectations**: Describe row contexts, nesting loops, and modern `VAR` alternatives.

#### 63. How do you optimize VertiPaq memory footprint by using integer indexing instead of text columns?
- **Detailed Answer**: The VertiPaq engine compresses data using dictionary encoding. Text columns require large dictionaries to map strings to integer keys. High-cardinality text columns (like transaction IDs) consume massive memory. You optimize this by converting text columns into integers or splitting them, and using integer keys for relationships, reducing dictionary size and memory overhead.
- **Follow-up Questions**: What is dictionary size? (Answer: The memory allocated to map actual unique values to VertiPaq's internal token codes).
- **Interviewer's Expectations**: Explain dictionary encoding compression, and identify text dictionary memory overheads.

#### 64. Explain the difference between SUMMARIZE and SUMMARIZECOLUMNS in DAX.
- **Detailed Answer**:
  - `SUMMARIZE`: An older table function that groups data by specified columns. It is prone to performance issues and calculation bugs when adding measures directly inside it.
  - `SUMMARIZECOLUMNS`: The modern, highly optimized grouping function used by Power BI visuals. It supports filter arguments directly and does not suffer from calculation context bugs.
- **Follow-up Questions**: Can you use `SUMMARIZECOLUMNS` in calculated columns? (Answer: No, it is disallowed in calculated columns if it references the current table, risking circular dependencies).
- **Interviewer's Expectations**: Contrast grouping functions and recommend `SUMMARIZECOLUMNS` for query measures.

#### 65. How do you implement dynamic currency conversion using Calculation Groups?
- **Detailed Answer**: Calculation Groups allow you to apply generic calculation logic to existing measures. To handle currency conversion, create a Calculation Group with items for each currency (e.g., USD, EUR). The calculation uses `SELECTEDMEASURE()` multiplied by the exchange rate retrieved from a rate table based on the active selection:
  ```dax
  SELECTEDMEASURE() * SELECTEDVALUE(ExchangeRates[Rate], 1)
  ```
  This dynamically alters the output of any measure placed in a visual based on the selected currency slicer.
- **Follow-up Questions**: What tool is required to create Calculation Groups? (Answer: Tabular Editor).
- **Interviewer's Expectations**: Detail Calculation Group setups, the `SELECTEDMEASURE()` function, and currency joins.

#### 66. What is the difference between CROSSFILTER and standard relationships?
- **Detailed Answer**: Standard relationships have a static cross-filter direction (Single or Both) defined in the model. `CROSSFILTER` is a filter modifier function used within `CALCULATE` to dynamically alter the direction or state (active, inactive, or none) of a relationship for the duration of the query, avoiding model-level ambiguity.
- **Follow-up Questions**: Why avoid setting cross-filter direction to "Both" globally? (Answer: It introduces performance overhead and can cause ambiguous circular paths in complex models).
- **Interviewer's Expectations**: Differentiate static model settings from query-level overrides.

#### 67. Explain the differences between Import, DirectQuery, and Composite models in Power BI.
- **Detailed Answer**:
  - **Import**: Queries all data into memory (VertiPaq engine). Fastest performance but limited by RAM size and requires scheduled refreshes.
  - **DirectQuery**: Data remains in the source database. Power BI sends SQL queries at runtime. Slowest performance but supports real-time data and large datasets.
  - **Composite**: Combines both Import and DirectQuery tables in a single model, balancing performance and storage.
- **Follow-up Questions**: What is dual storage mode? (Answer: A setting that allows a table to behave as Import or DirectQuery depending on the query context).
- **Interviewer's Expectations**: Contrast performance profiles, memory constraints, and query paths.

#### 68. How do you debug visual rendering latency using Power BI Performance Analyzer?
- **Detailed Answer**: Open Performance Analyzer, click Start Recording, and refresh visuals. It breaks latency down into:
  - **DAX Query**: The time Power BI took to execute the DAX calculation.
  - **Visual Display**: The time taken by the browser to render the visual elements.
  - **Other**: Network and queue wait times.
  If DAX Query is slow, copy the query and analyze it in DAX Studio to check the query plan and formula engine calls.
- **Follow-up Questions**: What is the difference between the Formula Engine (FE) and Storage Engine (SE)? (Answer: FE is single-threaded and handles complex logic. SE is multi-threaded and fetches raw data).
- **Interviewer's Expectations**: Identify performance metrics and describe DAX Studio debugging paths.

#### 69. Explain the implementation of incrementally refreshed datasets and partition limits.
- **Detailed Answer**: Incremental refresh defines parameters `RangeStart` and `RangeEnd` to partition tables in the source database. The Power BI service creates historical partitions that are locked, and only refreshes the active partition representing recent data. This reduces refresh times and source database queries.
- **Follow-up Questions**: Can you use incremental refresh with data sources that do not support query folding? (Answer: Yes, but the entire dataset must still be pulled into Power BI, eliminating performance gains).
- **Interviewer's Expectations**: Explain range parameters, partition splits, and query folding requirements.

#### 70. What is a semi-additive measure and how do you implement it in DAX?
- **Detailed Answer**: A semi-additive measure is a metric that is additive across some dimensions but not others. For example, inventory stock level is additive across stores (adding stock of Store A and B) but not across time (you do not add stock levels of Monday and Tuesday). Implement it using `LASTDATE` or `LASTNONBLANK`:
  ```dax
  CALCULATE(SUM(Inventory[Stock]), LASTDATE(Calendar[Date]))
  ```
- **Follow-up Questions**: Why use `LASTNONBLANK`? (Answer: To handle cases where the last day of a period (e.g. Sunday) has no record, returning the last active day's stock).
- **Interviewer's Expectations**: Explain dimension additive variations and show DAX calculations.

#### 71. Detail how to handle many-to-many relationships using bridge tables vs. cross-filter directions.
- **Detailed Answer**: Many-to-many relationships occur when multiple rows in Table A relate to multiple rows in Table B. Handling this directly in the relationship settings can lead to unexpected results. The best practice is to resolve it using a Bridge Table that contains unique values of the keys, creating two one-to-many relationships. Alternatively, you can use a direct many-to-many relationship with a single cross-filter direction, keeping the filter propagation clear.
- **Follow-up Questions**: What is a danger of bidirectional filtering in many-to-many relationships? (Answer: It can cause filters to propagate unexpectedly, returning incorrect results).
- **Interviewer's Expectations**: Contrast bridge tables with direct configurations and explain filter directions.

#### 72. Explain the use of SELECTEDVALUE and its fallback arguments.
- **Detailed Answer**: `SELECTEDVALUE(Column, [AlternateResult])` returns the value of a column if it has been filtered down to exactly one unique value in the current context. If there are multiple values or no values, it returns the `AlternateResult` (or `BLANK()` if omitted). It is syntactic sugar for `IF(HASONEVALUE(Column), VALUES(Column), AlternateResult)`.
- **Follow-up Questions**: Why is it safer than `VALUES()`? (Answer: Because if `VALUES()` returns multiple rows, it throws an error in single-value contexts).
- **Interviewer's Expectations**: Detail single-value filters and contrast with `VALUES` errors.

#### 73. How does ALLEXCEPT differ from ALL and VALUES in DAX filter manipulation?
- **Detailed Answer**:
  - `ALL`: Removes all filters on the specified table or columns.
  - `ALLEXCEPT`: Removes all filters on a table *except* for filters applied to the specified columns.
  - `VALUES`: Returns a list of unique values currently active in the filter context.
  `ALLEXCEPT` is used to preserve specific filters while clearing others, such as calculating percentages of totals.
- **Follow-up Questions**: What is the difference between `ALLEXCEPT` and `ALL` combined with `VALUES`? (Answer: `ALLEXCEPT` maintains the active filters on the columns; `ALL` followed by `VALUES` clears the filters and re-applies only the values, which can alter context transition).
- **Interviewer's Expectations**: Contrast filter clearing scopes.

#### 74. Explain how Power Query's query folding translates M queries to SQL.
- **Detailed Answer**: Query folding is the process where Power Query translates M steps (filtering, sorting, merging) into a single SQL statement that is executed directly on the source database server. This pushes calculations to the database. If a step cannot be folded (e.g., applying a custom M function), folding stops, and all subsequent steps must be executed in Power BI memory.
- **Follow-up Questions**: How do you identify if a step is folded? (Answer: Right-click the step in Power Query; if "View Native Query" is active, that step (and prior steps) folded).
- **Interviewer's Expectations**: Explain database pushdown benefits and identify steps that break folding.

#### 75. What is the difference between standard Row-Level Security (RLS) and Object-Level Security (OLS)?
- **Detailed Answer**:
  - **Row-Level Security (RLS)**: Restricts access to data *rows* based on user roles (e.g., a manager only sees sales data for their region). The table structure remains visible.
  - **Object-Level Security (OLS)**: Restricts access to entire *tables or columns*. If a user without permissions queries a visual containing an OLS-secured column, the visual returns an error because the column is completely hidden.
- **Follow-up Questions**: How is OLS configured? (Answer: Using Tabular Editor to set column and table permissions to None).
- **Interviewer's Expectations**: Differentiate row filtering from schema-level column hiding.

#### 76. What is the difference between TREATAS and standard relationships?
- **Detailed Answer**: Standard relationships are defined statically in the data model. `TREATAS` applies the results of a table expression as filters to columns of another table, creating a virtual, dynamic relationship at query time. It is faster than using `INTERSECT` or `FILTER` and is used when static relationships cannot be defined due to granularity mismatches or circular paths.
- **Follow-up Questions**: Write a basic `TREATAS` expression. (Answer: `CALCULATE(SUM(Sales[Amount]), TREATAS(ValuesTable, Sales[ProductKey]))`).
- **Interviewer's Expectations**: Explain virtual relationship mappings.

#### 77. Explain how the VertiPaq engine utilizes value encoding.
- **Detailed Answer**: Value encoding is a compression technique used by VertiPaq for numeric columns. It reduces the number of bits needed to store values by subtracting a constant or dividing them. For example, if a column contains values between 10,000 and 10,050, VertiPaq stores the values as offsets from 10,000 (0 to 50), reducing memory footprint.
- **Follow-up Questions**: Can value encoding be used on text? (Answer: No, value encoding is strictly for numeric types; text uses hash/dictionary encoding).
- **Interviewer's Expectations**: Explain numeric offset transformations.

#### 78. Explain the difference between Row-Level Security (RLS) and Object-Level Security (OLS) in Power BI.
- **Detailed Answer**: RLS filters rows of data within a table, but the table structure and column headers remain visible to the unauthorized user (they just see empty visuals or restricted rows). OLS restricts access to the entire table or column schema. If a user queries an OLS-secured column, the query fails completely and returns a visual error, hiding the schema entirely.
- **Follow-up Questions**: How do you test RLS/OLS? (Answer: In the Power BI Service using the "Test as role" feature, or in Desktop using "View as").
- **Interviewer's Expectations**: Differentiate row filtering from schema-level hiding.

#### 79. Explain how calculation groups interact with format strings.
- **Detailed Answer**: Calculation Groups can override both the calculation expression and the format string of a measure. In Tabular Editor, you can define a dynamic format string expression (e.g. formatting as currency if currency slicer is selected, or percentage if ratio is selected) using `SELECTEDMEASUREFORMATSTRING()`.
- **Follow-up Questions**: Can you hardcode the format string? (Answer: Yes, by setting the format string property to a static string like `"$#,##0"`).
- **Interviewer's Expectations**: Explain dynamic format overrides.

#### 80. What are the best practices for structuring date tables in Power BI?
- **Detailed Answer**: Date tables (Calendar tables) are required for time intelligence functions. Best practices include:
  - The table must contain a column of type Date containing unique, contiguous dates with no gaps covering the entire range of the dataset.
  - Mark the table as a Date Table in Power BI.
  - Do not use the automatic Date/Time settings in Power BI Desktop to save memory.
- **Follow-up Questions**: Why mark a table as a Date Table? (Answer: It disables the auto-generated date tables under the hood, saving memory, and ensures time intelligence functions calculate correctly over custom relationships).
- **Interviewer's Expectations**: Detail requirements for time intelligence correctness and memory optimization.

#### 81. Explain the use of the PATH function for parent-child hierarchies.
- **Detailed Answer**: The `PATH` function in DAX parses parent-child hierarchies (like employee-manager structures) and returns a delimited string showing the full path from the root node to the current row (e.g., `1|4|12`). This path can then be queried using `PATHITEM` or `PATHCONTAINS` to flatten the hierarchy into separate columns for visual filtering.
- **Follow-up Questions**: What parameters does `PATH` require? (Answer: The child ID column and the parent ID column).
- **Interviewer's Expectations**: Show how to flatten recursive hierarchies.

#### 82. What is the difference between active and passive relationships in Power BI?
- **Detailed Answer**: An active relationship is the default path used by the VertiPaq engine to propagate filters between tables. A passive (inactive) relationship exists when there are multiple alternative paths between tables. Passive relationships are ignored by default in queries but can be activated dynamically using the `USERELATIONSHIP` modifier inside a `CALCULATE` expression.
- **Follow-up Questions**: Can you have multiple active relationships between two tables? (Answer: No, only one relationship can be active between two specific tables at a time).
- **Interviewer's Expectations**: Differentiate default filter propagation paths from dynamic query-level activations.

#### 83. Explain the use of the COALESCE function in DAX.
- **Detailed Answer**: `COALESCE` evaluates a list of expressions in order and returns the value of the first expression that does not evaluate to `BLANK()`. If all expressions are blank, it returns `BLANK()`. It is equivalent to `IF(NOT ISBLANK(E1), E1, IF(NOT ISBLANK(E2), E2, ...))`, but runs faster and is easier to read.
- **Follow-up Questions**: How is `COALESCE` useful in formatting blank metrics? (Answer: By appending a default value: `COALESCE([Total Sales], 0)` returns `0` instead of a blank visual field).
- **Interviewer's Expectations**: Detail fallback evaluations and blank replacements.

#### 84. What is a star schema and why is it preferred over a snowflake schema in Power BI?
- **Detailed Answer**: A star schema structures data into centralized fact tables linked directly to denormalized dimension tables. A snowflake schema further normalizes dimensions into sub-dimensions (e.g., Category linked to Subcategory linked to Product). Star schemas are preferred in Power BI because they minimize relationship hops, reducing VertiPaq query traversal times and simplifying DAX logic.
- **Follow-up Questions**: How does a snowflake schema affect performance? (Answer: It increases the number of joins the storage engine must perform, leading to slower query times).
- **Interviewer's Expectations**: Contrast denormalized star structures with normalized snowflake setups.

#### 85. Explain how to manage large datasets using pre-aggregations.
- **Detailed Answer**: Pre-aggregations involve creating aggregated summary tables at a higher grain (e.g. Sales by Month instead of individual transactions). In Power BI, you load the aggregated table into memory (Import mode) and keep the detail table in the source database (DirectQuery mode). Using Power BI's aggregation settings, you map visual fields to the aggregated table; the engine automatically routes queries to the fast in-memory table if the visual only requests aggregated summaries, falling back to DirectQuery only for granular details.
- **Follow-up Questions**: What is a dual storage mode table? (Answer: A dimension table that can be queried in both Import and DirectQuery modes to match the query path).
- **Interviewer's Expectations**: Detail composite configurations and automatic query routing.

#### 86. What is the difference between USERPRINCIPALNAME and USERNAME in DAX?
- **Detailed Answer**: Both functions return the identity of the currently logged-in user, but they return different formats. `USERNAME()` returns the user's domain and logon name in the format `DOMAIN\user` (especially in on-premises or local Desktop environments). `USERPRINCIPALNAME()` returns the user's User Principal Name (UPN) in email format (e.g., `user@domain.com`). In the Power BI Service, `USERPRINCIPALNAME()` is preferred for dynamic Row-Level Security (RLS) to match Azure AD email identities.
- **Follow-up Questions**: What does `USERPRINCIPALNAME()` return in Power BI Desktop? (Answer: The local computer's login domain username, matching `USERNAME()`).
- **Interviewer's Expectations**: Differentiate local logon structures from cloud UPN email formats.

#### 87. Explain how the CALCULATE function performs context transition.
- **Detailed Answer**: Context transition is the process where a row context is converted into an equivalent filter context. This transition occurs automatically whenever a measure is evaluated inside a row context (like inside an iterator function like `SUMX` or inside a calculated column). Wrapping an expression in `CALCULATE` forces this transition, converting all active row values into filters that restrict the calculation.
- **Follow-up Questions**: What is a performance risk of context transition in calculated columns? (Answer: Running it on large tables transitions every row, causing high memory and slow JIT executions).
- **Interviewer's Expectations**: Explain the conversion of row variables into filter sets.

#### 88. What is the DAX Query Plan and how do you analyze it?
- **Detailed Answer**: The DAX Query Plan is the execution tree generated by the formula engine to satisfy a DAX query. It consists of two layers:
  - **Logical Plan**: The initial representation of the query structure.
  - **Physical Plan**: The actual execution steps, detailing which queries are sent to the storage engine (VertiPaq) and how the formula engine merges results.
  Analyze it using DAX Studio by enabling the Query Plan trace, checking for callback loops or large data transfers between the engines.
- **Follow-up Questions**: What is a callback loop? (Answer: A performance bottleneck where the storage engine must call the formula engine repeatedly during a scan).
- **Interviewer's Expectations**: Describe the differences between logical and physical plans.

#### 89. Explain the use of the HASONEVALUE function in DAX.
- **Detailed Answer**: `HASONEVALUE(Column)` returns `TRUE` when the specified column has been filtered down to exactly one unique value in the current context. It is commonly used to prevent totals or sub-totals from displaying calculations that only make sense for individual rows, or to write custom conditional formatting rules.
- **Follow-up Questions**: How does it differ from `HASONEFILTER`? (Answer: `HASONEFILTER` returns true if there is a direct filter on the column, even if it has multiple values; `HASONEVALUE` returns true if only one value exists, regardless of how it was filtered).
- **Interviewer's Expectations**: Explain filter context boundaries and single-value validation.

#### 90. Explain how to implement a relative date filter or rolling time window using DAX.
- **Detailed Answer**: A rolling time window (e.g. last 12 months) is calculated by modifying the filter context over the Date table. Use `DATESINPERIOD` inside `CALCULATE`, specifying the date column, the end date (usually `MAX(Calendar[Date])`), the number of intervals, and the interval type:
  ```dax
  Rolling12Months = CALCULATE(SUM(Sales[Amount]), DATESINPERIOD(Calendar[Date], MAX(Calendar[Date]), -12, MONTH))
  ```
  This creates a continuous range of dates representing the last 12 months from the active date.
- **Follow-up Questions**: Why use `MAX` instead of `TODAY()`? (Answer: To allow the visual to calculate rolling totals historically based on the selected period rather than fixing it to the current date).
- **Interviewer's Expectations**: Show how to manipulate filter contexts using time intelligence functions.

#### 91. What is the difference between TREATAS and TREATAS with VALUES in DAX?
- **Detailed Answer**: `TREATAS` accepts a table expression and maps its columns to other tables virtually. When using `TREATAS(VALUES(Table1[Key]), Table2[Key])`, it takes only the unique active values of `Key` in `Table1` and applies them as a filter to `Table2`. If `VALUES` is omitted and a full table is passed, `TREATAS` attempts to map all columns, which can fail if columns do not align.
- **Follow-up Questions**: When does mapping multiple columns fail? (Answer: If the column count or data types do not match the target table columns).
- **Interviewer's Expectations**: Detail column mapping structures and filter constraints.

#### 90. Explain how to implement a relative date filter or rolling time window using DAX.
- **Detailed Answer**: A rolling time window (e.g. last 12 months) is calculated by modifying the filter context over the Date table. Use `DATESINPERIOD` inside `CALCULATE`, specifying the date column, the end date (usually `MAX(Calendar[Date])`), the number of intervals, and the interval type:
  ```dax
  Rolling12Months = CALCULATE(SUM(Sales[Amount]), DATESINPERIOD(Calendar[Date], MAX(Calendar[Date]), -12, MONTH))
  ```
  This creates a continuous range of dates representing the last 12 months from the active date.
- **Follow-up Questions**: Why use `MAX` instead of `TODAY()`? (Answer: To allow the visual to calculate rolling totals historically based on the selected period rather than fixing it to the current date).
- **Interviewer's Expectations**: Show how to manipulate filter contexts using time intelligence functions.

#### 91. What is the difference between TREATAS and TREATAS with VALUES in DAX?
- **Detailed Answer**: `TREATAS` accepts a table expression and maps its columns to other tables virtually. When using `TREATAS(VALUES(Table1[Key]), Table2[Key])`, it takes only the unique active values of `Key` in `Table1` and applies them as a filter to `Table2`. If `VALUES` is omitted and a full table is passed, `TREATAS` attempts to map all columns, which can fail if columns do not align.
- **Follow-up Questions**: When does mapping multiple columns fail? (Answer: If the column count or data types do not match the target table columns).
- **Interviewer's Expectations**: Detail column mapping structures and filter constraints.

---

## 10. Common Mistakes
- **Bidirectional Loops**: Creating bidirectional relationships unnecessarily.
- **High Cardinality Columns**: Importing raw timestamps or unique keys, ruining column compression.
- **Calculated Columns abuse**: Using calculated columns for calculations that should be measures.
- **Neglecting Star Schema**: Flattening all source tables into a single wide table.
- **Incorrect Context Transition**: Writing calculated columns with `SUM` instead of `CALCULATE(SUM())`.

---

## 11. Comparison Section: Power BI vs Tableau vs Excel

| Feature | Power BI | Tableau | Microsoft Excel |
|---|---|---|---|
| **Primary Engine** | VertiPaq Columnar DB | Hyper Data Engine | Grid-Based Row Calc Engine |
| **Formula Language** | DAX / M Language | Tableau Calculations | Excel Formulas / VBA |
| **Data Capacity** | Gigabytes (Premium) | Gigabytes | 1,048,576 rows max |
| **Deployment Model** | Cloud Workspaces | Tableau Server / Online | Local Files / OneDrive |
| **Row-Level Security** | Built-in out of the box | Built-in | None (manual workarounds) |

---

## 12. Practical Project Ideas
- **Beginner**: A sales performance dashboard with basic filters, cards, and date slicers.
- **Intermediate**: A financial P&L report utilizing complex calendar tables, custom DAX metrics, and monthly growth calculations.
- **Advanced**: An HR analytics dashboard implementing dynamic Row-Level Security, Incremental Refresh, and a hybrid DirectQuery database connection.

---

## 13. Internship Preparation Notes
- **Focus Areas**: Star Schema modeling, basic visual interactions, writing simple DAX measures (`SUM`, `AVERAGE`), and Power Query merges.
- **Key Concepts**: Row vs Filter context, and calculated columns vs measures.
- **Practical Check**: Clean an Excel dataset in Power Query, load it, and build a Sales-by-Category chart.

---

## 14. Cheat Sheet
- **Filter Context modifier**: `CALCULATE([Measure], Table[Column] = "Filter")`
- **Prior Year calculation**: `CALCULATE([Measure], SAMEPERIODLASTYEAR('Date'[Date]))`
- **Dynamic User Principal**: `USERPRINCIPALNAME()`
- **Safe division**: `DIVIDE(Numerator, Denominator, 0)`

---

## 15. One-Day Revision Guide
- [ ] Differentiate Row Context vs Filter Context.
- [ ] Differentiate Calculated Column vs Measure.
- [ ] Explain how VertiPaq columnar compression operates.
- [ ] Create a YoY sales growth measure.
- [ ] Diagram a Star Schema model.
- [ ] Explain how dynamic RLS routes user access.
- [ ] Compare Power BI and Excel capabilities.
