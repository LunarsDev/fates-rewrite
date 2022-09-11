# Fates List Rewrite

## Components

- ``Mapleshade`` - The core API implementations of fates list

## Requirements

- Python 3.10+

## Database Seeding

Firstly apply piccolo migrations.

Then, pen ``psql``, then run the following:

```sql
\c fateslist

\copy bots FROM 'seed_data/seed.csv' DELIMITER ',' CSV;
```