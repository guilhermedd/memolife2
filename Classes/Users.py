import psycopg2

class Users:
    def __init__(self, email, password, first, last, username, conn, id = None):
        self.id             = id
        self.email          = email
        self.password       = password
        self.first          = first
        self.last           = last
        self.username       = username
        self.CONN           = conn
    
    def create(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    "INSERT INTO Users (email, password, first, last, username) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                    (self.email, self.password, self.first, self.last, self.username)
                )
                self.CONN.commit()
                pych_data = cur.fetchone()
                self.id = pych_data[0]
                print("User created:\n", self.show())
            return pych_data
        except (Exception, psycopg2.DatabaseError) as error:
            print("error:",error)
            return None
    
    def get_users_emails(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"SELECT email FROM Users WHERE not id = {self.id};",
                )
                users_list = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print("error:",error)
        return users_list

    def create_self(self):
        print("Please insert the following data:")

        users_list = self.get_users_emails()

        emails_taken = [email[0] for email in users_list]
        email = input("Email (Maximum of 50 characters): \n")
        while len(email) > 50 or len(email) < 3 or '@' not in email or email in emails_taken:
            if len(email) > 50:
                email = input("Email is too long (Maximum of 50 characters): \n")
            elif '@' not in email:
                email = input("Please enter a valid email address: \n")
            elif email in emails_taken:
                email = input("Email already taken: \n")
            elif len(email) < 3:
                email = input("Email is too short (Minimum of 3 characters): \n")

        password = input("Password (Maximum of 50 characters): \n")
        while len(password) > 50 or len(password) < 3:
            if len(password) > 50:
                password = input("Password is too long (Maximum of 50 characters): \n")
            elif len(password) < 3:
                password = input("Password is too short (Minimum of 3 characters): \n")

        first = input("First name (Maximum of 20 characters): \n")
        while len(first) > 20 or len(first) < 3:
            if len(first) > 20:
                first = input("First name is too long (Maximum of 20 characters): \n")
            elif len(first) < 3:
                first = input("First name is too short (Minimum of 3 characters): \n")
        first = first.title()

        last = input("Last name(s) (Maximum of 50 characters): \n")
        while len(last) > 50 or len(last) < 3:
            if len(last) > 50:
                last = input("Last name is too long (Maximum of 50 characters): \n")
            elif len(last) < 3:
                last = input("Last name is too short (Minimum of 3 characters): \n")
        last = last.title()

        usernames_taken = [user.username for user in users_list.values()]
        username = input("Username (Maximum of 20 characters): \n")
        while len(username) > 20 or username in usernames_taken or len(username) < 3:
            if len(username) > 20:
                username = input("Username is too long (Maximum of 20 characters): \n")
            elif username in usernames_taken:
                username = input("Username already taken: \n")
            elif len(username) < 3:
                username = input("Username is too short (Minimum of 3 characters): \n")
        
        self.email      = email
        self.password   = password
        self.first      = first
        self.last       = last
        self.username   = username
    
    def data(self):
        return [self.email, self.password, self.first, self.last, self.username]

    def show(self):
        return f"Id: {self.id} | Email: {self.email} | First Name: {self.first} | Last Name: {self.last} | Username: {self.username}"
        
    def delete(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    "DELETE FROM Users WHERE id = %s;",
                    (self.id,)
                )
                self.CONN.commit()
                print("User deleted:\n", self.show())
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print("error:",error)
            return False

    
