from flask import g
import psycopg

class Document:
    def __init__(self, app_num, link, doc_type=None, doc_num=None):
        self.doc_num = doc_num
        self.app_num = app_num
        self.link = link
        self.doc_type = doc_type
        try:
            self.conn = g.conn
        except RuntimeError:
            self.conn = None

    def set_connection_manually(self, conn):
        self.conn = conn

    def close_connection_manually(self):
        self.conn.close()

    def __repr__(self):
        return f"Document(doc_num={self.doc_num}, app_num={self.app_num}, link='{self.link}', doc_type='{self.doc_type}')"

    def create(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    INSERT INTO document (app_num, link, doc_type)
                    VALUES (%s, %s, %s)
                    RETURNING doc_num
                    ''',
                    (self.app_num, self.link, self.doc_type)
                )
                self.doc_num = cur.fetchone()[0]
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error creating document: {e}"

    def fetch(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM document
                    WHERE doc_num = %s or app_num = %s
                    ''',
                    (self.doc_num, self.app_num)
                )
                return cur.fetchall()
            except Exception as e:
                self.conn.rollback()
                print(f"Error fetching document: {e}")
                return None

    def auto_fill(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM document
                    WHERE doc_num = %s
                    ''',
                    (self.doc_num,)
                )

                document_data = cur.fetchone()

                if document_data:
                    (self.doc_num, self.app_num, self.link, self.doc_type) = document_data
                    self.conn.commit()
                    return True
                else:
                    print(f"Document with ID {self.doc_num} not found.")
                    return False
            except Exception as e:
                self.conn.rollback()
                return f"Error auto-filling document: {e}"

    def delete(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    DELETE FROM document
                    WHERE doc_num = %s
                    ''',
                    (self.doc_num,)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error deleting document: {e}"
