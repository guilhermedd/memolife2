import psycopg2

from Classes.Psychologists import Psychologists  # 1
from Classes.Users import Users  # 2
from Classes.Posts import Posts  # 3
from Classes.Consultations import Consultations  # 4

from Relations.Friends import Friends  # 5
from Relations.Publicated import Publicated  # 6
from Relations.Read import Read  # 7

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
                instance = Psychologists(id=row[0], name=row[1], email=row[2], password=row[3], conn=CONN)
            elif class_name == 'Users':
                instance = Users(id = row[0], email=row[1], password=row[2], first=row[3], last=row[4], username=row[5], conn=CONN)
            elif class_name == 'Posts':
                instance = Posts(id = row[0], title=row[1], summary=row[2], content=row[3], feeling=row[4], 
                             date=row[5], ispublic=row[6], conn=CONN)
            elif class_name == 'Consultations':
                pass
                # classes.append(Consultations(row[1], row[2], row[3], row[4], row[5], row[6], row[7], CONN))
            instances[row[0]] = instance 
    data[class_name] = instances
    return data 

# List = {"class_name" : {"id": atributes}}
    
table_list = initialize('Users', CONN)

# Admin functions
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
    if not get_all(class_name, CONN):
        return (-1, None)
    try:
        with CONN.cursor() as cur:
            cur.execute(
                f"DELETE FROM {class_name};"
            )
            CONN.commit()
            print(f"Deleted all {class_name}")
            return (0, None)
    except (Exception, psycopg2.DatabaseError) as error:
        print("error:",error)
        return (-1, None)

def insert_one(class_name, CONN):
    table_list = initialize(class_name, CONN)

    if class_name == 'Psychologists':
        instance = Psychologists('', '', '', CONN)
    elif class_name == 'Users':
        instance = Users('', '', '', '', '', CONN)
    elif class_name == 'Posts':
        instance = Posts('', '', '', '', '', '', CONN)

    instance.create_self()
    clear()
    if instance.create() is not None:
        table_list.update({instance.id: instance})
        return (0, instance)
    else:
        return (-1, instance)

# User functions
def add_friend(current_user, CONN):
    return current_user.add_friend()
        
def see_friends(current_user, CONN):
    friends = current_user.see_friends()

    if friends:
        for friend in friends:
            print(
                Users(
                    id=friend[0], 
                    email=friend[1],
                    password=friend[2], 
                    first=friend[3],
                    last=friend[3], 
                    username=friend[3], 
                    conn=CONN).show()
            )

def create_post(current_user, CONN):
    return current_user.create_post()

def check_my_posts(current_user, CONN):
    posts = current_user.check_posts()

    if posts:
        for post in posts:
            print(
                Posts(
                    id=post[0], 
                    title=post[1],
                    summary=post[2], 
                    content=post[3],
                    feeling=post[4], 
                    date=post[5], 
                    ispublic=post[6], 
                    conn=CONN).show()
            )
        return 1
    print("You haven't posted anything yet!")
    return 0

def check_friends_posts(current_user, CONN):
    posts = current_user.check_friends_posts()

    if posts:
        for post in posts:
            print(
                Posts(
                    id=post[0], 
                    title=post[1],
                    summary=post[2], 
                    content=post[3],
                    feeling=post[4], 
                    date=post[5], 
                    ispublic=post[6], 
                    conn=CONN).show()
            )
        return 1
    return 0

def schedule_consultation(current_user, CONN):
    consultation = current_user.schedule_consultation()
    if consultation:
        print(Consultations(id=consultation[0], date=consultation[1], id_user=consultation[2], id_psychologist=consultation[3], conn=CONN).show())
        return 1
    return 0

def check_consultations(current_user, CONN):
    consultations = current_user.check_consultations()
    if consultations:
        for consultation in consultations:
            print(Consultations(id=consultation[0], date=consultation[1], id_user=consultation[2], id_psychologist=consultation[3], conn=CONN).show())
        return 1
    return 0

def unfollow_friend(current_user, CONN):
    return current_user.unfriend()

def delete_post(current_user, CONN):
    return current_user.delete_post()

def unschedule_consultation(current_user, CONN):
    return current_user.unschedule_consultation()

def delete_account(current_user, CONN):
    return current_user.delete_account()

CLASSES = ['Psychologists', 'Users', 'Posts', 'Consultations']
ADMIN_FUNCTIONS = [get_all, delete_all, insert_one]
USER_FUNCTIONS = [
                    add_friend,
                    see_friends, 
                    create_post, 
                    check_my_posts, 
                    check_friends_posts, 
                    schedule_consultation, 
                    check_consultations, 
                    unfollow_friend, 
                    delete_post,
                    unschedule_consultation, 
                    delete_account
                ]

def admin_options(exit_index):
    print("Welcome to Memolife!\n")
    print("---------------------------")
    print("| 1 - Search all integrants of a class")
    print("| 2 - Delete all integrants of a class")
    print("| 3 - Insert one integrant of a class")
    print(f"| {exit_index} - Exit")
    print("---------------------------")

def user_options(exit_index):
    print("Welcome to Memolife!\n")
    print("---------------------------")
    print("| 1 - Add a Friend")
    print("| 2 - See all my Friends")
    print("| 3 - Create a Post")
    print("| 4 - Check my Posts")
    print("| 5 - Check my Friends' Posts")
    print("| 6 - Schedule a Consultation")
    print("| 7 - Check all my Consultations")
    print("| 8 - Unfollow a Friend")
    print("| 9 - Delete a Post")
    print("| 10 - Unschedule a Consultation")
    print("| 11 - Delete my Account")
    print(f"| {exit_index} - Exit")
    print("---------------------------")

def get_profile(class_name, conn, args):
    # args = [email, password]
    try:
        with conn.cursor() as cur:
            cur.execute(
                        f"SELECT * FROM {class_name} WHERE email = '{args[0]}' AND password = '{args[1]}';"
                    )
            data = cur.fetchone()
            table_list = initialize(class_name, CONN)
        return table_list[class_name][data[0]]  # Return user or Psychologist
    except:
        return None

def admin_menu():
    answer_menu = None
    EXIT_INDEX = 4

    while not answer_menu or answer_menu < 1 or answer_menu > EXIT_INDEX:
        admin_options(EXIT_INDEX)

        answer_menu = int(input("\nChoose an option:\n"))
        clear()

    if answer_menu == EXIT_INDEX:
        return -1
    answer = None
    
    # Show all classes
    while not answer:
        for i, class_name in enumerate(CLASSES):
            print(f"{i+1} - {class_name}")
        answer = int(input("\nChoose an option:\n"))
        answer = answer if answer > 0 and answer < 5 else None
        clear()

    # Call the function chosen
    func = ADMIN_FUNCTIONS[answer_menu-1](CLASSES[answer-1], CONN)

    if func[0] == 0:
        print("\nEverything went well!")
    elif func[0] == -1:
        print("There was an error")
    elif func[1] == None:
        print("There is no data to show")
    else:
        for instance in func:
            print(instance.show())

    input("\nPress any key to continue...")

def user_menu(current_user):
    # Pick a option
    answer_menu = None
    EXIT_INDEX = 12

    while not answer_menu or answer_menu < 1 or answer_menu > EXIT_INDEX:
        user_options(EXIT_INDEX)

        answer_menu = int(input("\nChoose an option:\n"))
        clear()

    # Exit
    if answer_menu == EXIT_INDEX:
        return -1

    # Call the function chosen
    func = USER_FUNCTIONS[answer_menu-1](current_user, CONN)

    if func == 1:
        print("\nEverything went well!")
    elif func == 0:
        print("There was an error")
    elif func == None:
        pass

    input("\nPress any key to continue...")

def login(CONN):
    clear()
    print("Welcome to Memolife!\n")
    print("---------------------------")
    print("| 1 - I already have an account")
    print("| 2 - I wish to create an account")
    print(f"| 3 - Exit")
    print("---------------------------")

    option = int(input("\nChoose an option:\n"))

    clear()

    if option == 1:
        class_name = int(input('Do you want to login as:\nUser (1)\nPsychologist (2)\n'))
        while class_name != 1 and class_name != 2:
            class_name = int(input('Do you want to login as:\nUser (1)\nPsychologist (2)\n'))

        class_name = 'Users' if class_name == 1 else 'Psychologists'

        email = input("Email: ")
        password = input("Password: ")

        clear()

        if email == 'admin' and password == 'admin':
            # Admin login

            return (get_profile(class_name, CONN, [email, password]), 1)
        else:
            # User or Psychologist login

            current_user = get_profile(class_name, CONN, [email, password])
            if current_user is None:
                # User not found

                choise = input("User not found... Do you want to try again (1) or create an profile (2)?\n")
                while choise != '1' and choise != '2':
                    choise = input("Incorrect option... Do you want to try again (1) or create an profile (2)?\n")
                if choise == '1':
                    return login(CONN)
                else:
                    option = 2
        
        if current_user is not None:
            # User found

            print("Welcome back!")
            print(current_user.show())

            class_name = 0 if class_name == 'Users' else 1
            return (current_user, class_name)
        else:
            option = 2
        
    if option == 2:
        class_name = int(input('You can create the following account type:\nUser (1)\nPsychologist (2)\n'))

        while class_name != 1 and class_name != 2:
            class_name = int(input('You can create the following account type:\nUser (1)\nPsychologist (2)\n'))
        class_name = 'Users' if class_name == 1 else 'Psychologists'

        return (insert_one(class_name, CONN)[1], 0)
    elif option == 3:
        return None, None

def menu():
    current_user, role = login(CONN)  # role = 0 -> user, role = 1 -> admin

    if role != None:
        print(current_user.show(), role)

    while True:
        clear()

        if role == 1:
            saida = admin_menu()
        elif role == 0:
            saida = user_menu(current_user)
        elif role == 1:
            saida = admin_menu()        

        if current_user == None or saida == -1:
            break


if __name__ == "__main__":
    menu()
    CONN.close()
    


