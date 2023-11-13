import psycopg2

class Users:
    def __init__(self, email, password, first, last, username, conn, id = None):
        self.id             = id
        self.email:str      = email
        self.password:str   = password
        self.first:str      = first
        self.last:str       = last
        self.username:str   = username
        self.CONN           = conn
    
    def create(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    "INSERT INTO Users (email, password, first, last, username) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                    (self.email, self.password, self.first, self.last, self.username)
                )
                cur.execute("SELECT id FROM Users WHERE email = %s AND username = %s;", (self.email, self.username))
                self.id = cur.fetchone()
                user_data = cur.fetchone()
                print("User created: " + user_data)
            return user_data
        except (Exception, psycopg2.DatabaseError) as error:
            return error
    
    def data(self):
        return [self.email, self.password, self.first, self.last, self.username]

    def show(self):
        return f"Id: {self.id} | Email: {self.email} | First Name: {self.first} | Last Name: {self.last} | Username: {self.username}"
        


    
