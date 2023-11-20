import psycopg2

import Classes.Users as Users

class Friends:
    def __init__(self, id_user, id_friend, conn, id = None):
        self.id                 = id
        self.id_user            = id_user
        self.id_friend          = id_friend
        self.CONN               = conn
    
    def create(self):
        with open('password.txt', 'r') as file:
            PASSWORD = file.read().splitlines()[0]
# Conectar ao banco de dados PostgreSQL
        self.CONN = psycopg2.connect(
            host="localhost",
            database="memolife",
            user="postgres",
            password=PASSWORD
        )
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    "INSERT INTO Friends (id_user, id_friend) VALUES (%s, %s) RETURNING id;",
                    (self.id_user, self.id_friend)
                )

                pych_data = cur.fetchone()
                self.id = pych_data[0]

                print("Relation created:\n", self.show())
                self.CONN.commit()
            return pych_data
        except (Exception, psycopg2.DatabaseError) as error:
            print("Friends error(create):",error)
            return None
    
    def create_self(self):

        # Fornecer lista de id_psychologists para o usuário escolher
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"""SELECT * FROM users WHERE id <> {self.id_user} AND id NOT IN 
                        (SELECT id_friend FROM Friends WHERE id_user = {self.id_user})
                    """,
                )
                pych_data = cur.fetchall()

                if not pych_data:
                    print("There are no other users to befriend.")
                    return 0
                
                print("Please insert the following data:")

                for i, psych in enumerate(pych_data):
                    print(f" Index = {i} | Name: {psych[3]} {psych[4]} | Username: {psych[5]}")
                print(" Index = -1 | Exit")
                
                index = int(input("Choose the index of the Users you want to befriend: \n"))
                while index < -1 or index >= len(pych_data):
                    index = int(input("Choose the index of the Users you want to befriend:\n"))
                
                if index == -1:
                    return 0

                self.id_friend = pych_data[index][0]
                return 1
        except (Exception, psycopg2.DatabaseError) as error:
            print("Friends error(create):",error)
            return 0
   
    def get_friends(self):
        # Return a list of friends(Users)
        try:
            with self.CONN.cursor() as cur:
                cur.execute(f"SELECT * FROM Users WHERE id IN (SELECT id_friend FROM Friends WHERE id_user = {self.id_user});")
                friends = cur.fetchall()
                return friends
        except (Exception, psycopg2.DatabaseError) as error:
            print("Friends error(create_self):",error)
            return None

    def delete(self, all):
        friends = self.get_friends()
        if friends:
            try:
                with self.CONN.cursor() as cur:
                    if all:
                        cur.execute(
                            f"DELETE FROM Friends WHERE id_user = {self.id_user} OR id_friend = {self.id_user};"
                        )
                        print(f"Deleted friends")
                    else:
                        for i, friend in enumerate(friends):
                            print(f" Index = {i} | Name: {friend[3]} {friend[4]} | Username: {friend[5]}")

                        index = int(input("Choose the index of the friend you want to unfriend: \n"))

                        while index < 0 or index >= len(friends):
                            index = int(input("Invalid index. Please choose a valid index: \n"))

                        self.id_friend = friends[index][0]

                        cur.execute(
                            f"DELETE FROM Friends WHERE id_user = {self.id_user} AND id_friend = {self.id_friend};"
                        )
                        print(f"Deleted friend for {self.show()}")
                    
                    self.CONN.commit()
                    return 1

            except (Exception, psycopg2.DatabaseError) as error:
                print("Friends error(delete):", error)
                return 0

        else:
            print("You do not have friends")
            return 0


        
    def show(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"SELECT * FROM Users WHERE id = {self.id_user};",
                )
                user = cur.fetchone()
                cur.execute(
                    f"SELECT * FROM Users WHERE id = {self.id_friend};",
                )
                friend = cur.fetchone()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Friends error(show):",error)

        return f"""
        User
        Id: {user[0]}
        Name: {user[3]} {user[4]}
        Username: {user[5]}
        -------------------
        Friend:
        Id: {friend[0]}
        Name: {friend[3]} {friend[4]}
        Username: {friend[5]}
        """    
