from flask import g
import psycopg
from users import User

class Program:
    def __init__(self, program_num=None, program_name=None, program_description=None, program_status=None):
        self.program_num = program_num
        self.program_name = program_name
        self.program_description = program_description
        self.program_status = program_status
        try:
            self.conn = g.conn
        except RuntimeError:
            self.conn = None

    def set_connection_manually(self, conn):
        self.conn = conn

    def close_connection_manually(self):
        self.conn.close()

    def __repr__(self):
        return f"Program(program_num={self.program_num}, program_name='{self.program_name}', " \
               f"program_description='{self.program_description}', program_status='{self.program_status}')"

    def create(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    INSERT INTO programs (program_name, program_description, program_status)
                    VALUES (%s, %s, %s)
                    RETURNING program_num
                    ''',
                    (self.program_name, self.program_description, self.program_status)
                )
                self.program_num = cur.fetchone()[0]
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error creating program: {e}"

    def fetch(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM programs
                    WHERE program_num = %s OR program_name = %s OR program_status = %s
                    ''',
                    (self.program_num, self.program_name, self.program_status)
                )
                return cur.fetchall()
            except Exception as e:
                self.conn.rollback()
                print(f"Error fetching program: {e}")
                return None

    def auto_fill(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM programs
                    WHERE program_num = %s OR program_name = %s
                    ''',
                    (self.program_num, self.program_name)
                )

                program_data = cur.fetchone()

                if program_data:
                    (self.program_num, self.program_name, self.program_description, self.program_status) = program_data
                    self.conn.commit()
                    return True
                else:
                    print(f"Program with ID {self.program_num} or name {self.program_name} not found.")
                    return False
            except Exception as e:
                self.conn.rollback()
                return f"Error auto-filling program: {e}"

    def update(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    UPDATE programs
                    SET program_name = %s, program_description = %s, program_status = %s
                    WHERE program_num = %s
                    ''',
                    (self.program_name, self.program_description, self.program_status, self.program_num)
                )

                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error updating program: {e}"

    def delete(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    DELETE FROM programs
                    WHERE program_num = %s OR program_name = %s
                    ''',
                    (self.program_num, self.program_name)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error deleting program: {e}"

    def activate_program(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    UPDATE programs
                    SET program_status = %s
                    WHERE program_num = %s
                    ''',
                    ('ACTIVE', self.program_num)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error activating program: {e}"

    def deactivate_program(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    UPDATE programs
                    SET program_status = %s
                    WHERE program_num = %s
                    ''',
                    ('INACTIVE', self.program_num)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error deactivating program: {e}"
    
    def add_user_to_program(self, uin):
        assert isinstance(self.conn, psycopg.Connection)
        userTest = User(uin = uin)
        if (len(userTest.fetch()) == 0):
            return f"Error adding user to program: uin not found"
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    INSERT INTO track (program_num, uin)
                    VALUES (%s, %s)
                    ''',
                    (self.program_num, uin)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error adding user to program: {e}"
