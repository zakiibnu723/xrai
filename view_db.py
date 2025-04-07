import sqlite3

# Connect to the database
conn = sqlite3.connect('instance/patients.db')
cursor = conn.cursor()

# Query all data from the 'patient' table (replace 'patient' with your table name)
cursor.execute('SELECT * FROM patient')

# Fetch all rows
rows = cursor.fetchall()

# Print each row
for row in rows:
    print(row)

# Close the connection
conn.close()
