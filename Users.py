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
                self.CONN.commit()
                cur.execute("SELECT * FROM Users WHERE email = %s AND username = %s;", (self.email, self.username))
                user_data = cur.fetchone()
                self.id = user_data[0]

            print("User created:\n", self.show())
            return user_data
        except (Exception, psycopg2.DatabaseError) as error:
            return error
    
    def create_self(self, users_list):
        print("Please insert the following data:")

        emails_taken = [user.email for user in users_list.values()]
        email = input("Email (Maximum of 50 characters): \n")
        while len(email) > 50 or '@' not in email or email in emails_taken:
            if len(email) > 50:
                email = input("Email is too long (Maximum of 50 characters): \n")
            elif '@' not in email:
                email = input("Please enter a valid email address: \n")
            elif email in emails_taken:
                email = input("Email already taken: \n")

        password = input("Password (Maximum of 50 characters): \n")
        while len(password) > 50:
            password = input("Password is too long (Maximum of 50 characters): \n")

        first = input("First name (Maximum of 20 characters): \n")
        while len(first) > 20:
            first = input("First name is too long (Maximum of 20 characters): \n")
        first = first.capitalize()

        last = input("Last name(s) (Maximum of 50 characters): \n")
        while len(last) > 50:
            last = input("Last name is too long (Maximum of 50 characters): \n")
        last = ' '.join(name.capitalize() for name in last.split())

        usernames_taken = [user.username for user in users_list.values()]
        username = input("Username (Maximum of 20 characters): \n")
        while len(username) > 20 or username in usernames_taken:
            if len(username) > 20:
                username = input("Username is too long (Maximum of 20 characters): \n")
            elif username in usernames_taken:
                username = input("Username already taken: \n")
        
        self.email      = email
        self.password   = password
        self.first      = first
        self.last       = last
        self.username   = username
    
    def data(self):
        return [self.email, self.password, self.first, self.last, self.username]

    def show(self):
        return f"Id: {self.id} | Email: {self.email} | First Name: {self.first} | Last Name: {self.last} | Username: {self.username}"
        


    
