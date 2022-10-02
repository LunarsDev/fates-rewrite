SELECT sh.nspname AS table_schema,
  tbl.relname AS table_name,
  col.attname AS column_name,
  referenced_sh.nspname AS foreign_table_schema,
  referenced_tbl.relname AS foreign_table_name,
  referenced_field.attname AS foreign_column_name
FROM pg_constraint c
    INNER JOIN pg_namespace AS sh ON sh.oid = c.connamespace
    INNER JOIN (SELECT oid, unnest(conkey) as conkey FROM pg_constraint) con ON c.oid = con.oid
    INNER JOIN pg_class tbl ON tbl.oid = c.conrelid
    INNER JOIN pg_attribute col ON (col.attrelid = tbl.oid AND col.attnum = con.conkey)
    INNER JOIN pg_class referenced_tbl ON c.confrelid = referenced_tbl.oid
    INNER JOIN pg_namespace AS referenced_sh ON referenced_sh.oid = referenced_tbl.relnamespace
    INNER JOIN (SELECT oid, unnest(confkey) as confkey FROM pg_constraint) conf ON c.oid = conf.oid
    INNER JOIN pg_attribute referenced_field ON (referenced_field.attrelid = c.confrelid AND referenced_field.attnum = conf.confkey)
WHERE c.contype = 'f'