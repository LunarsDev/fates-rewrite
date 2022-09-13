# Fates List Rewrite

## Components

### Backend

- ``Mapleshade`` - The core API implementations of fates list
- ``Silverpelt`` - A IPC service to handle all discord API actions (using fastapi and msgpack)

### Frontend

- ``Sunbeam`` - Fates List Frontend

## Requirements

- Python 3.10+

## Running

1. Run ``uvicorn silverpelt.app:app --port 3030`` to start silverpelt
2. Then run ``uvicorn fates.app:app`` to start main API

## Database Seeding

Firstly apply piccolo migrations.

Then, pen ``psql``, then run the following:

```sql
\c fateslist

\copy bots FROM 'seed_data/seed.csv' DELIMITER ',' CSV;
```

## DB Changes

**Sept 12th 2022** 

- ``bot_library`` renamed to ``library``