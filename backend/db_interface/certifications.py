from flask import g
import psycopg

class Certification:
    def __init__(self, cert_id=None, cert_level=None, cert_name=None, cert_description=None):
        self.cert_id = cert_id
        self.cert_level = cert_level
        self.cert_name = cert_name
        self.cert_description = cert_description
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
        return f"Certification(cert_id={self.cert_id}, cert_level='{self.cert_level}', " \
               f"cert_name='{self.cert_name}', cert_description='{self.cert_description}')"

    def create(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    INSERT INTO certification (cert_level, cert_name, cert_description)
                    VALUES (%s, %s, %s)
                    RETURNING cert_id
                    ''',
                    (self.cert_level, self.cert_name, self.cert_description)
                )
                self.cert_id = cur.fetchone()
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error creating certification: {e}"

    def fetch(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM certification
                    WHERE cert_id = %s OR cert_name = %s
                    ''',
                    (self.cert_id, self.cert_name)
                )
                return cur.fetchall()
            except Exception as e:
                self.conn.rollback()
                print(f"Error fetching certification: {e}")
                return []

    def auto_fill(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM certification
                    WHERE cert_id = %s OR cert_name = %s
                    ''',
                    (self.cert_id, self.cert_name)
                )

                certification_data = cur.fetchone()

                if certification_data:
                    (self.cert_id, self.cert_level, self.cert_name, self.cert_description) = certification_data
                    self.conn.commit()
                    return True
                else:
                    print(f"Certification with ID {self.cert_id} or name {self.cert_name} not found.")
                    return False
            except Exception as e:
                self.conn.rollback()
                return f"Error auto-filling certification: {e}"

    def update(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    UPDATE certification
                    SET cert_level = %s, cert_name = %s, cert_description = %s
                    WHERE cert_id = %s
                    ''',
                    (self.cert_level, self.cert_name, self.cert_description, self.cert_id)
                )

                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error updating certification: {e}"

    def delete(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    DELETE FROM certification
                    WHERE cert_id = %s OR cert_name = %s
                    ''',
                    (self.cert_id, self.cert_name)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error deleting certification: {e}"

    def get_json(self):
        """
        Return JSON representation of the Certification object.
        """
        return {
            "cert_id": self.cert_id,
            "cert_level": self.cert_level,
            "cert_name": self.cert_name,
            "cert_description": self.cert_description
        }
