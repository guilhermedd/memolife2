import psycopg2

try:
    with open('password.txt', 'r') as file:
        PASSWORD = file.read().splitlines()[0]

    # Conectar ao banco de dados PostgreSQL
    CONN = psycopg2.connect(
        host="localhost",
        database="memolife",
        user="postgres",
        password=PASSWORD
    )
except (Exception, psycopg2.DatabaseError) as error:
    print("Ocorreu um erro", error)

def get():
    with CONN.cursor() as cur:
        cur.execute(
            "SELECT * FROM USERS"
        )
        id = cur.fetchone()
        print(id)
        # cur.execute("SELECT * FROM Users WHERE id = %s;", (id))
        # user_data = cur.fetchone()
        # print("User created: " + user_data)
get()
CONN.commit()
CONN.close()
