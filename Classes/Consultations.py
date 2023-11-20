import psycopg2
import datetime

class Consultations:
    def __init__(self, date, id_user, id_psychologist, conn, id = None):
        self.id                 = id
        self.date               = date
        self.id_user            = id_user
        self.id_psychologist    = id_psychologist
        self.CONN               = conn
    
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
                    "INSERT INTO Consultations (date, id_user, id_psychologist) VALUES (%s, %s, %s) RETURNING id;",
                    (self.date, self.id_user, self.id_psychologist)
                )
                pych_data = cur.fetchone()
                self.id = pych_data[0]
                print("User created:\n", self.show())
                self.CONN.commit()
            return pych_data
        except (Exception, psycopg2.DatabaseError) as error:
            print("Consultation error(Create):",error)
            return None
    
    def create_self(self):
        # Fornecer lista de id_psychologists para o usuário escolher
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    "SELECT * FROM Psychologists;",
                )
                pych_data = cur.fetchall()

                if not pych_data:
                    print("There are no psychologists to choose from.")
                    return 0

                print("Please insert the following data:")
                
                for i, psych in enumerate(pych_data):
                    print(f" Index = {i} | Id: {psych[0]} | Name: {psych[1]}")
                
                index = int(input("Choose the index of the psychologist you want to consult: \n"))
                while index < 0 or index > len(pych_data):
                    index = int(input("Invalid index. Please choose a valid index: \n"))
        except (Exception, psycopg2.DatabaseError) as error:
            print("Consultation error(create_self):",error)
            return 0
        
        while True:

            # Tentar converter a string da data para um objeto datetime
            date_str = input("Enter the date in the format DD/MM/YYYY (e.g., 14/11/2023): \n")
            try:
                user_provided_date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
                user_provided_date = user_provided_date.date()
                break # Se a conversão for bem-sucedida, sair do loop
            except ValueError:
                print("Invalid date format. Please use the format DD/MM/YYYY.")
                continue # Se houver um erro, continue solicitando a data

        # If the psychologist has more than 5 consultations that day, ask for another date
        while True:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"SELECT COUNT(*) FROM Consultations WHERE id_psychologist = {pych_data[index][0]} AND date = '{user_provided_date}';",
                )
                count = cur.fetchone()[0]
                if count >= 5:
                    print(f"This psychologist has {count} consultations that day, which is more than 5. Please choose another date.")
                    continue
                else:
                    print(f"This psychologist has {count} consultations that day. This date is available!")
                    self.date               = user_provided_date
                    self.id_psychologist = pych_data[index][0]
                    break

        return 1
    
    def data(self):
        return [self.email, self.password, self.first, self.last, self.username]

    def get_psychologists(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"SELECT * FROM Psychologists WHERE id = {self.id_psychologist};",
                )
                pych_data = cur.fetchone()
        except (Exception, psycopg2.DatabaseError) as error:
            print("error:",error)
            return []
        return pych_data

    def get_user(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"SELECT * FROM Users WHERE id = {self.id_user};",
                )
                user = cur.fetchone()
                return user
        except (Exception, psycopg2.DatabaseError) as error:
            print("error:",error)
            return []

    def delete(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"DELETE FROM Consultations WHERE id = {self.id};",
                )
                self.CONN.commit()
                print(f"Deleted {self.show()}")
                return 1
        except (Exception, psycopg2.DatabaseError) as error:
            print("error:",error)
            return 0
        
    def show(self):
        psych = self.get_psychologists()
        user = self.get_user()

        return f"""Id: {self.id}
        Psychologist: 
        Id: {psych[0]}
        Name: {psych[1]}
        -----------------
        Patient:
        Id: {user[0]}
        Name: {user[3]} {user[4]}
        Username: {user[5]}
        -----------------
        Date: {self.date.strftime("%d/%m/%Y")}
        """


    
