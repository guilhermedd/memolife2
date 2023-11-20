import psycopg2
import datetime

class Posts:
    def __init__(self, title, summary, content, feeling, date, ispublic, conn, id = None):
        self.id = id
        self.title = title
        self.summary = summary
        self.content = content
        self.feeling = feeling
        self.date = date
        self.ispublic = ispublic
        self.CONN = conn

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
                cur.execute(
                "INSERT INTO Posts (title, summary, content, feeling, date, ispublic) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;",
                (self.title, self.summary, self.content, self.feeling, self.date, self.ispublic)
                )
                self.CONN.commit()

                post_data = cur.fetchone()
            print('Post_data', post_data[0])
            self.id = post_data[0]
            print("Post created:\n", self.show())

            return post_data
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error em Posts:",error)
            return None

    def create_self(self):
        print("Please insert the following data:")

        print("Type -1 to Exit or 1 to Continue!")
        while True:
            index = int(input("Do you want to continue?: \n"))
            if index == -1:
                return 0
            if index == 1:
                break

        title = input("Title (Maximum of 50 characters): \n")
        while len(title) > 50 or len(title) < 3:
            if len(email) > 50:
                email = input("Title is too long (Maximum of 50 characters): \n")
            elif len(email) < 3:
                email = input("Title is too short (Minimum of 3 characters): \n")

        summary = input("Summary (Maximum of 50 characters): \n")
        while len(summary) > 100 or len(summary) < 3:
            if len(summary) > 100:
                summary = input("Summary is too long (Maximum of 50 characters): \n")
            elif len(summary) < 3:
                summary = input("Summary is too short (Minimum of 3 characters): \n")

        content = input("Content (Maximum of 1000 characters): \n")
        while len(content) > 1000 or len(content) < 3:
            if len(content) > 1000:
                content = input("Content is too long (Maximum of 50 characters): \n")
            elif len(content) < 3:
                content = input("Content is too short (Minimum of 3 characters): \n")

        feeling = input("Feeling (Maximum of 20 characters): \n")
        while len(feeling) > 20 or len(feeling) < 3:
            if len(feeling) > 20:
                feeling = input("Feeling is too long (Maximum of 20 characters): \n")
            elif len(feeling) < 3:
                feeling = input("Feeling is too short (Minimum of 3 characters): \n")

        while True:
            date_str = input("Enter the date in the format DD/MM/YYYY (e.g., 14/11/2023): \n")

            # Tentar converter a string da data para um objeto datetime
            try:
                user_provided_date = datetime.datetime.strptime(date_str, "%d/%m/%Y")

                user_provided_date = user_provided_date.date()
                break # Se a conversão for bem-sucedida, sair do loop
            except ValueError:
                print("Invalid date format. Please use the format DD/MM/YYYY.")
                continue # Se houver um erro, continue solicitando a data

        ispublic = input("Is this post public? (y/n): \n")
        while ispublic != 'y' and ispublic != 'n':
            ispublic = input("Please answer with y or n: \n")

        ispublic = ispublic == 'y'

        self.title = title
        self.summary = summary
        self.content = content
        self.feeling = feeling
        self.date = user_provided_date
        self.ispublic = ispublic

        return 1

    def data(self):
        return [self.title, self.summary, self.content, self.feeling, self.date, self.ispublic]

    def show(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(f"""
                    SELECT u.*
                    FROM Users u
                    JOIN Publicated p ON u.ID = p.id_user
                    JOIN Posts pos ON p.id_post = pos.ID
                    WHERE pos.ID = {self.id};
                """)
                user = cur.fetchone()
        except (Exception, psycopg2.DatabaseError) as error:
            # print("Posts error(show):",error)
            user = None
            pass

        user = f"User: {user[3]} {user[4]} ({user[5]})" if user != None else "User: None"

        return f"""Id: {self.id}
        Title: {self.title}
        --------------
        Summary: 
        {self.summary}
        --------------
        Content: 
        {self.content}
        --------------
        Feeling: {self.feeling}
        Date: {self.date.strftime("%d/%m/%Y")}
        This post {'IS' if self.ispublic else 'is NOT'} public!
        {user}
        """
    
    def delete(self):
        # Delete all relations
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"DELETE FROM Read WHERE id_post = {self.id};"
                    )
                cur.execute(
                    f"DELETE FROM Publicated WHERE id_post = {self.id};", 
                    )
                cur.execute(
                    f"DELETE FROM Posts WHERE id = {self.id};",
                )
                print(f"Deleted {self.show()}")
                self.CONN.commit()
                return 1
        except (Exception, psycopg2.DatabaseError) as error:
            print("Posts error(delete):",error)
            return 0