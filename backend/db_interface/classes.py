from flask import g
import psycopg

class CourseClass:
    def __init__(self, class_id=None, class_name=None, class_description=None, class_type=None):
        self.class_id = class_id
        self.class_name = class_name
        self.class_description = class_description
        self.class_type = class_type
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
        return f"CourseClass(class_id={self.class_id}, class_name='{self.class_name}', " \
               f"class_description='{self.class_description}', class_type='{self.class_type}')"

    def create(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    INSERT INTO classes (class_name, class_description, class_type)
                    VALUES (%s, %s, %s)
                    RETURNING class_id
                    ''',
                    (self.class_name, self.class_description, self.class_type)
                )
                self.class_id = cur.fetchone()
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error creating class: {e}"

    def fetch(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM classes
                    WHERE class_id = %s OR class_name = %s
                    ''',
                    (self.class_id, self.class_name)
                )
                return cur.fetchall()
            except Exception as e:
                self.conn.rollback()
                print(f"Error fetching class: {e}")
                return []

    def auto_fill(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM classes
                    WHERE class_id = %s OR class_name = %s
                    ''',
                    (self.class_id, self.class_name)
                )

                class_data = cur.fetchone()

                if class_data:
                    (self.class_id, self.class_name, self.class_description, self.class_type) = class_data
                    self.conn.commit()
                    return True
                else:
                    print(f"Class with ID {self.class_id} or name {self.class_name} not found.")
                    return False
            except Exception as e:
                self.conn.rollback()
                return f"Error auto-filling class: {e}"

    def update(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    UPDATE classes
                    SET class_name = %s, class_description = %s, class_type = %s
                    WHERE class_id = %s
                    ''',
                    (self.class_name, self.class_description, self.class_type, self.class_id)
                )

                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error updating class: {e}"

    def delete(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    DELETE FROM classes
                    WHERE class_id = %s OR class_name = %s
                    ''',
                    (self.class_id, self.class_name)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error deleting class: {e}"

    def get_json(self):
        """
        Return a JSON representation of the CourseClass object.
        """
        class_json = {
            "class_id": self.class_id,
            "class_name": self.class_name,
            "class_description": self.class_description,
            "class_type": self.class_type
        }
        return class_json