import psycopg2

class Psychologists:
    def __init__(self, name, email, password, conn, id = None):
        self.id             = id
        self.name           = name
        self.email:str      = email
        self.password:str   = password
        self.CONN           = conn
    
    def create(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    "INSERT INTO Psychologists (name, email, password) VALUES (%s, %s, %s) RETURNING id;",
                    (self.name, self.email, self.password)
                )
                self.CONN.commit()
                user_data = cur.fetchone()
                self.id = user_data[0]
            print("Psychologist created:\n", self.show())
            return user_data
        except (Exception, psycopg2.DatabaseError) as error:
            print("error:",error)
            return None
    
    def create_self(self, psychologists_list):
        print("Please insert the following data:")

        emails_taken = [psycho.email for psycho in psychologists_list.values()]
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

        name = input("Complete Name (Maximum of 20 characters): \n")
        while len(name) > 20 or len(name) < 3 or len(name.split(' ')) < 2:
            if len(name) > 20:
                name = input("Name is too long (Maximum of 20 characters): \n")
            elif len(name) < 3:
                name = input("Name is too short (Minimum of 3 characters): \n")
            elif len(name.split(' ')) < 2:
                name = input("Please enter your complete name: \n")
        name = name.title()
        self.email      = email
        self.password   = password
        self.name       = name
    
    def data(self):
        return [self.email, self.password, self.name]

    def show(self):
        return f"Id: {self.id} | Email: {self.email} | Complete Name: {self.name}"
        


    
