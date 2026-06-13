# 12. Pandas (Data Analysis and Manipulation)

## 1. Introduction

### What it is
Pandas is a Python library for data manipulation and analysis built on top of NumPy. Its core data structures—**Series** (1D) and **DataFrame** (2D)—provide labeled axes, heterogeneous dtypes, and SQL-like operations (groupby, join, pivot) for tabular data.

### Why it exists
NumPy excels at homogeneous numerical arrays; Pandas adds labels, missing data handling (NaN), and operations optimized for tabular data (groupby, merge, time series). Pandas bridges NumPy and statistical/ML libraries; essential for data cleaning and exploratory analysis.

### Problems it solves
- **Heterogeneous Data**: Mix integers, floats, strings in one table.
- **Labeled Axes**: Named columns and rows (not just integer positions).
- **Missing Data**: Native handling of NaN/None values.
- **Alignment**: Automatic alignment on join/merge; less error-prone than manual indexing.
- **Groupby Operations**: SQL-like GROUP BY without database.
- **Time Series**: DatetimeIndex for resampling, rolling windows, lag/lead.

### Industry Use Cases
- **Data Cleaning**: Remove duplicates, handle missing values, type conversions.
- **Exploratory Analysis**: Describe statistics, value counts, cross-tabulation.
- **Feature Engineering**: Groupby aggregations, rolling windows, one-hot encoding.
- **Financial Analysis**: Time-series resampling, moving averages, correlation.
- **Reporting**: Pivot tables, summary statistics by category.

### Analogy
Pandas DataFrames are like Excel spreadsheets with superpowers: you can query, filter, and aggregate data programmatically without manual cell formulas. Series are labeled lists; DataFrames are labeled tables.

---

## 2. Core Concepts

### Series and DataFrames
```python
import pandas as pd

# Series: 1D labeled array
s = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
print(s['a'])  # 1

# DataFrame: 2D labeled table
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [30, 25, 35],
    'salary': [100000, 80000, 90000]
})

df['age']  # Series
df.loc[0]  # First row
```

### Index and MultiIndex
Flexible labeling beyond integer positions.

```python
# Set custom index
df = df.set_index('name')

# MultiIndex (hierarchical)
idx = pd.MultiIndex.from_tuples([('A', 1), ('A', 2), ('B', 1)])
df_multi = pd.DataFrame(data, index=idx)
df_multi.loc['A']  # All rows with 'A' in level 0
```

### Groupby Operations
Split-apply-combine paradigm.

```python
# Group by column; aggregate
grouped = df.groupby('department')['salary'].agg(['mean', 'sum', 'count'])

# Multiple aggregations
agg_dict = {'salary': ['mean', 'min', 'max'], 'age': 'mean'}
df.groupby('department').agg(agg_dict)

# Transform (returns same shape)
df['salary_rank'] = df.groupby('department')['salary'].rank()
```

### Join and Merge
Combine datasets.

```python
# Inner join (intersection)
merged = pd.merge(df1, df2, on='id', how='inner')

# Left join (keep all from left)
merged = pd.merge(df1, df2, on='id', how='left')

# Concatenate (combine rows/columns)
combined = pd.concat([df1, df2], axis=0)  # Rows
combined = pd.concat([df1, df2], axis=1)  # Columns
```

### Missing Data Handling
```python
df.isna()  # Boolean mask
df.dropna()  # Remove rows with NaN
df.fillna(0)  # Fill with value
df.fillna(method='ffill')  # Forward fill
df.interpolate()  # Linear interpolation
```

### Time Series and DatetimeIndex
```python
dates = pd.date_range('2024-01-01', periods=365, freq='D')
ts = pd.Series(range(365), index=dates)

# Resample (e.g., daily → monthly)
monthly = ts.resample('M').sum()

# Rolling window
ma30 = ts.rolling(window=30).mean()

# Lag/Lead
ts.shift(1)  # Previous value
```

---

## 3. Internal Working

### Storage Model
```
DataFrame
├─ Index (labels for rows)
├─ Columns (labels for columns)
└─ BlockManager (storage)
    ├─ Block 1 (float64 columns)
    ├─ Block 2 (int64 columns)
    └─ Block 3 (object columns)
```

Homogeneous blocks improve performance vs per-column storage.

### Groupby Pipeline
```
Input DataFrame
  ↓
Grouping (hash table of group → rows)
  ↓
Apply function to each group
  ↓
Combine results
  ↓
Output (reduced dimensionality)
```

### Merge Strategy
```
Left df                Right df
  ↓                      ↓
Hash on key          Hash on key
  ↓                      ↓
Match rows (hash join)
  ↓
Output (merged, aligned)
```

---

## 4. Important Terminology

| Term | Definition |
|------|-----------|
| **Series** | 1D labeled array (column from DataFrame) |
| **DataFrame** | 2D table with labeled rows and columns |
| **Index** | Row labels (can be MultiIndex) |
| **Columns** | Column names/labels |
| **Groupby** | Split-apply-combine operation |
| **Aggregation** | Reduce group to single value (sum, mean) |
| **Transform** | Return same shape after function |
| **Merge** | SQL-like join on key |
| **Concat** | Combine rows or columns |
| **Resample** | Change time-series frequency |
| **Rolling** | Compute over sliding window |
| **Pivot** | Reshape data (wide vs long format) |

---

## 5. Beginner Examples

### Example 1: Create and Inspect DataFrame
```python
import pandas as pd

df = pd.read_csv('data.csv')

# Inspect
print(df.head())
print(df.info())
print(df.describe())

# Access
print(df.columns)
print(df.dtypes)
print(df['column_name'])
```

### Example 2: Filtering and Selection
```python
# Boolean indexing
df[df['age'] > 30]

# Multiple conditions
df[(df['age'] > 30) & (df['salary'] > 80000)]

# isin for membership
df[df['department'].isin(['Engineering', 'Sales'])]

# loc (label-based)
df.loc[0]  # First row
df.loc[:, ['name', 'age']]  # Columns
```

### Example 3: Handling Missing Data
```python
df.isna().sum()  # Count missing per column

df.dropna()  # Remove rows with any NaN
df.dropna(thresh=3)  # Keep rows with at least 3 non-null

df.fillna(df.mean())  # Fill with column mean
df.fillna(method='ffill')  # Forward fill
```

### Example 4: Simple Groupby Aggregation
```python
df.groupby('department')['salary'].mean()

df.groupby('department').size()  # Count per group

df.groupby(['department', 'year'])['salary'].sum()
```

### Example 5: Basic Merge
```python
df1 = pd.DataFrame({'id': [1, 2, 3], 'name': ['A', 'B', 'C']})
df2 = pd.DataFrame({'id': [1, 2, 3], 'salary': [100, 200, 300]})

merged = pd.merge(df1, df2, on='id')
```

---

## 6. Intermediate Examples

### Example 1: Complex Groupby with Multiple Aggregations
```python
# Group by multiple columns; multiple agg functions
result = df.groupby(['department', 'year']).agg({
    'salary': ['mean', 'min', 'max', 'std'],
    'employee_id': 'count',
    'bonus': 'sum'
}).round(2)

# Flatten column names
result.columns = ['_'.join(col) for col in result.columns]
```

### Example 2: Rolling Window and Time Series
```python
# Daily stock prices → moving average
ts = pd.Series(prices, index=dates)

ma_30 = ts.rolling(window=30).mean()
ma_50 = ts.rolling(window=50).mean()

# Resample to monthly
monthly_prices = ts.resample('M').agg(['open', 'high', 'low', 'close'])
```

### Example 3: Pivot Tables
```python
# Reshape data: long → wide format
pivot = df.pivot_table(
    values='sales',
    index='region',
    columns='product',
    aggfunc='sum',
    fill_value=0
)
# Rows: regions, Columns: products, Values: total sales
```

### Example 4: Merge with Join Types
```python
# Left join (keep all from left; fill missing with NaN)
result = pd.merge(df1, df2, on='id', how='left')

# Outer join (union; fill missing)
result = pd.merge(df1, df2, on='id', how='outer')

# On different columns
result = pd.merge(df1, df2, left_on='user_id', right_on='customer_id')
```

### Example 5: String Operations
```python
# String methods on Series
df['name'].str.lower()
df['email'].str.contains('@gmail')
df['phone'].str.replace('-', '')

# Extract parts
df['name'].str.split(' ').str[0]  # First name
```

### Example 6: Custom Aggregations & Query Optimization (eval/query)
Performing complex aggregations using custom functions and optimizing intermediate column math with `pd.eval` or `df.query`.

```python
# Custom aggregate functions
def range_range(x):
    return x.max() - x.min()

agg_df = df.groupby('department').agg(
    total_salary=('salary', 'sum'),
    salary_range=('salary', range_range),
    avg_age=('age', 'mean')
)

# Optimization using query() and eval()
# Fast selection and calculations without creating large intermediate DataFrames in memory
high_sal_eng = df.query("department == 'Engineering' and salary > 100000")

# pd.eval executes string expressions faster on large DataFrames using NumExpr under the hood
adjusted_salary = pd.eval("df.salary * 1.10 + df.bonus", target=df)
```

### Example 7: Memory Optimization & Downcasting
Drastically reducing memory footprint for large datasets by downcasting numeric types and converting string columns to categories.

```python
import numpy as np

# Mock large dataframe
np.random.seed(42)
n_rows = 1_000_000
large_df = pd.DataFrame({
    'id': np.arange(n_rows),
    'age': np.random.randint(18, 90, size=n_rows),
    'salary': np.random.randint(30000, 200000, size=n_rows).astype(float),
    'city': np.random.choice(['New York', 'London', 'Paris', 'Tokyo'], size=n_rows)
})

print("Original Memory Usage:")
print(large_df.memory_usage(deep=True).sum() / (1024**2), "MB")  # ~56 MB

# 1. Downcast integers (int64 -> int8/int16/int32)
large_df['id'] = pd.to_numeric(large_df['id'], downcast='integer')      # int32
large_df['age'] = pd.to_numeric(large_df['age'], downcast='integer')    # int8

# 2. Downcast floats (float64 -> float32)
large_df['salary'] = pd.to_numeric(large_df['salary'], downcast='float') # float32

# 3. Convert low-cardinality string columns to 'category'
large_df['city'] = large_df['city'].astype('category')

print("Optimized Memory Usage:")
print(large_df.memory_usage(deep=True).sum() / (1024**2), "MB")  # ~9.5 MB (83% reduction!)
```

---

## 7. Advanced Examples

### Example 1: Custom Groupby Functions
```python
def custom_agg(group):
    return {
        'median_salary': group['salary'].median(),
        'salary_range': group['salary'].max() - group['salary'].min(),
        'outliers': sum(group['salary'] > group['salary'].quantile(0.95))
    }

result = df.groupby('department').apply(custom_agg).unstack()
```

### Example 2: Multi-Level Indexing (MultiIndex)
```python
# Create MultiIndex
idx = pd.MultiIndex.from_product([['A', 'B'], [1, 2, 3]])
df_multi = pd.DataFrame(data, index=idx, columns=['value'])

# Query MultiIndex
df_multi.loc['A']  # All 'A' entries
df_multi.loc[('A', 1)]  # Specific level 0 and 1
df_multi.xs('A', level=0)  # Cross-section
```

### Example 3: Category Data and Memory Optimization
```python
# Use category dtype for low-cardinality strings (saves 90% memory)
df['product'] = df['product'].astype('category')

# Memory before: 800MB; after: 80MB for 1M rows
print(df.memory_usage(deep=True))
```

### Example 4: Time-Based Resampling and Aggregation
```python
# Intraday data → daily
df_daily = df.resample('D').agg({
    'price': 'last',
    'volume': 'sum',
    'high': 'max',
    'low': 'min'
})

# Rolling correlation
rolling_corr = df['returns'].rolling(window=60).corr(benchmark['returns'])
```

### Example 5: Feature Engineering with Groupby Transform
```python
# Create features relative to group mean
df['salary_vs_dept_mean'] = df.groupby('department')['salary'].transform(
    lambda x: (x - x.mean()) / x.std()
)

# Rank within group
df['dept_rank'] = df.groupby('department')['salary'].rank()

# Cumulative sum within group
df['salary_cumsum'] = df.groupby('department')['salary'].cumsum()
```

---

## 8. How Interviewers Think

### Red Flags
- ❌ Using apply() when vectorized method exists
- ❌ Not understanding groupby semantics (apply vs transform vs agg)
- ❌ Ignoring performance; creating copies unnecessarily
- ❌ Not handling missing data explicitly

### Green Flags
- ✅ Understanding split-apply-combine
- ✅ Using appropriate dtype (category for strings)
- ✅ Knowing when to use merge vs concat
- ✅ Memory-efficient operations on large datasets

### Answer Matrix
**Q: "How would you compute mean salary per department and add it back to DataFrame?"**
- 🟢 Use transform: `df.groupby('dept')['salary'].transform('mean')`
- 🟡 Use merge: `pd.merge(df, agg, on='dept')`
- 🔴 Use apply with loop (slow; creates copies)

---

## 9. Frequently Asked Interview Questions

### Beginner (Q1-Q20)

**Q1: What is the difference between Series and DataFrame?**
A: Series is 1D labeled array. DataFrame is 2D table with columns. Access DataFrame column returns Series.

**Q2: How do you read a CSV file into Pandas?**
A: `pd.read_csv('file.csv', sep=',', dtype={'id': int}, na_values='NA')`

**Q3: Explain groupby semantics.**
A: Split data by group key; apply function to each group; combine results. Example: `df.groupby('dept')['salary'].mean()`.

**Q4: What is the difference between merge and concat?**
A: merge() joins on key (SQL-like). concat() combines rows/columns. Use merge for relational data; concat for stacking.

**Q5: How do you handle missing values in Pandas?**
A: isna() detects; dropna() removes; fillna() replaces. Use interpolate() for smooth fill.

**Q6: Explain apply, transform, and agg in groupby context.**
A: agg reduces to single value per group. transform returns same shape. apply is flexible but slower.

**Q7: What is MultiIndex?**
A: Hierarchical index with multiple levels. Enables sophisticated grouping and slicing operations.

**Q8: How do you rename columns?**
A: `df.rename(columns={'old': 'new'})`

**Q9: What is a pivot table?**
A: Reshape data; aggregate by dimensions. Example: rows=region, columns=product, values=sales sum.

**Q10: How do you filter DataFrame rows?**
A: Boolean indexing: `df[df['age'] > 30]`

**Q11: What is loc vs iloc?**
A: loc is label-based; iloc is position-based.

**Q12: How do you set index?**
A: `df.set_index('column_name')`

**Q13: Explain rolling windows.**
A: Compute aggregation over sliding window. `ts.rolling(30).mean()` computes 30-day moving average.

**Q14: What is resample?**
A: Change time-series frequency. `ts.resample('M').sum()` converts daily to monthly.

**Q15: How do you handle duplicates?**
A: `df.drop_duplicates(subset=['col1', 'col2'])`

**Q16: What is the difference between copy and view in Pandas?**
A: Slicing can return view or copy depending on context. Use `.copy()` when unsure.

**Q17: How do you apply custom function to DataFrame?**
A: `df.apply(custom_fn, axis=0)` applies to columns; axis=1 for rows.

**Q18: Explain categorical dtype.**
A: Stores categories, not values; saves 90% memory for low-cardinality strings. `df['col'].astype('category')`

**Q19: How do you compute correlation?**
A: `df.corr()` computes correlation matrix; `df['x'].corr(df['y'])` pairwise correlation.

**Q20: How do you get descriptive statistics?**
A: `df.describe()` shows count, mean, std, min, 25%, 50%, 75%, max.

### Intermediate (Q21-Q40)

**Q21: How would you handle class imbalance in a classification dataset?**
A: Oversample minority, undersample majority, or use SMOTE. `df.groupby('target').size()` check balance.

**Q22: Explain handling missing data in time series.**
A: Forward fill `fillna(method='ffill')`, interpolate `interpolate()`, or seasonal decomposition.

**Q23: How do you merge on multiple keys?**
A: `pd.merge(df1, df2, on=['key1', 'key2'])`

**Q24: What is stack and unstack?**
A: stack() pivots columns → rows. unstack() pivots rows → columns.

**Q25: How do you get top N rows per group?**
A: `df.groupby('group').apply(lambda x: x.nlargest(5, 'value'))`

**Q26: Explain .loc vs .at.**
A: loc is for rows/columns; at is for single element (faster).

**Q27: How do you handle outliers?**
A: Z-score: keep `|z| < 3`. IQR: keep between Q1-1.5*IQR and Q3+1.5*IQR.

**Q28: Implement SQL DISTINCT in Pandas.**
A: `df['col'].unique()` or `df.drop_duplicates(subset=['col'])`

**Q29: How do you compute cumulative statistics?**
A: `df.cumsum()`, `df.cumprod()`, `df.cummax()`, `df.cummin()`

**Q30: Explain the difference between reset_index and set_index.**
A: set_index() moves column to index. reset_index() moves index to column.

### Advanced (Q31-Q60) 

**Q31: How would you handle memory efficiently for 100M row DataFrame?**
A: Use categorical dtype, downcast int/float, partition into chunks, use parquet/HDF5.

**Q32: Implement window functions equivalent to SQL LAG/LEAD.**
A: `df['lag'] = df.groupby('group')['value'].shift(1)`

**Q33: How do you join on date ranges (non-exact match)?**
A: Use `pd.merge_asof()` for approximate join on sorted key.

**Q34: Explain performance implications of different index types.**
A: Hash index O(1) lookup; RangeIndex O(1); MultiIndex O(log n) but hierarchical.

**Q35-Q60: [Additional advanced scenarios covering distributed Pandas, dask integration, performance optimization, complex data pipelines, and real-world data science workflows.]**

---

## 10. Common Mistakes

**Mistake 1: Using apply() instead of vectorized methods**
- ❌ `df.apply(lambda x: x ** 2)` (slow)
- ✅ `df ** 2` (vectorized)
- Impact: 10-100x slower

**Mistake 2: Not specifying dtype when reading CSV**
- ❌ `pd.read_csv('file.csv')` (infers all types)
- ✅ `pd.read_csv('file.csv', dtype={'id': int, 'date': 'datetime64'})`
- Impact: Parsing time; memory waste

**Mistake 3: Forgetting to handle missing data**
- ❌ Pass NaN to model
- ✅ Explicit dropna() or fillna()
- Impact: Model errors; unpredictable behavior

**Mistake 4: Confusing agg and transform**
- ❌ Use agg when transform needed (shape mismatch)
- ✅ agg reduces; transform preserves shape
- Impact: Silent bugs; shape errors

**Mistake 5: Creating unnecessary copies**
- ❌ `df_copy = df[df > 5]` (modifying then forgetting)
- ✅ Use `.copy()` only when modifying
- Impact: Memory waste; performance hit

**Mistake 6: Ignoring index misalignment**
- ❌ Concatenate without checking index
- ✅ Reset index; use concat with ignore_index=True
- Impact: Incorrect alignment; silent bugs

**Mistake 7: Not using categorical for strings**
- ❌ Store low-cardinality strings as object
- ✅ `df['col'].astype('category')`
- Impact: 10x memory usage

**Mistake 8: Modifying DataFrame in loop**
- ❌ `for row in df: df.loc[row] = ...`
- ✅ Vectorized operations or list → DataFrame
- Impact: 100x slower

**Mistake 9: Not understanding groupby direction**
- ❌ Confusion between axis, how groups formed
- ✅ Test with small data first
- Impact: Wrong aggregation results

**Mistake 10: Ignoring performance on large datasets**
- ❌ No optimization for 100M rows
- ✅ Profile; use efficient dtypes; partition data
- Impact: Out of memory; timeouts

---

## 11. Comparison Section

### Pandas vs SQL

| Task | Pandas | SQL |
|------|--------|-----|
| **Filter** | `df[df['age'] > 30]` | `WHERE age > 30` |
| **Group** | `.groupby('col')` | `GROUP BY col` |
| **Join** | `.merge()` | `JOIN` |
| **Aggregate** | `.agg()` | `SUM(), COUNT()` |
| **Order** | `.sort_values()` | `ORDER BY` |

---

## 12. Practical Projects

**Project 1: Data Cleaning Pipeline**
Read messy CSV; handle missing data; remove duplicates; validate schemas.

**Project 2: Sales Analytics**
Load transactions; group by region/product; compute KPIs; create pivot tables.

**Project 3: Time Series Analysis**
Load stock prices; resample; compute moving averages; detect anomalies.

---

## 13. Internship Preparation Notes

**Resume Tips**:
- "Cleaned 50M row dataset using Pandas; identified and handled 15% missing data"
- "Designed feature engineering pipeline with groupby transforms; improved model accuracy by 5%"
- "Built automated reporting using pivot tables and aggregations"

---

## 14. Cheat Sheet

**Basic Operations**
```python
df.head()
df.info()
df.describe()
df['col']
df[df['x'] > 5]
df.groupby('col').agg()
df.merge(other, on='key')
df.fillna(0)
```

---

## 15. One-Day Revision Checklist

- [ ] Read/write CSV with dtype specification
- [ ] Boolean indexing and filtering
- [ ] Groupby split-apply-combine
- [ ] Merge (inner/left/outer)
- [ ] Handle missing data (dropna, fillna)
- [ ] Understand agg vs transform
- [ ] Pivot tables
- [ ] Time series resample and rolling
- [ ] MultiIndex operations
- [ ] Memory optimization (categorical, dtype)

### Advanced (Q41-Q60)

**Q41: How would you implement a custom rolling aggregation?**
A: Use rolling().apply() with custom function. Example: rolling MAD (Mean Absolute Deviation).

**Q42: Explain memory profiling for large DataFrames.**
A: Use df.memory_usage(deep=True); identify expensive dtypes; convert to category or downcast int/float.

**Q43: How do you handle imbalanced classes in classification?**
A: Oversample minority (resample), undersample majority, or use SMOTE.

**Q44: Implement SQL HAVING clause equivalent.**
A: Filter after groupby: `df.groupby('col').filter(lambda x: len(x) > threshold)`

**Q45: How to get n_largest and n_smallest by group?**
A: `df.groupby('group').apply(lambda x: x.nlargest(n, 'value'))`

**Q46: Explain how to handle time zone conversions.**
A: `df['date'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')`

**Q47: How to implement cumulative operations within groups?**
A: `df.groupby('group')['value'].cumsum()`

**Q48: What is the difference between nunique and cardinality?**
A: nunique() counts unique values; cardinality refers to count of unique values.

**Q49: How to merge on partial key match?**
A: Use merge_asof() for nearest-match join on sorted key.

**Q50: Implement hierarchical index slicing efficiently.**
A: Use .xs() or IndexSlice notation for multi-level indexing.

**Q51: How do you handle circular references in DataFrames?**
A: Avoid modifying while iterating; use vectorized operations.

**Q52: Explain distributed Pandas with Dask.**
A: Dask provides lazy evaluation; scales Pandas to clusters.

**Q53: How to efficiently compute DataFrame.apply on large data?**
A: Use vectorized methods first; apply() as last resort; consider Numba/Cython for loops.

**Q54: Implement rolling correlation matrix efficiently.**
A: Use DataFrame.rolling().cov() or pandas_rolling_stats library.

**Q55: How do you profile Pandas code?**
A: Use %prun in Jupyter; cProfile for detailed timing.

**Q56: Explain the difference between merge, join, and concat.**
A: merge() uses keys; join() uses index; concat() combines rows/columns.

**Q57: How to efficiently find nearest neighbor in DataFrame?**
A: Use merge_asof() on sorted index; KD-tree if complex.

**Q58: Implement feature engineering pipeline with Pandas.**
A: Define transformers; chain with pipe(): df.pipe(func1).pipe(func2).

**Q59: How to handle schema evolution (new columns over time)?**
A: Read with specific dtypes; fill missing with appropriate values; validate schema.

**Q60: Explain how to optimize groupby for large datasets.**
A: Ensure groupby key is indexed; consider aggregate over apply; profile with %prun.

---

#### 61. What is the difference between GroupBy.apply() and GroupBy.transform()? When should you use each?
- **Detailed Answer**:
  - `GroupBy.apply()` is the most flexible split-apply-combine tool. It passes each sub-DataFrame (group) to the custom function. The function can return a DataFrame, Series, or scalar of any shape. Because it operates on high-level Pandas objects per group, it incurs substantial Python overhead and is relatively slow.
  - `GroupBy.transform()` applies a function to each column of each group, and must return a Series that is the **same shape** as the input group. Pandas optimizes `transform` internally (especially for built-in strings like `'mean'`, `'std'`, `'sum'`), broadcasting the aggregated values back to the original row indexes.
  - *When to use*: Use `transform` for broadcasting group statistics back to the original DataFrame (e.g. z-scoring columns within groups). Use `apply` only when the operation cannot be expressed as a standard reduction/transformation (e.g., fitting a regression model per group and returning coefficients).
- **Follow-up Questions**: What is the difference between `transform` and `agg`? (Answer: `agg` reduces the dimensions by returning one row per group, whereas `transform` retains the original DataFrame's row dimensions).
- **Interviewer's Expectations**: Contrast the input/output shapes of both methods, explain that `transform` is optimized and vectorized while `apply` has heavy Python loop overhead, and provide a practical use-case (like group-level scaling).

---

#### 62. How does Pandas store data internally? Explain the role of the BlockManager and how heterogeneous dtypes affect performance.
- **Detailed Answer**: Internally, Pandas DataFrames do not store data as a collection of individual column arrays. Instead, they use a data structure called the **BlockManager**. The BlockManager groups columns of the **same data type** into 2D NumPy arrays (blocks). For example, all float64 columns are stored in one 2D float64 block, and all int64 columns in an int64 block.
Heterogeneous dtypes affect performance in several ways:
  - **Memory & Copying**: Operations that force type coercion (e.g., inserting a float into an integer column) require Pandas to split/rebuild blocks, which is slow and memory-intensive.
  - **Single Dtype Operations**: If a DataFrame consists of a single dtype (e.g., all float64), operations like transposing or `.values` are zero-copy views. If there are mixed dtypes, calling `.values` forces consolidation into a single 2D object array, copying all data and upcasting numeric values.
- **Follow-up Questions**: How does Pandas 2.0 PyArrow integration change this? (Answer: PyArrow stores data in a column-oriented format (Arrow tables) with contiguous memory chunks per column, avoiding the block-consolidation overhead of BlockManager and improving speed for string and null-value operations).
- **Interviewer's Expectations**: Define the BlockManager, explain that columns of the same type are grouped into 2D blocks, and identify how mixed-dtype DataFrames cause memory copying and type upcasting during conversions.

---

#### 63. How do df.query() and pd.eval() improve performance and memory efficiency in Pandas?
- **Detailed Answer**: Standard Pandas expressions like `df[(df['A'] > 5) & (df['B'] < 10)]` evaluate step-by-step, allocating large temporary boolean arrays in memory for each sub-expression. For massive DataFrames, this causes cache misses and high memory overhead.
  - `df.query()` and `pd.eval()` solve this by taking string expressions and compiling them into optimized bytecode.
  - Under the hood, they use **NumExpr** (if installed), which evaluates the entire expression in a single pass in C. It splits the array into small chunks that fit into the CPU's L1/L2 cache, executing operations in parallel across multiple CPU cores without allocating intermediate temporary arrays.
  - *When to use*: Use them when performing mathematical column transformations or complex row filtering on large DataFrames (typically >100,000 rows) to save memory and speed up computation.
- **Follow-up Questions**: Can you reference local variables inside `df.query()`? (Answer: Yes, by prefixing the variable name with the `@` symbol, e.g., `df.query("salary > @min_sal")`).
- **Interviewer's Expectations**: Describe how standard Pandas allocations create temporary arrays, explain how NumExpr compiles string expressions to run in C-level loops, and mention CPU cache locality and parallel execution.

---

## 10. Common Mistakes

**Mistake 1: Using apply() instead of vectorized methods**
- ❌ `df['col'].apply(lambda x: x ** 2)` (slow on 1M rows)
- ✅ `df['col'] ** 2` (vectorized; 100x faster)
- Impact: 10-100x performance penalty

**Mistake 2: Not specifying dtype when reading CSV**
- ❌ Automatic type inference (slow, incorrect)
- ✅ `pd.read_csv('data.csv', dtype={'id': 'int32', 'amount': 'float32'})`
- Impact: 2x slower I/O; 2x memory usage

**Mistake 3: Forgetting to handle missing data**
- ❌ Pass NaN to model/aggregation
- ✅ Explicit dropna() or fillna()
- Impact: Silent bugs; model errors

**Mistake 4: Confusing agg(), transform(), and apply()**
- ❌ Use agg() when transform needed (shape mismatch)
- ✅ agg reduces rows; transform preserves shape
- Impact: Shape errors; incorrect results

**Mistake 5: Creating unnecessary copies**
- ❌ `filtered = df[df['age'] > 30]; filtered['new_col'] = ...`
- ✅ Use chaining or `.copy()` only when modifying
- Impact: 2x memory usage; slower

**Mistake 6: Modifying DataFrame in loop**
- ❌ `for idx, row in df.iterrows(): df.loc[idx] = ...`
- ✅ Vectorized operations or build list then DataFrame
- Impact: 100x slower on 100K rows

**Mistake 7: Not using categorical for strings**
- ❌ Store low-cardinality strings as 'object' dtype
- ✅ `df['col'] = df['col'].astype('category')`
- Impact: 10x memory waste on 1M rows

**Mistake 8: Ignoring index misalignment**
- ❌ concat() without checking index alignment
- ✅ Reset index or use concat(ignore_index=True)
- Impact: Silent alignment errors

**Mistake 9: Not understanding groupby semantics**
- ❌ Confusion between agg() vs transform() in groupby
- ✅ Test with small data; understand output shape
- Impact: Wrong aggregation results

**Mistake 10: Ignoring performance on large datasets**
- ❌ No optimization for 100M rows
- ✅ Use efficient dtypes, indexing, partitioning
- Impact: Out-of-memory errors; timeouts

## 11. Comparison

### Pandas vs NumPy vs SQL

| Task | Pandas | NumPy | SQL |
|------|--------|-------|-----|
| **Tabular Data** | Best | Not ideal | Good |
| **Mixed Types** | Yes | No | Yes |
| **Labels** | Yes | No | Yes |
| **Groupby** | Easy | Complex | Native |
| **Performance** | Good | Best | Fast |

---

## 12. Projects

**Project 1: Data Cleaning Pipeline**
Read messy CSV; handle 15% missing data; remove duplicates; validate schema; export.

**Project 2: Sales Analytics Dashboard**
Load transactions; compute KPIs by region/product; create pivot tables; visualize trends.

**Project 3: Feature Engineering for ML**
Aggregate user behavior; create lag features; handle imbalance; export train/test sets.

---

## 13. Internship Prep

**Resume Highlights**:
- "Cleaned 50M row dataset; identified and imputed 15% missing values"
- "Engineered features for ML model using groupby transforms; improved accuracy 8%"
- "Built automated reporting using pivot tables and Seaborn visualization"

**Interview Focus**:
- Groupby semantics (agg vs transform)
- Merge strategies (left/right/outer/inner)
- Memory optimization (dtype, categorical)
- Real-world data issues (missing data, duplicates)

---

## 14. Cheat Sheet

**Reading/Writing**
```python
df = pd.read_csv('file.csv', dtype={'id': int})
df.to_csv('output.csv', index=False)
df = pd.read_excel('file.xlsx', sheet_name='Sheet1')
```

**Exploration**
```python
df.head(10)
df.describe()
df.info()
df.value_counts()
```

**Filtering**
```python
df[df['col'] > 5]
df[(df['col1'] > 5) & (df['col2'] == 'A')]
df.isin(['value1', 'value2'])
```

**Grouping**
```python
df.groupby('col')['val'].sum()
df.groupby(['col1', 'col2']).agg({'val': 'mean'})
df.groupby('col').apply(custom_function)
```

**Merging**
```python
pd.merge(df1, df2, on='key', how='inner')
df1.join(df2, lsuffix='_left')
pd.concat([df1, df2], axis=0)
```

**Time Series**
```python
df.set_index('date').resample('M').sum()
df.rolling(30).mean()
df['date'].dt.month
```

