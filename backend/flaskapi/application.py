from flask import g
import psycopg
from datetime import date

class Application:
    def __init__(self, program_num=None, uin=None, uncom_cert=None, com_cert=None, app_num=None, purpose_statement=None):
        self.app_num = app_num
        self.program_num = program_num
        self.uin = uin
        self.uncom_cert = uncom_cert
        self.com_cert = com_cert
        self.purpose_statement = purpose_statement
        self.app_date = date.today()
        try:
            self.conn = g.conn
        except RuntimeError:
            self.conn = None

    def create(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    INSERT INTO applications (program_num, uin, uncom_cert, com_cert, purpose_statement, app_date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING app_num
                    ''',
                    (self.program_num, self.uin, self.uncom_cert, self.com_cert, self.purpose_statement, self.app_date)
                )
                self.app_num = cur.fetchone()[0]
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error creating application: {e}"

    def update(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    UPDATE applications
                    SET program_num = %s, uin = %s, uncom_cert = %s, com_cert = %s,
                        purpose_statement = %s
                    WHERE app_num = %s
                    ''',
                    (self.program_num, self.uin, self.uncom_cert, self.com_cert, self.purpose_statement, self.app_num)
                )

                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error updating application: {e}"

    def fetch(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM applications
                    WHERE app_num = %s OR program_num = %s OR uin = %s
                    ''',
                    (self.app_num, self.program_num, self.uin)
                )
                return cur.fetchall()
            except Exception as e:
                self.conn.rollback()
                print(f"Error fetching application: {e}")
               
