import psycopg2

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
                self.CONN.commit()
                pych_data = cur.fetchone()
                self.id = pych_data[0]
                print("Relation created:\n", self.show())
            return pych_data
        except (Exception, psycopg2.DatabaseError) as error:
            print("error:",error)
            return None
    
    def create_self(self):
        print("Please insert the following data:")

        # Fornecer lista de id_psychologists para o usuário escolher
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"SELECT * FROM Users WHERE not id = {self.id_user};",
                )
                pych_data = cur.fetchone()

                for i, psych in enumerate(pych_data):
                    print(f" Index = {i} | Name: {psych[3]} {psych[4]} | Username: {psych[5]}")
                
                index = int(input("Choose the index of the Users you want to befriend: \n"))
                while index < 0 or index > len(pych_data):
                    index = int(input("Invalid index. Please choose a valid index: \n"))

        except (Exception, psycopg2.DatabaseError) as error:
            print("error:",error)

        self.id_friend = pych_data[index][0]
    
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
            print("error:",error)

        return f"""
        Me: Id: {user[0]} | Name: {user[3]} {user[4]} | Username: {user[5]}
        Friend: Id: {friend[0]} | Name: {friend[3]} {friend[4]} | Username: {friend[5]}
        """
        


    
