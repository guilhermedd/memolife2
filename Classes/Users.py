import psycopg2

from Relations.Friends import Friends
from Relations.Publicated import Publicated
from Relations.Read import Read

from Classes.Posts import Posts
from Classes.Consultations import Consultations

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
                pych_data = cur.fetchone()
                self.id = pych_data[0]
                print("User created:\n", self.show())
                self.CONN.commit()
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
        return f"""Id: {self.id}
        Name: {self.first} {self.last}
        Username: {self.username}
        """
        
    def add_friend(self):
        friend = Friends(self.id, '', self.CONN)
        available = friend.create_self()
        if available == 0:
            return 1
        if friend.create() is None:
            return 0
        return 1

    def see_friends(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"SELECT * FROM Users WHERE id in (SELECT id_friend FROM Friends WHERE id_user = {self.id});",
                )
                friends = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print("error:",error)
            return None
        return friends
    
    def create_post(self):
        post = Posts('', '', '', '', '', '', self.CONN)
        if not post.create_self():
            return 1
        
        if post.create() is None:
            return 0
        
        if Read(self.id, post.id, self.CONN) is None:
            return 0

        publicated = Publicated(date='', time='', id_user=self.id, id_post=post.id, conn=self.CONN)
        return 1 if publicated.create() is not None else 0

    def check_posts(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"SELECT * FROM Posts WHERE id in (SELECT id_post FROM Publicated WHERE id_user = {self.id});",
                )
                posts = cur.fetchall()
                cur.execute(
                    f"""
                    SELECT COUNT(*) 
                    FROM (
                        SELECT Posts.* 
                        FROM Posts 
                        JOIN Publicated ON Posts.id = Publicated.id_post 
                        WHERE Publicated.id_user = {self.id}
                    ) AS subquery;
                    """
                )
                count = cur.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as error:
            print("error:",error)
            return None
        return posts, count
    
    def check_friends_posts(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"SELECT * FROM Posts WHERE id in (SELECT id_post FROM Publicated WHERE id_user in (SELECT id_friend FROM Friends WHERE id_user = {self.id}));",
                )
                posts = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Users error(check_friends_posts):",error)
            return None
        return posts
    
    def schedule_consultations(self):
        consultation = Consultations(date='', id_user=self.id, id_psychologist='', conn=self.CONN, id='')
        valid = consultation.create_self()
        if valid == 0:
            return 1
        elif valid == None:
            return 0
        if consultation.create() is None:
            return 0
        return 1

    def check_consultations(self):
        try:
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"SELECT * FROM Consultations WHERE id_user = {self.id};",
                )
                consultations = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print("error:",error)
            return None
        return consultations

    def unfriend(self, all = False):
        friendship = Friends(id_user=self.id, id_friend='', conn=self.CONN)
        return friendship.delete(all)

    def delete_post(self, all = False):
        # Have to delete: Read, Publicated, Post
        # Select which post to delete
        posts, _ = self.check_posts()
        if posts:
            if all:
                for post in posts:
                    Posts(
                        id=post[0], 
                        title=post[1],
                        summary=post[2], 
                        content=post[3],
                        feeling=post[4], 
                        date=post[5], 
                        ispublic=post[6], 
                        conn=self.CONN).delete()
                return 1
            else:
                for i, post in enumerate(posts):
                    print("Index: ", i, '\n',
                    Posts(
                        id=post[0], 
                        title=post[1],
                        summary=post[2], 
                        content=post[3],
                        feeling=post[4], 
                        date=post[5], 
                        ispublic=post[6], 
                        conn=self.CONN).show()
                )
                index = int(input("Choose the index of the post you want to delete: \n"))
                while index < 0 or index > len(posts):
                    index = int(input("Invalid index. Please choose a valid index: \n"))
                return Posts(
                        id=posts[index][0],
                        title=posts[index][1],
                        summary=posts[index][2],
                        content=posts[index][3],
                        feeling=posts[index][4],
                        date=posts[index][5],
                        ispublic=posts[index][6],
                        conn=self.CONN
                    ).delete()
        else:
            print("You do not have posts")
            return 0

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
            # To delete User, first have to delete: Post, Friends, Consultations
            # Delete Posts
            while self.check_posts()[1] > 0:
                self.delete_post(all=True)

            # Delete Consultations
            self.delete_consultation(all=True)

            # Delete User from Friends (just in case there are references left)
            self.unfriend(all=True)

            with self.CONN.cursor() as cur:
                cur.execute(
                    "DELETE FROM Friends WHERE id_user = %s OR id_friend = %s;",
                    (self.id, self.id)
                )
                self.CONN.commit()
            
            with self.CONN.cursor() as cur:
                cur.execute(
                    f"DELETE FROM Read WHERE id_user = {self.id};",
                )
                self.CONN.commit()

            # Finally, delete the User
            with self.CONN.cursor() as cur:
                cur.execute(
                    "DELETE FROM Users WHERE id = %s;",
                    (self.id,)
                )
                self.CONN.commit()
                print("User deleted:\n", self.show())
            
            return 1
        except (Exception, psycopg2.DatabaseError) as error:
            print("error:", error)
            return 0

