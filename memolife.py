import psycopg2
from Psycologists import Psycologists
from Users import Users
from Posts import Posts
from Consultations import Consultations

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="memolife",
    user="postgres",
    password="8837"
)

# Create the Users table
with conn.cursor() as cur:
    cur.execute("""
        SELECT * FROM Users;
    """)
    # fetchall() retorna uma lista de tuplas
    print(cur.fetchall()[0])



# Commit the changes and close the connection
conn.commit()
conn.close()
