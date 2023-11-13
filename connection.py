import psycopg2

def connect_db():
    try:
        with open('password.txt', 'r') as file:
            PASSWORD = file.read().splitlines()[0]

        # Conectar ao banco de dados PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            database="memolife",
            user="postgres",
            password=PASSWORD
        )
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)