# Week 10

This folder contains Python scripts and SQL files developed during Week 10 of the FinTrust Cloud Portfolio project.

## Folder Structure

```text
week_10/
├── python/
│   ├── fintrust_migration/
|   |   ├── __init__.py 
|   |   ├── utils/
|   |   |   ├── __init__.py
|   |   |   └── sessions.py
|   |   └── s3/ 
|   |      ├── __init__.py
|   |      └── sync_helpers.py
│   ├── classifier.py
│   └── dms_helpers.py
└── sql/
    ├── datasync_views.sql
    ├── dms_views.sql
    ├── sql_views.sql
    └── v_wave_progress.sql
```

## Contents

### Python

| File/Folder | Description |
|-------------|-------------|
| `fintrust_migration/` | Migration-related Python modules and scripts. |
| `classifier.py` | Classification logic and processing utilities. |
| `dms_helpers.py` | Helper functions for DMS-related operations. |

### SQL

| File | Description |
|-------|-------------|
| `datasync_views.sql` | SQL views related to data synchronization. |
| `dms_views.sql` | SQL views supporting DMS processes. |
| `sql_views.sql` | General SQL view definitions. |
| `v_wave_progress.sql` | View for tracking wave progress metrics. |

## Purpose

This week's work focuses on:

- Database view creation and management.
- Data migration support utilities.
- DMS integration helpers.
- Data classification and processing logic.

## Repository Path

```text
fintrust-cloud-portfolio/
└── week_10/
```
