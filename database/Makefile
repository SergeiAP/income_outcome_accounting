fill_database:
	sqlite3 ../src/database.sqlite3 < ../database/init_insert.sql
drop_operations_table:
	sqlite3 ../src/database.sqlite3  'DROP TABLE operations'
drop_alembic_table:
	sqlite3 ../src/database.sqlite3  'DROP TABLE alembic_version'
