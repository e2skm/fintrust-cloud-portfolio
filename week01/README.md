# Week 1 – Foundation

## Overview

During Week 1, I built a foundation in Git, GitHub, version control, and SQL. I learned how developers track changes, collaborate using repositories, write professional commit messages, resolve common Git issues, and query databases using SQL.

## Git and GitHub

### Git
Git is a distributed version control system used to track changes in files and projects.

### GitHub
GitHub is a cloud platform used to host Git repositories and collaborate with other developers.

## The Git Three-Area Model

### 1. Working Directory
The area where files are created, edited, and deleted.

### 2. Staging Area (Index)
A temporary area used to prepare changes before committing.

```bash
git add .
```

### 3. Repository (.git)
The database that stores commit history and project versions.

```bash
git commit -m "docs: add README"
```

### Workflow

```text
Working Directory
        ↓
     git add
        ↓
 Staging Area
        ↓
   git commit
        ↓
 Repository (.git)
```

## Basic Git Commands

```bash
git init
git clone <repository-url>
git status
git diff
git add .
git commit -m "message"
git log
git push origin main
git pull origin main
git fetch
```

## Writing Good Commit Messages

Good commits should:

- Be clear and concise
- Describe one logical change
- Be easy to understand later
- Follow a consistent format

Examples:

```text
feat: add customer search feature
fix: correct balance calculation
docs: update README
```

## Conventional Commits

### Common Types

```text
feat: new feature
fix: bug fix
docs: documentation changes
style: formatting changes
refactor: code improvement
test: testing updates
chore: maintenance work
```

## Common Git Problems and Solutions

### Forgot to Stage Changes

```bash
git add .
git commit -m "feat: add feature"
```

### Wrong Commit Message

```bash
git commit --amend -m "correct message"
```

### Accidentally Staged a File

```bash
git restore --staged filename
```

### Discard Local Changes

```bash
git restore filename
```

### Merge Conflicts

1. Open conflicting files.
2. Resolve the conflict.
3. Save the file.
4. Stage the changes.
5. Complete the commit.

## SQL Fundamentals

Using the FinTrust database, I practised writing SQL queries and filtering data.

### Topics Covered

- SELECT statements
- WHERE clause
- Comparison operators
- AND, OR, and NOT operators
- LIKE pattern matching
- IN operator
- BETWEEN operator
- NULL handling
- Date filtering
- ORDER BY sorting

### Example Queries

```sql
SELECT *
FROM customers
WHERE province = 'Gauteng';
```

```sql
SELECT *
FROM accounts
WHERE balance > 5000;
```

```sql
SELECT *
FROM customers
WHERE email LIKE '%gmail%';
```

```sql
SELECT *
FROM transactions
WHERE amount BETWEEN 100 AND 1000;
```

```sql
SELECT *
FROM transactions
WHERE merchant_category IS NULL;
```

## SQL Scripts Completed

### day4_where_filtering_queries.sql

Practised:

- Customer filtering
- Account filtering
- Transaction filtering
- LIKE queries
- IN conditions
- BETWEEN ranges
- NULL handling
- Logical operators
- Operator precedence

### day4_where_challenges.sql

Practised:

- Partial string matching
- Date filtering
- YEAR(), MONTH(), and DAY() functions
- Relative date filtering
- Aggregations involving NULL values
- Multi-condition filtering
- Sorting results with ORDER BY

## Skills Developed

- Git Version Control
- GitHub Repository Management
- Commit Standards
- Git Troubleshooting
- SQL Query Writing
- Data Filtering
- Database Fundamentals
- Problem Solving

## Week 1 Reflection

Week 1 provided a strong foundation in software development fundamentals. I gained practical experience using Git and GitHub, learned professional commit standards, and developed SQL skills for querying and filtering data. These skills will support future learning in software engineering, databases, and collaborative development environments.
