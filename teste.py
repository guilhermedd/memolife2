import psycopg2


with open('password.txt', 'r') as file:
        PASSWORD = file.read().splitlines()[0]
        print("Password:", PASSWORD)
# Conectar ao banco de dados PostgreSQL
CONN = psycopg2.connect(
    host="localhost",
    database="memolife",
    user="postgres",
    password=PASSWORD
)

with CONN.cursor() as cur:
    cur.execute(
        f"SELECT ispublic FROM Posts WHERE id = 4;",
    )
    users_list = cur.fetchall()[0]

    # emails_taken = [email[0] for email in users_list]
    if users_list[0] == True:
        print("True")
    else:
        print("False")
    # print(users_list[0])