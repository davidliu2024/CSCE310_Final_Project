from flask import g
import psycopg


class Document:
    def __init__(self, person_id, document_type, document_uri, upload_date, expiration_date):
        self.person_id = person_id
        self.document_type = document_type
        self.document_uri = document_uri
        self.upload_date = upload_date
        self.expiration_date = expiration_date

        try:
            self.conn = g.__contains__
        except RuntimeError:
            self.conn = None

    
    def upload_document(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    INSERT INTO documents
                    '''
                    ()
                )
                self.conn.commit()
                return "success"
            
            
            except Exception as e:
                self.conn.rollback()
                return f"Error uploading document to database"