import psycopg2
from Psycologists import Psycologists
from Users import Users
from Posts import Posts
from Consultations import Consultations

with open('password.txt', 'r') as file:
    PASSWORD = file.read().splitlines()[0]

# # Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="memolife",
    user="postgres",
    password=PASSWORD
)

# Create the Users table
with conn.cursor() as cur:
    cur.execute("""
        SELECT * FROM Users WHERE last like 'dos Santos%';
    """)
    print(cur.fetchall())
    # fetchall() retorna uma lista de tuplas


# Commit the changes and close the connection
conn.commit()
conn.close()
