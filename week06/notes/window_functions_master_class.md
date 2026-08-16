# SQL Window Functions Master Class

## Introduction

Window functions perform calculations across a set of rows related to the current row without collapsing the result set. Unlike `GROUP BY`, window functions return a value for every row while still allowing access to row-level detail.

## Why Window Functions Matter

Traditional aggregates:

```sql
SELECT Department, AVG(Salary)
FROM Employees
GROUP BY Department;
```

Returns one row per department.

Window aggregate:

```sql
SELECT EmployeeName,
       Department,
       Salary,
       AVG(Salary) OVER(PARTITION BY Department) AS DeptAvgSalary
FROM Employees;
```

Returns every employee plus the departmental average.

---

# Window Function Syntax

General pattern:

```sql
window_function(expression)
OVER (
    PARTITION BY column_name
    ORDER BY column_name
    frame_clause
)
```

Based on the screenshots, a window consists of four major components:

1. Function Expression
2. OVER Clause
3. PARTITION BY Clause
4. ORDER BY Clause
5. Frame Clause (optional but powerful)

Example:

```sql
AVG(Sales) OVER (
    PARTITION BY Category
    ORDER BY OrderDate
    ROWS UNBOUNDED PRECEDING
)
```

## Function Expression

Defines the calculation.

Examples:

```sql
AVG(Sales)
SUM(Sales)
COUNT(*)
RANK()
LAG(Sales)
```

## OVER Clause

Defines the window used by the calculation.

```sql
SUM(Sales) OVER()
```

Calculates the sum across the entire result set.

---

# PARTITION BY

Divides data into independent groups.

```sql
SUM(Sales) OVER(PARTITION BY Category)
```

Each category becomes its own logical window.

Example:

```sql
SELECT Product,
       Category,
       Sales,
       SUM(Sales) OVER(PARTITION BY Category) AS CategoryTotal
FROM SalesData;
```

---

# ORDER BY in Window Functions

Controls sequence inside a partition.

```sql
SUM(Sales) OVER(
    PARTITION BY Category
    ORDER BY OrderDate
)
```

Often used for:

- Running totals
- Ranking
- Moving averages
- Period comparisons

---

# Window Function Categories

## 1. Aggregate Window Functions

These use traditional aggregate functions as window functions.

### COUNT

```sql
COUNT(*) OVER(PARTITION BY Category)
```

### SUM

```sql
SUM(Sales) OVER(PARTITION BY Category)
```

### AVG

```sql
AVG(Sales) OVER(PARTITION BY Category)
```

### MIN

```sql
MIN(Sales) OVER(PARTITION BY Category)
```

### MAX

```sql
MAX(Sales) OVER(PARTITION BY Category)
```

### Challenge 1

Return:

- Product
- Category
- Sales
- Category Total Sales
- Category Average Sales

---

# Ranking Window Functions

## ROW_NUMBER()

Assigns a unique sequential number.

```sql
ROW_NUMBER() OVER(
    PARTITION BY Category
    ORDER BY Sales DESC
)
```

Example:

```text
Sales  Row_Number
1000   1
900    2
900    3
800    4
```

## RANK()

Equal values get the same rank.

Gaps appear.

```sql
RANK() OVER(
    ORDER BY Sales DESC
)
```

```text
1000  1
900   2
900   2
800   4
```

## DENSE_RANK()

Equal values share a rank.

No gaps.

```sql
DENSE_RANK() OVER(
    ORDER BY Sales DESC
)
```

```text
1000  1
900   2
900   2
800   3
```

## PERCENT_RANK()

Returns relative ranking between 0 and 1.

```sql
PERCENT_RANK() OVER(
    ORDER BY Sales
)
```

## CUME_DIST()

Cumulative distribution.

```sql
CUME_DIST() OVER(
    ORDER BY Sales
)
```

## NTILE()

Divides rows into buckets.

```sql
NTILE(4) OVER(
    ORDER BY Sales DESC
)
```

Often used for quartiles.

### Challenge 2

Find the top 3 products by sales within each category.

---

# Value (Analytic) Functions

## LAG()

Accesses a previous row.

Syntax:

```sql
LAG(expression, offset, default)
```

Example:

```sql
SELECT OrderDate,
       Sales,
       LAG(Sales,1,0) OVER(
           ORDER BY OrderDate
       ) AS PreviousSales
FROM SalesData;
```

## LEAD()

Accesses a future row.

```sql
LEAD(Sales,1,0) OVER(
    ORDER BY OrderDate
)
```

## FIRST_VALUE()

Returns the first value in the window.

```sql
FIRST_VALUE(Sales) OVER(
    ORDER BY OrderDate
)
```

## LAST_VALUE()

Returns the last value in the frame.

```sql
LAST_VALUE(Sales) OVER(
    ORDER BY OrderDate
    ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
)
```

### Challenge 3

Calculate month-over-month sales growth using LAG().

---

# Frame Clause Deep Dive

The frame clause defines which rows are visible to the current calculation.

## Frame Types

### ROWS

Uses physical row positions.

```sql
ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
```

### RANGE

Uses logical value ranges.

```sql
RANGE BETWEEN UNBOUNDED PRECEDING
      AND CURRENT ROW
```

---

# Frame Boundaries

Lower boundaries:

```sql
CURRENT ROW
N PRECEDING
UNBOUNDED PRECEDING
```

Upper boundaries:

```sql
CURRENT ROW
N FOLLOWING
UNBOUNDED FOLLOWING
```

Example:

```sql
AVG(Sales) OVER(
    ORDER BY OrderDate
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)
```

Calculates a 3-row moving average.

---

# Common Patterns

## Running Total

```sql
SELECT OrderDate,
       Sales,
       SUM(Sales) OVER(
           ORDER BY OrderDate
           ROWS UNBOUNDED PRECEDING
       ) AS RunningTotal
FROM SalesData;
```

## Moving Average

```sql
SELECT OrderDate,
       AVG(Sales) OVER(
           ORDER BY OrderDate
           ROWS BETWEEN 6 PRECEDING
           AND CURRENT ROW
       ) AS SevenDayAverage
FROM SalesData;
```

## Percentage of Total

```sql
SELECT Product,
       Sales,
       Sales * 100.0 /
       SUM(Sales) OVER() AS PercentOfTotal
FROM SalesData;
```

## Top N Per Group

```sql
WITH Ranked AS (
    SELECT *,
           ROW_NUMBER() OVER(
               PARTITION BY Category
               ORDER BY Sales DESC
           ) AS rn
    FROM SalesData
)
SELECT *
FROM Ranked
WHERE rn <= 3;
```

---

# Interview Questions

1. Difference between GROUP BY and window functions?
2. Difference between RANK and DENSE_RANK?
3. When would you use ROW_NUMBER?
4. Difference between ROWS and RANGE?
5. Why does LAST_VALUE sometimes return unexpected results?
6. How do you calculate running totals?
7. How do you compare current and previous rows?

---

# Master Challenge

Using a Sales table containing:

```text
OrderID
OrderDate
Category
Product
Sales
```

Create a query that returns:

- Running Total by Category
- Category Average Sales
- Product Rank within Category
- Previous Sale Amount
- Next Sale Amount
- 3-row Moving Average
- Percentage of Category Total

Use:

- SUM()
- AVG()
- ROW_NUMBER() or RANK()
- LAG()
- LEAD()
- Frame clauses

---

# Key Takeaways

- Window functions do not collapse rows.
- OVER() defines the window.
- PARTITION BY creates groups.
- ORDER BY creates sequence.
- Frame clauses define visible rows.
- Aggregate, Ranking, and Analytic functions form the three major categories.
- Mastering LAG, LEAD, RANK, and running totals covers most real-world analytics workloads.
