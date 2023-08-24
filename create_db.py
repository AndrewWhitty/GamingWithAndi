import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('gwa.db')

# Read the SQL statements from the .sql file
with open('gwa_database.sql', 'r') as sql_file:
    sql_statements = sql_file.read()

# Execute the SQL statements
conn.executescript(sql_statements)

# Commit and close the connection
conn.commit()
conn.close()
