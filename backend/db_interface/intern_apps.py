from flask import g
import psycopg

class InternApplication:
    def __init__(self, uin=None, intern_id=None, app_status=None, app_year=None, ia_num=None):
        self.ia_num = ia_num
        self.uin = uin
        self.intern_id = intern_id
        self.app_status = app_status
        self.app_year = app_year
        try:
            self.conn = g.conn
        except RuntimeError:
            self.conn = None

    def set_connection_manually(self, conn):
        assert isinstance(conn, psycopg.Connection)
        self.conn = conn

    def close_connection_manually(self):
        assert isinstance(self.conn, psycopg.Connection)
        self.conn.close()

    def __repr__(self):
        return f"InternApplication(ia_num={self.ia_num}, uin={self.uin}, intern_id={self.intern_id}, " \
               f"app_status='{self.app_status}', app_year={self.app_year})"

    def create(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    INSERT INTO intern_app (uin, intern_id, app_status, app_year)
                    VALUES (%s, %s, %s, %s)
                    RETURNING ia_num
                    ''',
                    (self.uin, self.intern_id, self.app_status, self.app_year)
                )
                self.ia_num = cur.fetchone()
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error creating intern application: {e}"

    def fetch(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM intern_app
                    WHERE ia_num = %s OR uin = %s OR intern_id = %s
                    ''',
                    (self.ia_num, self.uin, self.intern_id)
                )
                return cur.fetchall()
            except Exception as e:
                self.conn.rollback()
                print(f"Error fetching intern application: {e}")
                return []

    def auto_fill(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM intern_app
                    WHERE ia_num = %s OR (uin = %s AND intern_id = %s)
                    ''',
                    (self.ia_num, self.uin, self.intern_id)
                )

                intern_app_data = cur.fetchone()

                if intern_app_data:
                    (self.ia_num, self.uin, self.intern_id, self.app_status, self.app_year) = intern_app_data
                    self.conn.commit()
                    return True
                else:
                    print(f"Intern Application with ID {self.ia_num} not found.")
                    return False
            except Exception as e:
                self.conn.rollback()
                return f"Error auto-filling intern application: {e}"

    def update(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    UPDATE intern_app
                    SET uin = %s, intern_id = %s, app_status = %s, app_year = %s
                    WHERE ia_num = %s
                    ''',
                    (self.uin, self.intern_id, self.app_status, self.app_year, self.ia_num)
                )

                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error updating intern application: {e}"

    def delete(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    DELETE FROM intern_app
                    WHERE ia_num = %s OR (uin = %s AND intern_id = %s)
                    ''',
                    (self.ia_num, self.uin, self.intern_id)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error deleting intern application: {e}"

    def get_json(self):
        # Create a dictionary with the attributes of the object
        intern_app_dict = {
            "ia_num": self.ia_num,
            "uin": self.uin,
            "intern_id": self.intern_id,
            "app_status": self.app_status,
            "app_year": self.app_year,
        }

        # Convert the dictionary to a JSON-formatted string
        intern_app_json = intern_app_dict

        return intern_app_json
