from flask import g
from db_interface.applications import Application

def submit_application(application_data) -> Application:
    """
    Submit a new application and return the application instance.
    """
    application = Application(
        program_num=application_data['program_num'],
        user_id=g.userobj.user_id,
        uncompleted_certificate=application_data.get('uncompleted_certificate'),
        completed_certificate=application_data.get('completed_certificate'),
        purpose_statement=application_data.get('purpose_statement'),
    )

    application.create()
    return application

def edit_application(application_id, updated_data) -> Application:
    """
    Edit an existing application and return the updated application instance.
    """
    application = Application(application_id=application_id)

    if not application.fetch():
        return {"response": f"No application with ID: {application_id}"}

    application.update(updated_data)
    return application

def view_application_info(application_id) -> dict:
    """
    View the details and status of a specific application.
    """
    application = Application(application_id=application_id)

    if not application.fetch():
        return {"response": f"No application with ID: {application_id}"}

    return {
        'application_id': application.application_id,
        'program_num': application.program_num,
        'purpose_statement': application.purpose_statement,
        'application_status': application.application_status,
    }

def delete_application(application_id) -> dict:
    """
    Delete a specific application and return a response.
    """
    application = Application(application_id=application_id)

    if not application.fetch():
        return {"response": f"No application with ID: {application_id}"}

    response = application.delete()
    return response
