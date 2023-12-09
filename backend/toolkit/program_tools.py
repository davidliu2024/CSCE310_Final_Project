from posixpath import isabs
from flask import g, jsonify
import psycopg
from db_interface.programs import Program
from db_interface.users import User

def create_program(programJSON):
    '''
    Create a new program and return the program with programJSON
    '''
    program = Program(
        program_name=programJSON['program_name'],
        program_description=programJSON.get('program_description'),
        program_status=programJSON.get('program_status')
    )

    return program.create()

def fetch_all_programs():
    '''
    Fetch all programs and return as JSON
    '''
    assert isinstance(g.conn, psycopg.Connection)
    assert isinstance(g.userobj, User)
    programs = Program().fetch_all()
    if g.userobj.isAdmin():
        return programs
    else:
        active_only = [program for program in programs if program.get("program_status") == "ACTIVE"]
        return active_only

        
def fetch_user_programs():
    '''
    Get all programs that the authenticated user is enrolled in based on g.useruin
    '''
    assert isinstance(g.conn, psycopg.Connection)

    with g.conn.cursor() as cur:
        try:
            cur.execute(
                '''
                SELECT p.program_num, p.program_name, p.program_description, p.program_status
                FROM programs p
                JOIN track t ON p.program_num = t.program_num
                WHERE t.uin = %s
                ''',
                (g.useruin,)
            )
            program_records = cur.fetchall()

            # Convert the result to a list of dictionaries
            programs_list = [
                {
                    'program_num': record[0],
                    'program_name': record[1],
                    'program_description': record[2],
                    'program_status': record[3]
                }
                for record in program_records
            ]

            return jsonify(programs_list)

        except Exception as e:
            g.conn.rollback()
            return {"response": f"Error fetching user enrolled programs: {e}"}          

def patch_program(program_num, programJSON):
    '''
    Update an existing program and return the program with programJSON
    '''
    program = Program(
        program_num=program_num,
        program_name=programJSON['program_name'],
        program_description=programJSON.get('program_description'),
        program_status=programJSON.get('program_status')
    )

    return program.update()
