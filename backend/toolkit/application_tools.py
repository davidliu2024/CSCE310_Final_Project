from flask import g
import psycopg
from datetime import date
from db_interface.applications import Application

class ApplicationTools:
    @staticmethod
    def create_application(program_num, uin, uncom_cert=None, com_cert=None, purpose_statement=None):
        application_instance = Application(
            program_num=program_num,
            uin=uin,
            uncom_cert=uncom_cert,
            com_cert=com_cert,
            purpose_statement=purpose_statement
        )

        return application_instance.create()

    @staticmethod
    def fetch_application(app_num=None, program_num=None, uin=None):
        application_instance = Application(app_num=app_num, program_num=program_num, uin=uin)
        return application_instance.fetch()

    @staticmethod
    def auto_fill_application(app_num=None, program_num=None, uin=None):
        application_instance = Application(app_num=app_num, program_num=program_num, uin=uin)
        return application_instance.auto_fill()

    @staticmethod
    def update_application(app_num, program_num, uin, uncom_cert=None, com_cert=None, purpose_statement=None):
        application_instance = Application(
            app_num=app_num,
            program_num=program_num,
            uin=uin,
            uncom_cert=uncom_cert,
            com_cert=com_cert,
            purpose_statement=purpose_statement
        )

        return application_instance.update()

    @staticmethod
    def delete_application(app_num=None, program_num=None, uin=None):
        application_instance = Application(app_num=app_num, program_num=program_num, uin=uin)
        return application_instance.delete()

    @staticmethod
    def fetch_applications_between_dates(start_date, end_date):
        return Application().fetch_applications_between_dates(start_date, end_date)

