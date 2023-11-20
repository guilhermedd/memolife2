import psycopg2

from Classes.Consultations import Consultations

class Psychologists:
    def __init__(self, name, email, password, conn, id = None):
        self.id             = id
        self.name           = name
        self.email:str      = email
        self.password:str   = password
        self.CONN           = conn
    
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
    
    def get_psychologists_emails(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"SELECT email FROM Psychologists WHERE not id = {self.id};",
                )
                psychologists_list = cur.fetchall()
            return psychologists_list
        except (Exception, psycopg2.DatabaseError) as error:
            return []

    def create_self(self):
        print("Please insert the following data:")

        psychologists_list = self.get_psychologists_emails()

        emails_taken = [email[0] for email in psychologists_list]
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
        
    def check_consultations(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"SELECT * FROM Consultations WHERE id_psychologist = {self.id};",
                )
                consultations = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print("error:",error)
            return None
        return consultations

    def delete_consultation(self, all = False):
        consultations = self.check_consultations()

        if consultations:
            if all:
                for consultation in consultations:
                    Consultations(
                        id=consultation[0], 
                        date=consultation[1],
                        id_user=consultation[2],
                        id_psychologist=consultation[3],
                        conn=self.CONN).delete()
                return 1
            else:
                for i, consultation in enumerate(consultations):
                    print("Index: ", i, '\n',
                    Consultations(
                        id=consultation[0], 
                        date=consultation[1],
                        id_user=consultation[2],
                        id_psychologist=consultation[3],
                        conn=self.CONN).show()
                )
                
                index = int(input("Choose the index of the consultation you want to delete: \n"))
                while index < 0 or index > len(consultations):
                    index = int(input("Invalid index. Please choose a valid index: \n"))
                
                return Consultations(
                        id=consultations[index][0], 
                        date=consultations[index][1],
                        id_user=consultations[index][2],
                        id_psychologist=consultations[index][3],
                        conn=self.CONN).delete()
        else:
            print("You do not have consultations")
            return 1

    def delete_account(self):
        try:
            # Delete Consultations
            self.delete_consultation(all=True)

            # Finally, delete the User
            with self.CONN.cursor() as cur:
                cur.execute(
                    "DELETE FROM Psychologists WHERE id = %s;",
                    (self.id,)
                )
                self.CONN.commit()
                print("User deleted:\n", self.show())
            
            return 1
        except (Exception, psycopg2.DatabaseError) as error:
            print("error:", error)
            return 0


    
