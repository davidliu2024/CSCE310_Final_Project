from flask import g
import psycopg
from datetime import date

class Application:
    def __init__(self, program_num, uin, uncom_cert=None, com_cert=None,app_num=None,
                 purpose_statement=None):
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

    def set_connection_manually(self, conn):
        self.conn = conn

    def close_connection_manually(self):
        self.conn.close()

    def __repr__(self):
        return f"Application(app_num={self.app_num}, program_num={self.program_num}, uin={self.uin}, " \
               f"uncom_cert='{self.uncom_cert}', com_cert='{self.com_cert}', " \
               f"purpose_statement='{self.purpose_statement}', app_date={self.app_date})"

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
                    (self.program_num, self.uin, self.uncom_cert, self.com_cert,
                     self.purpose_statement, self.app_date)
                )
                self.app_num = cur.fetchone()[0]
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error creating application: {e}"

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
                return None

    def auto_fill(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM applications
                    WHERE app_num = %s OR (program_num = %s AND uin = %s)
                    ''',
                    (self.app_num, self.program_num, self.uin)
                )

                application_data = cur.fetchone()

                if application_data:
                    (self.app_num, self.program_num, self.uin, self.uncom_cert, self.com_cert,
                     self.purpose_statement, self.app_date) = application_data
                    self.conn.commit()
                    return True
                else:
                    print(f"Application with ID {self.app_num} not found.")
                    return False
            except Exception as e:
                self.conn.rollback()
                return f"Error auto-filling application: {e}"

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
                    (self.program_num, self.uin, self.uncom_cert, self.com_cert,
                     self.purpose_statement, self.app_num)
                )

                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error updating application: {e}"

    def delete(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    DELETE FROM applications
                    WHERE app_num = %s OR (program_num = %s AND uin = %s)
                    ''',
                    (self.app_num, self.program_num, self.uin)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error deleting application: {e}"

    def fetch_applications_between_dates(self, start_date, end_date):
        assert isinstance(self.conn, psycopg.Connection)
        assert isinstance(start_date, date)
        assert isinstance(end_date, date)

        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM applications
                    WHERE app_date >= %s AND app_date <= %s
                    ''',
                    (start_date, end_date)
                )
                result = cur.fetchall()
                self.conn.commit()
                return result
            except Exception as e:
                self.conn.rollback()
                return f"Error fetching applications between dates: {e}"

