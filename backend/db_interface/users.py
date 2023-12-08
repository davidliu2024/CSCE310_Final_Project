from flask import g
import psycopg
from db_interface.programs import Program

class User:
    def __init__(self, uin = None, first_name = None, last_name = None, username = None, password = None, user_type = None, email = None, discord_name = None, m_initial = None):
        self.uin = uin
        self.first_name = first_name
        self.m_initial = m_initial
        self.last_name = last_name
        self.username = username
        self.password = password
        self.user_type = user_type
        self.email = email
        self.discord_name = discord_name
        try:
            self.conn = g.conn
        except RuntimeError:
            self.conn = None

    def clear(self):
        self.uin = None
        self.first_name = None
        self.m_initial = None
        self.last_name = None
        self.username = None
        self.password = None
        self.user_type = None
        self.email = None
        self.discord_name = None 
    
    def setConnectionManually(self, conn):
        self.conn = conn
    
    def closeConnectionManually(self):
        assert isinstance(self.conn, psycopg.Connection)
        self.conn.close()

    def __repr__(self):
        return f"User(uin={self.uin}, first_name='{self.first_name}', m_initial='{self.m_initial}', " \
               f"last_name='{self.last_name}', username='{self.username}', password='{self.password}', " \
               f"user_type={self.user_type}, email='{self.email}', discord_name='{self.discord_name}')"
    
    def create(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    INSERT INTO users (first_name, last_name, username, passwords, user_type, email, discord_name, m_initial)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ''',
                    (self.first_name, self.last_name, self.username, self.password, self.user_type, self.email, self.discord_name, self.m_initial)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error creating user: {e}"
    
    def fetch(self) -> list:
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                '''
                SELECT * FROM users
                WHERE uin = %s OR username = %s OR (first_name = %s AND last_name = %s)
                ''',
                    (self.uin, self.username, self.first_name, self.last_name)
                )
                self.conn.commit()
                return cur.fetchall()
            except Exception as e:
                self.conn.rollback()
                print(f"Error fetching user: {e}")
                return []
    
    def isAdmin(self):
        self.autoFill()
        return True if self.user_type == 'ADMIN' else False
    
    def makeAdmin(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    UPDATE users
                    SET user_type = %s
                    WHERE uin = %s
                    ''',
                    ('ADMIN', self.uin)
                )
                self.conn.commit()
                self.user_type = 'ADMIN'
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error making user admin: {e}"

    def removeAdmin(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    UPDATE users
                    SET user_type = %s
                    WHERE uin = %s
                    ''',
                    ('USER', self.uin)
                )
                self.conn.commit()
                self.user_type = 'USER'
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error removing user admin status: {e}"
    
    def deactivate_user(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    UPDATE users
                    SET user_type = %s
                    WHERE uin = %s
                    ''',
                    ('DEACTIVATED', self.uin)
                )
                self.conn.commit()
                self.user_type = 'DEACTIVATED'
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error removing user admin status: {e}"
    
    def activate_user(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    UPDATE users
                    SET user_type = %s
                    WHERE uin = %s
                    ''',
                    ('USER', self.uin)
                )
                self.conn.commit()
                self.user_type = 'USER'
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error removing user admin status: {e}"


    def autoFill(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM users
                    WHERE uin = %s OR username = %s
                    ''',
                    (self.uin, self.username)
                )
                
                user_data = cur.fetchone()  # Assuming you want to fetch only one user
                
                if user_data:
                    # Assuming user_data is a tuple representing a row in the 'users' table
                    self.uin, self.first_name, self.m_initial, self.last_name, self.username, self.password, self.user_type, self.email, self.discord_name = user_data
                    self.conn.commit()
                    return True
                else:
                    print(f"User with UIN {self.uin} not found.")
                    return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error auto-filling user: {e}"

    def update(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    UPDATE users
                    SET first_name = %s, last_name = %s, username = %s, passwords = %s, user_type = %s, email = %s, discord_name = %s, m_initial = %s
                    WHERE uin = %s
                    ''',
                    (self.first_name, self.last_name, self.username, self.password, self.user_type, self.email, self.discord_name, self.m_initial, self.uin)
                )
                
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error updating user: {e}"

    def delete(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    DELETE FROM users
                    WHERE uin=%s
                    ''',
                    (self.uin,)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error deleting user: {e}"
    
    def get_user_programs(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM track
                    WHERE uin=%s
                    ''',
                    (self.uin,)
                )
                data = cur.fetchall()
                
                self.conn.commit()

                return 
            except Exception as e:
                self.conn.rollback()
                return f"Error getting user programs: {e}"

    def add_user_to_program(self, program_num):
        assert isinstance(self.conn, psycopg.Connection)
        programTest = Program(program_num = program_num)
        programTest.auto_fill()
        if programTest.program_status == "INACTIVE":
            return "Error adding user to program: Program inactive"
        if (len(programTest.fetch()) == 0):
            return f"Error adding user to program: program_num not found"
        
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    INSERT INTO track (program_num, uin)
                    VALUES (%s, %s)
                    ''',
                    (program_num, self.uin)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error adding user to program: {e}"
    
    def remove_user_from_program(self, program_num):
        assert isinstance(self.conn, psycopg.Connection)

        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    DELETE FROM track
                    WHERE uin = %s AND program_num = %s
                    ''',
                    (self.uin, program_num)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error removing user from program: {e}"
            
    def add_user_to_event(self, event_id):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    INSERT INTO event_tracking (event_id, uin)
                    VALUES (%s, %s)
                    ''',
                    (event_id, self.uin)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error adding user to event: {e}"

    def remove_user_from_event(self, event_id):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    DELETE FROM event_tracking
                    WHERE uin = %s AND event_id = %s
                    ''',
                    (self.uin, event_id)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error removing user from event: {e}"
    
    def getJSON(self):
        user_dict = {
            "uin": self.uin,
            "first_name": self.first_name,
            "m_initial": self.m_initial,
            "last_name": self.last_name,
            "username": self.username,
            "password": self.password,
            "user_type": self.user_type,
            "email": self.email,
            "discord_name": self.discord_name
        }
        return user_dict


