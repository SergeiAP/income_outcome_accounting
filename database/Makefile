fill_database:
	sqlite3 ../src/database.sqlite3 < ../database/init_insert.sql
fill_database_with_user_1_2:
	sqlite3 ../src/database.sqlite3 < ../database/init_insert_user.sql
drop_operations_table:
	sqlite3 ../src/database.sqlite3  'DROP TABLE operations;'
drop_alembic_table:
	sqlite3 ../src/database.sqlite3  'DROP TABLE alembic_version;'
drop_users_table:
	sqlite3 ../src/database.sqlite3  'DROP TABLE users;'
