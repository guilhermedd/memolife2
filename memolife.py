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


if os.name == 'nt':  # Windows
    CLEAR = 'cls'
else:  # Mac and Linux
    CLEAR = 'clear'

def clear():
    os.system(CLEAR)

def initialize(class_name, connection):
    list = {}
    with connection.cursor() as cur:
        cur.execute(
            f"SELECT * FROM {class_name};"
        )
        tables = cur.fetchall()
        print(tables)
        classes = []
        for row in tables:
            if class_name == 'Psychologists':
                classes.append(Psychologists(row[1], row[2], row[3], row[4], row[5], row[6], row[7], CONN))
            elif class_name == 'Users':
                user = Users(row[1], row[2], row[3], row[4], row[5], CONN)
                classes.append(user)
                list.update({user.id: user})  
            elif class_name == 'Posts':
                classes.append(Posts(row[1], row[2], row[3], row[4], row[5], row[6], CONN))
            elif class_name == 'Consultations':
                classes.append(Consultations(row[1], row[2], row[3], row[4], row[5], row[6], row[7], CONN))
    return list 

users_list = initialize('Users', CONN)

def get_all(class_name, CONN):  # Return None if not found
    try:
        with CONN.cursor() as cur:
            cur.execute(
                f"SELECT * FROM {class_name};"
            )
            tables = cur.fetchall()	
            print("tables:", tables)
            ids = [row[0] for row in tables]
            instances = []
            print("ids:", ids, "| Users List: ", users_list)
            for id in ids:
                instances.append(users_list[id])
            print("instances:", instances)

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
            print(f"Deleted all {class_name}")
            return 0
    except (Exception, psycopg2.DatabaseError) as error:
        print("error:",error)
        return -1

def insert_one(class_name, CONN):
    if class_name == 'Psychologists':
        Psychologists()
    elif class_name == 'Users':
        print("Please insert the following data:")
        email = input("Email(Maximum of 50 characters): \n")
        password = input("Password(Maximum of 50 characters): \n ")
        first = input("First name(Maximum of 20 characters): \n ")
        last = input("Last name(Maximum of 50 characters): \n ")
        username = input("Username(Maximum of 20 characters): \n ")
        USER = Users(email, password, first, last, username, CONN)
        USER.create()
        clear()
        print(USER.show())
        if USER:
            users_list.update({USER.id: USER})
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
        
        while not answer:
            for i, class_name in enumerate(CLASSES):
                print(f"{i+1} - {class_name}")
            answer = int(input("\nChoose an option:\n"))
            answer = answer if answer > 0 and answer < 5 else None
            clear()

        func = FUNCTIONS[answer_menu-1](CLASSES[answer-1], CONN)

        if not func:
            print("There is no data to show")
        elif func == -1:
            print("There was an error")
        elif func == 0:
            pass
        else:
            for instalce in func:
                instalce.show()

        input("\nPress any key to continue...")

if __name__ == "__main__":
    menu()
    CONN.close()
    


