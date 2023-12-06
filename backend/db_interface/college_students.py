from flask import g
import psycopg
from db_interface.users import User

class CollegeStudent:
    def __init__(self, uin=None, gender=None, hispanic_latino=None, race=None, us_citizen=None,
                 first_generation=None, dob=None, gpa=None, major=None, minor1=None, minor2=None,
                 expected_graduation=None, school=None, classification=None, phone=None,
                 student_type=None):
        self.uin = uin
        self.gender = gender
        self.hispanic_latino = hispanic_latino
        self.race = race
        self.us_citizen = us_citizen
        self.first_generation = first_generation
        self.dob = dob
        self.gpa = gpa
        self.major = major
        self.minor1 = minor1
        self.minor2 = minor2
        self.expected_graduation = expected_graduation
        self.school = school
        self.classification = classification
        self.phone = phone
        self.student_type = student_type
        try:
            self.conn = g.conn
        except RuntimeError:
            self.conn = None

    def set_connection_manually(self, conn):
        self.conn = conn

    def close_connection_manually(self):
        self.conn.close()

    def __repr__(self):
        return f"CollegeStudent(uin={self.uin}, gender='{self.gender}', hispanic_latino={self.hispanic_latino}, " \
               f"race='{self.race}', us_citizen={self.us_citizen}, first_generation={self.first_generation}, " \
               f"dob='{self.dob}', gpa={self.gpa}, major='{self.major}', minor1='{self.minor1}', " \
               f"minor2='{self.minor2}', expected_graduation={self.expected_graduation}, school='{self.school}', " \
               f"classification='{self.classification}', phone='{self.phone}', student_type='{self.student_type}')"

    def create(self):
        assert isinstance(self.conn, psycopg.Connection)
        userTest = User(uin = self.uin)
        if (len(userTest.fetch)==0):
            return "Error creating college student: User does not exist yet"

        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    INSERT INTO college_student (
                        uin, gender, hispanic_latino, race, us_citizen, first_generation, dob, gpa, major,
                        minor1, minor2, expected_graduation, school, classification, phone, student_type
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''',
                    (self.uin, self.gender, self.hispanic_latino, self.race, self.us_citizen,
                     self.first_generation, self.dob, self.gpa, self.major, self.minor1, self.minor2,
                     self.expected_graduation, self.school, self.classification, self.phone, self.student_type)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error creating college student: {e}"
    
    def fetch(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM college_student
                    WHERE gender = %s OR hispanic_latino = %s OR race = %s OR us_citizen = %s
                        OR first_generation = %s OR dob = %s OR gpa = %s OR major = %s OR minor1 = %s
                        OR minor2 = %s OR expected_graduation = %s OR school = %s OR classification = %s
                        OR phone = %s OR student_type = %s
                    ''',
                    (self.gender, self.hispanic_latino, self.race, self.us_citizen, 
                        self.first_generation, self.dob, self.gpa, self.major, self.minor1, self.minor2, 
                        self.expected_graduation, self.school, self.classification, self.phone, 
                        self.student_type)
                )
                result = cur.fetchall()
                self.conn.commit()
                return result
            except Exception as e:
                self.conn.rollback()
                return f"Error fetching college student: {e}"

    def delete(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    DELETE FROM college_student
                    WHERE uin = %s
                    ''',
                    (self.uin,)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error deleting college student: {e}"

    def auto_fill(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM college_student
                    WHERE uin = %s
                    ''',
                    (self.uin,)
                )

                student_data = cur.fetchone()

                if student_data:
                    (self.uin, self.gender, self.hispanic_latino, self.race, self.us_citizen,
                     self.first_generation, self.dob, self.gpa, self.major, self.minor1, self.minor2,
                     self.expected_graduation, self.school, self.classification, self.phone,
                     self.student_type) = student_data

                    self.conn.commit()
                    return True
                else:
                    print(f"College student with UIN {self.uin} not found.")
                    return False
            except Exception as e:
                self.conn.rollback()
                return f"Error auto-filling college student: {e}"

    def update(self):
        assert isinstance(self.conn, psycopg.Connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    UPDATE college_student
                    SET gender = %s, hispanic_latino = %s, race = %s, us_citizen = %s,
                        first_generation = %s, dob = %s, gpa = %s, major = %s, minor1 = %s,
                        minor2 = %s, expected_graduation = %s, school = %s, classification = %s,
                        phone = %s, student_type = %s
                    WHERE uin = %s
                    ''',
                    (self.gender, self.hispanic_latino, self.race, self.us_citizen,
                     self.first_generation, self.dob, self.gpa, self.major, self.minor1, self.minor2,
                     self.expected_graduation, self.school, self.classification, self.phone,
                     self.student_type, self.uin)
                )

                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error updating college student: {e}"

    def getJSON(self):
        student_dict = {
            "uin": self.uin,
            "gender": self.gender,
            "hispanic_latino": self.hispanic_latino,
            "race": self.race,
            "us_citizen": self.us_citizen,
            "first_generation": self.first_generation,
            "dob": self.dob,
            "gpa": self.gpa,
            "major": self.major,
            "minor1": self.minor1,
            "minor2": self.minor2,
            "expected_graduation": self.expected_graduation,
            "school": self.school,
            "classification": self.classification,
            "phone": self.phone,
            "student_type": self.student_type
        }
        return student_dict