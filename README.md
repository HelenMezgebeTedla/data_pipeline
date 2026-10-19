# Data Pipeline

Simple Python pipeline that loads user data from a public REST API
into a local SQLite warehouse.

## Setup
```bash
source ~/projects/env/bin/activate
pip install -r requirements.txt
```

## Run
```bash
python3 pipeline.py
```

## Output
- `warehouse.db` SQLite database with `users` table
- `pipeline.log` run log

## Features
- Retry with backoff on API failure
- Idempotent loads: running the pipeline twice keeps 10 rows, not 20,
  because ON CONFLICT(id) updates the existing row instead of inserting a new one
- Structured logging to file and console

## Production
In production, SQLite would be replaced by Google BigQuery using
google-cloud-bigquery, matching the Compass stack

## Security
.env and *.db files are gitignored so secrets and local data
never reach the repository