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
            with self.CONN.cursor() as cur:
                cur.execute(
                    "INSERT INTO Consultations (date, id_user, id_psychologist) VALUES (%s, %s, %s) RETURNING id;",
                    (self.date, self.id_user, self.id_psychologist)
                )
                self.CONN.commit()
                pych_data = cur.fetchone()
                self.id = pych_data[0]
                print("User created:\n", self.show())
            return pych_data
        except (Exception, psycopg2.DatabaseError) as error:
            print("error:",error)
            return None
    
    def create_self(self):
        print("Please insert the following data:")

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

        # Fornecer lista de id_psychologists para o usuário escolher
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    "SELECT * FROM Psychologists;",
                )
                pych_data = cur.fetchone()

                for i, psych in enumerate(pych_data):
                    print(f" Index = {i} | Id: {psych[0]} | Name: {psych[1]}")
                
                index = int(input("Choose the index of the psychologist you want to consult: \n"))
                while index < 0 or index > len(pych_data):
                    index = int(input("Invalid index. Please choose a valid index: \n"))

        except (Exception, psycopg2.DatabaseError) as error:
            print("error:",error)

        self.date               = user_provided_date
        self.id_psychologist = pych_data[index][0]
    
    def data(self):
        return [self.email, self.password, self.first, self.last, self.username]

    def show(self):
        return f"Id: {self.id} | Email: {self.email} | First Name: {self.first} | Last Name: {self.last} | Username: {self.username}"
        


    
