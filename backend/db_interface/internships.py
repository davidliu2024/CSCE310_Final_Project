from flask import g
import psycopg

class Internship:
    def __init__(self, intern_id=None, internship_name=None, internship_description=None, is_gov=None):
        self.intern_id = intern_id
        self.internship_name = internship_name
        self.internship_description = internship_description
        self.is_gov = is_gov
        try:
            self.conn = g.conn
        except RuntimeError:
            self.conn = None

    def set_connection_manually(self, conn):
        self.conn = conn

    def close_connection_manually(self):
        self.conn.close()

    def __repr__(self):
        return f"Internship(intern_id={self.intern_id}, internship_name='{self.internship_name}', " \
               f"internship_description='{self.internship_description}', is_gov={self.is_gov})"

    def create(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    INSERT INTO internship (internship_name, internship_description, is_gov)
                    VALUES (%s, %s, %s)
                    RETURNING intern_id
                    ''',
                    (self.internship_name, self.internship_description, self.is_gov)
                )
                self.intern_id = cur.fetchone()[0]
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error creating internship: {e}"

    def fetch(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM internship
                    WHERE intern_id = %s OR internship_name = %s OR is_gov = %s
                    ''',
                    (self.intern_id, self.internship_name, self.is_gov)
                )
                return cur.fetchall()
            except Exception as e:
                self.conn.rollback()
                print(f"Error fetching internship: {e}")
                return None

    def auto_fill(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM internship
                    WHERE intern_id = %s OR internship_name = %s
                    ''',
                    (self.intern_id, self.internship_name)
                )

                internship_data = cur.fetchone()

                if internship_data:
                    (self.intern_id, self.internship_name, self.internship_description, self.is_gov) = internship_data
                    self.conn.commit()
                    return True
                else:
                    print(f"Internship with ID {self.intern_id} or name {self.internship_name} not found.")
                    return False
            except Exception as e:
                self.conn.rollback()
                return f"Error auto-filling internship: {e}"

    def update(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    UPDATE internship
                    SET internship_name = %s, internship_description = %s, is_gov = %s
                    WHERE intern_id = %s
                    ''',
                    (self.internship_name, self.internship_description, self.is_gov, self.intern_id)
                )

                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error updating internship: {e}"

    def delete(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    DELETE FROM internship
                    WHERE intern_id = %s OR internship_name = %s
                    ''',
                    (self.intern_id, self.internship_name)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error deleting internship: {e}"
