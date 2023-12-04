from flask import g
import psycopg

class Event:
    def __init__(self, event_id=None, uin=None, program_num=None, event_name=None, event_start_date=None,
                 event_start_time=None, event_end_date=None, event_end_time=None, event_location=None, event_type=None):
        self.event_id = event_id
        self.uin = uin
        self.program_num = program_num
        self.event_name = event_name
        self.event_start_date = event_start_date
        self.event_start_time = event_start_time
        self.event_end_date = event_end_date
        self.event_end_time = event_end_time
        self.event_location = event_location
        self.event_type = event_type
        try:
            self.conn = g.conn
        except RuntimeError:
            self.conn = None

    def set_connection_manually(self, conn):
        self.conn = conn

    def close_connection_manually(self):
        self.conn.close()

    def __repr__(self):
        return f"Event(event_id={self.event_id}, uin={self.uin}, program_num={self.program_num}, " \
               f"event_name='{self.event_name}', event_start_date={self.event_start_date}, " \
               f"event_start_time={self.event_start_time}, event_end_date={self.event_end_date}, " \
               f"event_end_time={self.event_end_time}, event_location='{self.event_location}', " \
               f"event_type='{self.event_type}')"

    def create(self):
        assert isinstance(self.conn, psycopg.connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    INSERT INTO event_table (uin, program_num, event_name, event_start_date, event_start_time,
                                            event_end_date, event_end_time, event_location, event_type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING event_id
                    ''',
                    (self.uin, self.program_num, self.event_name, self.event_start_date, self.event_start_time,
                     self.event_end_date, self.event_end_time, self.event_location, self.event_type)
                )
                self.event_id = cur.fetchone()[0]
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error creating event: {e}"

    def fetch(self):
        assert isinstance(self.conn, psycopg.connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM event_table
                    WHERE event_id = %s OR uin = %s OR program_num = %s OR event_name = %s
                    ''',
                    (self.event_id, self.uin, self.program_num, self.event_name)
                )
                return cur.fetchall()
            except Exception as e:
                self.conn.rollback()
                print(f"Error fetching event: {e}")
                return None

    def auto_fill(self):
        assert isinstance(self.conn, psycopg.connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    SELECT * FROM event_table
                    WHERE event_id = %s OR uin = %s OR program_num = %s OR event_name = %s
                    ''',
                    (self.event_id, self.uin, self.program_num, self.event_name)
                )

                event_data = cur.fetchone()

                if event_data:
                    (self.event_id, self.uin, self.program_num, self.event_name, self.event_start_date,
                     self.event_start_time, self.event_end_date, self.event_end_time, self.event_location,
                     self.event_type) = event_data
                    self.conn.commit()
                    return True
                else:
                    print(f"Event with ID {self.event_id} or name {self.event_name} not found.")
                    return False
            except Exception as e:
                self.conn.rollback()
                return f"Error auto-filling event: {e}"

    def update(self):
        assert isinstance(self.conn, psycopg.connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    UPDATE event_table
                    SET uin = %s, program_num = %s, event_name = %s, event_start_date = %s, event_start_time = %s,
                        event_end_date = %s, event_end_time = %s, event_location = %s, event_type = %s
                    WHERE event_id = %s
                    ''',
                    (self.uin, self.program_num, self.event_name, self.event_start_date, self.event_start_time,
                     self.event_end_date, self.event_end_time, self.event_location, self.event_type, self.event_id)
                )

                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error updating event: {e}"

    def delete(self):
        assert isinstance(self.conn, psycopg.connection)
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    '''
                    DELETE FROM event_table
                    WHERE event_id = %s OR uin = %s OR program_num = %s OR event_name = %s
                    ''',
                    (self.event_id, self.uin, self.program_num, self.event_name)
                )
                self.conn.commit()
                return "success"
            except Exception as e:
                self.conn.rollback()
                return f"Error deleting event: {e}"
