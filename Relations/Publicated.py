import psycopg2
import datetime

class Publicated:
    def __init__(self, date, time, id_user, id_post, conn, id = None):
        self.id                 = id
        self.date               = date
        self.time               = time
        self.id_user            = id_user
        self.id_post            = id_post
        self.CONN               = conn
    
    def create(self):
        try:
            with open('password.txt', 'r') as file:
                PASSWORD = file.read().splitlines()[0]
# Conectar ao banco de dados PostgreSQL
            self.CONN = psycopg2.connect(
                host="localhost",
                database="memolife",
                user="postgres",
                password=PASSWORD
            )
            with self.CONN.cursor() as cur:
                now = datetime.datetime.now()
                date = now.strftime("%d/%m/%Y")
                self.date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
                time = now.strftime("%H:%M:%S")
                self.time = datetime.datetime.strptime(time, "%H:%M:%S").time()

                cur.execute(
                    "INSERT INTO Publicated (date, time, id_user, id_post) VALUES (%s, %s, %s, %s) RETURNING id;",
                    (self.date, self.time, self.id_user, self.id_post)
                )
                pych_data = cur.fetchone()
                self.id = pych_data[0]
                
                print("Published relation created:\n", self.show())
                self.CONN.commit()
            return pych_data
        except (Exception, psycopg2.DatabaseError) as error:
            print("Publicated error(create):",error)
            return None
    
    def delete(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"DELETE FROM Publicated WHERE id = {self.id};",
                )
                print(f"Deleted {self.show()}")
                self.CONN.commit()
                return 0
        except (Exception, psycopg2.DatabaseError) as error:
            print("Publicated error(delete):",error)
            return -1
    
    def show(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"SELECT * FROM Users WHERE id = {self.id_user};",
                )
                user = cur.fetchone()
                cur.execute(
                    f"SELECT * FROM Posts WHERE id = {self.id_post};",
                )
                post = cur.fetchone()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Publicated error(show):",error)

        return f"""
        User: 
        Id: {user[0]}
        Name: {user[3]} {user[4]}
        Username: {user[5]}
        -------------------
        Post: 
        Id: {post[0]}
        Title: {post[1]}
        Summary: {post[2]}
        Feeling: {post[4]}
        Date: {post[5]}
        Is Public: {post[6]}
        """
        


    
