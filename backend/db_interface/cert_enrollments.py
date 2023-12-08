from flask import g
import psycopg

from db_interface.certifications import Certification

class CertEnrollment:
    def __init__(self, certe_num=None, uin=None, cert_id=None, cert_status=None, training_status=None,
                 program_num=None, semester=None, cert_year=None):
        self.certe_num = certe_num
        self.uin = uin
        self.cert_id = cert_id
        self.cert_status = cert_status
        self.training_status = training_status
        self.program_num = program_num
        self.semester = semester
        self.cert_year = cert_year
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
        return f"CertEnrollment(certe_num={self.certe_num}, uin={self.uin}, cert_id={self.cert_id}, " \
               f"cert_status='{self.cert_status}', training_status='{self.training_status}', " \
               f"program_num={self.program_num}, semester='{self.semester}', cert_year={self.cert_year})"

    def create(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    INSERT INTO cert_enrollment (uin, cert_id, cert_status, training_status,
                                                program_num, semester, cert_year)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING certe_num
                    ''',
                    (self.uin, self.cert_id, self.cert_status, self.training_status,
                     self.program_num, self.semester, self.cert_year)
                )
                self.certe_num = cur.fetchone()
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error creating certification enrollment: {e}"

    def fetch(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM cert_enrollment
                    WHERE certe_num = %s OR uin = %s OR cert_id = %s OR semester = %s OR cert_year = %s
                    ''',
                    (self.certe_num, self.uin, self.cert_id, self.semester, self.cert_year)
                )
                result = cur.fetchall()
                assert isinstance(cur.description, list)

                columns = [desc[0] for desc in cur.description]
                json_result = [dict(zip(columns, row)) for row in result]

                for result in json_result:
                    c = Certification(cert_id = result.get('cert_id'))
                    c.auto_fill()
                    result['cert_details'] = c.get_json()

                return json_result
            except Exception as e:
                self.conn.rollback()
                print(f"Error fetching certification enrollment: {e}")
                return []

    def auto_fill(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM cert_enrollment
                    WHERE certe_num = %s OR (uin = %s AND cert_id = %s)
                    ''',
                    (self.certe_num, self.uin, self.cert_id)
                )

                cert_enrollment_data = cur.fetchone()

                if cert_enrollment_data:
                    (self.certe_num, self.uin, self.cert_id, self.cert_status, self.training_status,
                     self.program_num, self.semester, self.cert_year) = cert_enrollment_data
                    self.conn.commit()
                    return True
                else:
                    print(f"Certification enrollment with ID {self.certe_num} not found.")
                    return False
            except Exception as e:
                self.conn.rollback()
                return f"Error auto-filling certification enrollment: {e}"

    def update(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    UPDATE cert_enrollment
                    SET uin = %s, cert_id = %s, cert_status = %s, training_status = %s,
                        program_num = %s, semester = %s, cert_year = %s
                    WHERE certe_num = %s
                    ''',
                    (self.uin, self.cert_id, self.cert_status, self.training_status,
                     self.program_num, self.semester, self.cert_year, self.certe_num)
                )

                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error updating certification enrollment: {e}"

    def delete(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    DELETE FROM cert_enrollment
                    WHERE certe_num = %s OR (uin = %s AND cert_id = %s)
                    ''',
                    (self.certe_num, self.uin, self.cert_id)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error deleting certification enrollment: {e}"

    def get_json(self):
        return {
            "certe_num": self.certe_num,
            "uin": self.uin,
            "cert_id": self.cert_id,
            "cert_status": self.cert_status,
            "training_status": self.training_status,
            "program_num": self.program_num,
            "semester": self.semester,
            "cert_year": self.cert_year
        }