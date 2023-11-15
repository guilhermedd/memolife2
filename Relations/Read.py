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
                readers = cur.fetchone()
                readers = [reader[0] for reader in readers]
        except (Exception, psycopg2.DatabaseError) as error:
            print("error:",error)
        return readers
    
    def is_post_public(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"SELECT ispublic FROM Posts WHERE id = {self.id_post};",
                )
                posts = cur.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as error:
            print("error:",error)
        return posts[0]
    
    def create(self):  # create a table for  
        # IF post is public, create a read for all friends
        # ELSE create a read for no one
        if self.is_post_public():
            for reader_id in self.get_readers_id():
                try:
                    with self.CONN.cursor() as cur:
                        cur.execute(
                            "INSERT INTO Read (id_user, id_post) VALUES (%s, %s) RETURNING id;",
                            (reader_id, self.id_post)
                        )
                        self.CONN.commit()
                        pych_data = cur.fetchone()
                        self.id = pych_data[0]
                        print("Relation created:\n", self.show())
                    return pych_data
                except (Exception, psycopg2.DatabaseError) as error:
                    print("error:",error)
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
            print("error:",error)
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
            print("error:",error)

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
        


    
