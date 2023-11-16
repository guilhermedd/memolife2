import psycopg2

import Classes.Users as Users

class Friends:
    def __init__(self, id_user, id_friend, conn, id = None):
        self.id                 = id
        self.id_user            = id_user
        self.id_friend          = id_friend
        self.CONN               = conn
    
    def create(self):
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
        if friends != None:
            if all:
                for friend in friends:
                    self.id_friend = friend[0]
                    try:
                        with self.CON.cursor() as cur:
                            cur.execute(
                                f"DELETE FROM Friends WHERE id_user = {self.id_user} AND id_friend = {self.id_friend};",
                            )
                            self.CONN.commit()
                            print(f"Deleted {self.show()}")
                    except (Exception, psycopg2.DatabaseError) as error:
                        print("error:",error)
                        return 0
                return 1
            else:
                for i, friend in enumerate(friends):
                    print(f" Index = {i} | Name: {friend[3]} {friend[4]} | Username: {friend[5]}")

                index = int(input("Choose the index of the friend you want to unfriend: \n"))

                while index < 0 or index > len(friends):
                    index = int(input("Invalid index. Please choose a valid index: \n"))

                self.id_friend = friends[index][0]
        
        else:
            print("You do not have friends")
            return 0
        
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"DELETE FROM Friends WHERE id_user = {self.id_user} AND id_friend = {self.id_friend};",
                )
                print(f"Deleted {self.show()}")
                self.CONN.commit()
                return 1
        
        except (Exception, psycopg2.DatabaseError) as error:
            print("Friends error(delete):",error)
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
        Id: {friend[0]} | Name: {friend[3]} {friend[4]} | Username: {friend[5]}
        """    
