import csv
import sqlite3

class Logger:
    def __init__(self):
        self.db = sqlite3.connect('db.db')
        self.c = self.db.cursor()
        
        self.c.execute("""CREATE TABLE IF NOT EXISTS whitelist(
            id int,
            username text
            )
            """)

        # Create table with proper columns if not exists
        self.c.execute("""CREATE TABLE IF NOT EXISTS users(
            id text,
            username text,
            trophies int,
            gm int,
            gn int,
            responses int,
            reactions int,
            help int,
            memes int,
            name_trophy int,
            lvl_trophy int,
            msg_reactions text,
            secret_command int,
            secret_word int,  
            private_secret_word int,
            secret_channel_trophy int
            )
            """)
    
    ##############################################################################################################################
    
    def user_exists(self, user_id):
        """Checking if a user is already in the database"""
        
        # Looking for an user with its id
        return bool(self.c.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone())
    
    
    def check(self, count, user_id):
        """Returns a specific count from a user"""
        
        return self.c.execute(f"SELECT {count} FROM users WHERE id = {user_id}").fetchone()
    
    def check_wl(self, user_id):
        """Returns a boolean depending on
        user's WL status"""
        
        return bool(self.c.execute(f"SELECT {user_id} FROM whitelist").fetchone())
    
    def all_trophies(self):
        return self.c.execute("SELECT username, trophies FROM users WHERE trophies > 0").fetchall()
    ##############################################################################################################################
    
    def save_user(self, user_id: int, username: str):
        """Add a user to the database"""
        with self.db:
            # Adding all needed values
            self.c.execute("""INSERT INTO users VALUES (
                :id, 
                :username,
                :trophies,
                :gm,
                :gn,
                :responses,
                :reactions,
                :help,
                :memes,
                :name_trophy,
                :lvl_trophy,       
                :msg_reactions,   
                :secret_command,
                :secret_word,       
                :private_secret_word,
                :secret_channel_trophy
                )""",
                {'id': user_id, 'username': username, 'trophies': 0, 'gm': 0, 'gn': 0,
                 'responses': 0, 'reactions': 0, 'help': 0, 'memes': 0, 'name_trophy': 0,
                 'lvl_trophy': 0, 'msg_reactions': 0, 'secret_command': 0, 'secret_word': 0,  'private_secret_word': 0,
                 'secret_channel_trophy': 0})
        
        print(f'"{username}" added to the database.')
    
    def increment(self, count: str, user_id: int, username: str, value=1):
        """Increment any count from a user."""
         
        if self.user_exists(user_id):
            with self.db:
                # Increment count
                if count in ["msg_reactions"]:
                    self.c.execute(f"UPDATE users SET {count} = {value} WHERE id = {user_id}")
                                        
                else:
                    self.c.execute(f"UPDATE users SET {count} = {count} + {value} WHERE id = {user_id}")
                
                    print(f'{value} "{count}" added to {username}.')
                
            return self.c.execute(f"SELECT {count} FROM users WHERE id = {user_id}").fetchone()
        
        # If user not already in db, adding him and using recursion
        elif not self.user_exists(user_id):
            self.save_user(user_id, username)
            self.increment(count, user_id, username, value)
    
    ##############################################################################################################################
    
    def whitelist(self, user_id: int, username: str):
        with self.db:
            if not self.c.execute(f"SELECT id FROM whitelist WHERE id = {user_id}").fetchone():
                self.c.execute(f"INSERT INTO whitelist VALUES ('{user_id}', '{username}')")
                print(f'"{username}" added to whitelist.')
                return f'**"{username}" added to whitelist.**'
            
            else:
                print(f'"{username}" already registered in WL database.')
                return f'**"{username}" already registered in WL database.**'

    def remove_whitelist(self, user_id: int, username: str):
        with self.db:
            if self.c.execute(f"SELECT id FROM whitelist WHERE id = {user_id}").fetchone():
                self.c.execute(f"DELETE FROM whitelist WHERE id = {user_id}")
                
                print(f'**"{username}" removed from whitelist.**')
                return f'**"{username}" removed from whitelist.**'
            
            else:
                print(f'**"{username}" was not found in WL database.**')
                return f'**"{username}" was not found in WL database.**'
    
    def fetch_whitelisted(self):
        """Create a file with all whitelisted users"""
        res = self.c.execute("SELECT id, username FROM whitelist").fetchall()
        
        if res:
            with open("whitelist.csv", "w", encoding="utf8") as file:
                writer = csv.writer(file, delimiter=',')
                
                for user in res:
                    writer.writerow(user)
            return f"File created.\n\n{len(res)} people are currently whitelisted."
        elif not res:
            return "Nobody is whitelisted at the moment."