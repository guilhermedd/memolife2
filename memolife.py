import psycopg2

from Psychologists import Psychologists  # 1
from Users import Users  # 2
from Posts import Posts  # 3
from Consultations import Consultations  # 4

import os
import traceback

try:
    with open('password.txt', 'r') as file:
        PASSWORD = file.read().splitlines()[0]
        print("Password:", PASSWORD)
# Conectar ao banco de dados PostgreSQL
    CONN = psycopg2.connect(
        host="localhost",
        database="memolife",
        user="postgres",
        password=PASSWORD
    )
except (Exception, psycopg2.DatabaseError) as error:
    print("Ocorreu um erro", error)

def clear():
    if os.name == 'nt':  # Windows
        CLEAR = 'cls'
    else:  # Mac and Linux
        CLEAR = 'clear'
    os.system(CLEAR)

def initialize(class_name, connection):
    data = {}
    instances = {}
    with connection.cursor() as cur:
        cur.execute(
            f"SELECT * FROM {class_name};"
        )
        tables = cur.fetchall()
        for row in tables:
            if class_name == 'Psychologists':
                pass
                # classes.append(Psychologists(row[1], row[2], row[3], row[4], row[5], row[6], row[7], CONN))
            elif class_name == 'Users':
                user = Users(row[1], row[2], row[3], row[4], row[5], CONN, id = row[0])
                instances[row[0]] = user 
            elif class_name == 'Posts':
                pass
                # classes.append(Posts(row[1], row[2], row[3], row[4], row[5], row[6], CONN))
            elif class_name == 'Consultations':
                pass
                # classes.append(Consultations(row[1], row[2], row[3], row[4], row[5], row[6], row[7], CONN))
    data[class_name] = instances
    return data 


# List = {"class_name" : {"id": atributes}}
    
table_list = initialize('Users', CONN)

def create_example(class_name, CONN, number_of_instances):
    for i in range(number_of_instances):
        if class_name == 'Psychologists':
            Psychologists()
        elif class_name == 'Users':
            user = Users(f"email_{i}@gmail.com", f"password_{i}", f"first_name_{i}", f"last_name_{i}", f"username_{i}", CONN)
            user.create()
        elif class_name == 'Posts':
            Posts()
        elif class_name == 'Consultations':
            Consultations()

def get_all(class_name, CONN):  # Return None if not found
    table_list = initialize(class_name, CONN)
    try:
        with CONN.cursor() as cur:
            cur.execute(
                f"SELECT * FROM {class_name};"
            )

            tables = cur.fetchall()	
            ids = [row[0] for row in tables]
            instances = []

            for id in ids:
                instances.append(table_list[class_name][id])

            return instances if instances else None
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
        traceback.print_exc()  # Isso imprime o traceback completo da exceção
        return None

def delete_all(class_name, CONN):  # return -1 if not found
    # if not get_all(class_name):
    #     return -1
    try:
        with CONN.cursor() as cur:
            cur.execute(
                f"DELETE FROM {class_name};"
            )
            CONN.commit()
            print(f"Deleted all {class_name}")
            return 0
    except (Exception, psycopg2.DatabaseError) as error:
        print("error:",error)
        return -1

def insert_one(class_name, CONN):
    table_list = initialize(class_name, CONN)
    if class_name == 'Psychologists':
        Psychologists()
    elif class_name == 'Users':
        user = Users('', '', '', '', '', CONN)
        user.create_self(table_list[class_name])
        clear()
        if user.create() is not None:
            table_list.update({user.id: user})
            return 0
        else:
            return -1
        
CLASSES = ['Psychologists', 'Users', 'Posts', 'Consultations']
FUNCTIONS = [get_all, delete_all, insert_one]

def menu():
    while True:
        clear()
        answer_menu = None
        EXIT_INDEX = 4

        while not answer_menu or answer_menu < 1 or answer_menu > EXIT_INDEX:
            print("Welcome to Memolife!\n")
            print("---------------------------")
            print("| 1 - Search all integrants of a class")
            print("| 2 - Delete all integrants of a class")
            print("| 3 - Insert one integrant of a class")
            print(f"| {EXIT_INDEX} - Exit")
            print("---------------------------")

            answer_menu = int(input("\nChoose an option:\n"))
            clear()

        if answer_menu == EXIT_INDEX:
            return
        answer = None
        
        # Show all classes
        while not answer:
            for i, class_name in enumerate(CLASSES):
                print(f"{i+1} - {class_name}")
            answer = int(input("\nChoose an option:\n"))
            answer = answer if answer > 0 and answer < 5 else None
            clear()

        # Call the function chosen
        func = FUNCTIONS[answer_menu-1](CLASSES[answer-1], CONN)

        if func == None:
            print("There is no data to show")
        elif func == -1:
            print("There was an error")
        elif func == 0:
            print("\nEverything went well!")
        else:
            for instalce in func:
                print(instalce.show())

        input("\nPress any key to continue...")

if __name__ == "__main__":
    menu()
    CONN.close()
    


