from flask import g
import psycopg

class ClassEnrollment:
    def __init__(self, ce_num=None, uin=None, class_id=None, class_status=None, semester=None, class_year=None):
        self.ce_num = ce_num
        self.uin = uin
        self.class_id = class_id
        self.class_status = class_status
        self.semester = semester
        self.class_year = class_year
        try:
            self.conn = g.conn
        except RuntimeError:
            self.conn = None

    def set_connection_manually(self, conn):
        self.conn = conn

    def close_connection_manually(self):
        self.conn.close()

    def __repr__(self):
        return f"ClassEnrollment(ce_num={self.ce_num}, uin={self.uin}, class_id={self.class_id}, " \
               f"class_status='{self.class_status}', semester='{self.semester}', class_year={self.class_year})"

    def create(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    INSERT INTO class_enrollment (uin, class_id, class_status, semester, class_year)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING ce_num
                    ''',
                    (self.uin, self.class_id, self.class_status, self.semester, self.class_year)
                )
                self.ce_num = cur.fetchone()[0]
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error creating class enrollment: {e}"

    def fetch(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM class_enrollment
                    WHERE ce_num = %s OR uin = %s OR class_id = %s OR semester = %s OR class_year = %s
                    ''',
                    (self.ce_num, self.uin, self.class_id)
                )
                return cur.fetchall()
            except Exception as e:
                self.conn.rollback()
                print(f"Error fetching class enrollment: {e}")
                return None

    def auto_fill(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM class_enrollment
                    WHERE ce_num = %s OR (uin = %s AND class_id = %s)
                    ''',
                    (self.ce_num, self.uin, self.class_id)
                )

                enrollment_data = cur.fetchone()

                if enrollment_data:
                    (self.ce_num, self.uin, self.class_id, self.class_status, self.semester, self.class_year) = enrollment_data
                    self.conn.commit()
                    return True
                else:
                    print(f"Class enrollment with ID {self.ce_num} or UIN {self.uin} or class ID {self.class_id} not found.")
                    return False
            except Exception as e:
                self.conn.rollback()
                return f"Error auto-filling class enrollment: {e}"

    def update(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    UPDATE class_enrollment
                    SET uin = %s, class_id = %s, class_status = %s, semester = %s, class_year = %s
                    WHERE ce_num = %s
                    ''',
                    (self.uin, self.class_id, self.class_status, self.semester, self.class_year, self.ce_num)
                )

                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error updating class enrollment: {e}"

    def delete(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    DELETE FROM class_enrollment
                    WHERE ce_num = %s OR uin = %s OR class_id = %s
                    ''',
                    (self.ce_num, self.uin, self.class_id)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error deleting class enrollment: {e}"
