# Fates List Rewrite

## Components

- ``Mapleshade`` - The core API implementations of fates list
- ``Sunbeam`` - Fates List Frontend

## Requirements

- Python 3.10+

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