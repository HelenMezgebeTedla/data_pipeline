# Data Pipeline

Simple Python pipeline that loads user data from a public REST API into a local SQLite warehouse.

## Run

```bash
python3 pipeline.py
```

## Output

- `warehouse.db` SQLite database with `users` table
- `pipeline.log` run log

## Features

- Retry with backoff on API failure
- Upsert (idempotent loads)
- Structured logging
