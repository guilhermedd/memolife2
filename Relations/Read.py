import psycopg2

class Read:
    def __init__(self, id_user, id_post, conn, id = None):
        self.id                 = id
        self.id_user            = id_user
        self.id_post            = id_post
        self.CONN               = conn
        self.create()
    
    def get_readers_id(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"SELECT id FROM Users;",
                )
                readers = cur.fetchall()
                readers = [reader[0] for reader in readers]
        except (Exception, psycopg2.DatabaseError) as error:
            print("Read error(get_readers_id):",error)
        return readers
    
    def is_post_public(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"SELECT ispublic FROM Posts WHERE id = {self.id_post};",
                )
                result = cur.fetchall()

                if result is not None:  # Check if the result is not None
                    return result[0]  # Return the first column value if available
                else:
                    return False  # Assuming the post is not public if there is no result
        except (Exception, psycopg2.DatabaseError) as error:
            print("Read error(is_post_public):", error)
            return False  # Return False in case of an error
  
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
        if self.is_post_public():
            for reader_id in self.get_readers_id():
                try:
                    with self.CONN.cursor() as cur:
                        cur.execute(
                            "INSERT INTO Read (id_user, id_post) VALUES (%s, %s) RETURNING id;",
                            (reader_id, self.id_post)
                        )
                        pych_data = cur.fetchone()
                        self.id = pych_data[0]
                        print("Read relation created:\n")
                        self.show()
                        self.CONN.commit()
                    return pych_data
                except (Exception, psycopg2.DatabaseError) as error:
                    print("Read error(create):", error)
                    return None
        else:
            print("Post is not public. No Read relation created.")
            return None

    def delete(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"DELETE FROM Read WHERE id = {self.id};",
                )
                self.CONN.commit()
                print(f"Deleted {self.show()}")
                return 0
        except (Exception, psycopg2.DatabaseError) as error:
            print("Read error(Delete):",error)
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
                friend = cur.fetchone()

        except (Exception, psycopg2.DatabaseError) as error:
            return ("Read error(Show):")


        return f"""
        Me: Id: {user[0]} | Name: {user[3]} {user[4]} | Username: {user[5]}
        Friend: Id: {friend[0]}
        Title: {friend[3]} 
        -------------------
        Summary: 
        {friend[4]}
        --------------------
        Date: {friend[5]}
        """
        


    
