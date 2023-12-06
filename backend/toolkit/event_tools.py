from flask import Blueprint, request, g, abort, Response, jsonify
import psycopg
from datetime import datetime
import sys
sys.path.insert(1, "/home/david-liu/david_liu/TAMU/FALL2023/CSCE310/final_project/CSCE310_Final_Project/backend")
from db_interface.events import Event

def create_event(eventJSON) -> Event:
    '''
    Create a new event and return the event with eventJSON
    '''
    event = Event(
        uin=eventJSON['uin'],
        program_num=eventJSON['program_num'],
        event_name=eventJSON['event_name'],
        event_start_date=eventJSON.get('event_start_date'),
        event_start_time=eventJSON.get('event_start_time'),
        event_end_date=eventJSON.get('event_end_date'),
        event_end_time=eventJSON.get('event_end_time'),
        event_location=eventJSON.get('event_location'),
        event_type=eventJSON.get('event_type')
    )

    event.create()
    return event


def fetch_all_events():
    '''
    Fetch all events and return as JSON
    '''
    assert isinstance(g.conn, psycopg.Connection)

    with g.conn.cursor() as cur:
        try:
            cur.execute(
                '''
                SELECT * FROM event_table
                '''
            )
            event_records = cur.fetchall()

            # Convert the result to a list of dictionaries
            events_list = [
                {
                    'event_id': record[0],
                    'uin': record[1],
                    'program_num': record[2],
                    'event_name': record[3],
                    'event_start_date': record[4],
                    'event_start_time': record[5],
                    'event_end_date': record[6],
                    'event_end_time': record[7],
                    'event_location': record[8],
                    'event_type': record[9]
                }
                for record in event_records
            ]

            return jsonify(events_list)

        except Exception as e:
            g.conn.rollback()
            return {"response" : f"Error fetching all events: {e}"}

def fetch_events_between_times(self, start_datetime, end_datetime):
    assert isinstance(self.conn, psycopg.Connection)
    assert isinstance(start_datetime, datetime)
    assert isinstance(end_datetime, datetime)

    start_time = start_datetime.time()
    end_time = end_datetime.time()
    start_date = start_datetime.date()
    end_date = end_datetime.date()

    with self.conn.cursor() as cur:
        try:
            cur.execute(
                '''
                SELECT * FROM event_table
                WHERE event_start_date >= %s AND event_end_date <= %s event_start_time >= %s AND event_end_time <= %s
                ''',
                (start_date, end_date, start_time, end_time)
            )
            result = cur.fetchall()
            self.conn.commit()
            return result
        except Exception as e:
            self.conn.rollback()
            return f"Error fetching events between times: {e}"

def patch_event(eventJSON) -> Event:
    '''
    Create a new event and return the event with eventJSON
    '''
    event = Event(
        uin=eventJSON['uin'],
        program_num=eventJSON['program_num'],
        event_name=eventJSON['event_name'],
        event_start_date=eventJSON.get('event_start_date'),
        event_start_time=eventJSON.get('event_start_time'),
        event_end_date=eventJSON.get('event_end_date'),
        event_end_time=eventJSON.get('event_end_time'),
        event_location=eventJSON.get('event_location'),
        event_type=eventJSON.get('event_type')
    )

    return { "response": event.update() }
