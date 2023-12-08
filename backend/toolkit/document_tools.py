from flask import abort, jsonify
from db_interface.documents import Document
from io import BytesIO
from googleapiclient.http import MediaIoBaseUpload
from datetime import datetime
from db_interface.applications import Application
from db_interface.programs import Program
from google_drive_interface.google_drive_service import GoogleDriveService
service = GoogleDriveService().build()


def upload_document(appnum, uploaded_file):
    buffer_memory=BytesIO()
    uploaded_file.save(buffer_memory)

    media_body=MediaIoBaseUpload(uploaded_file, uploaded_file.mimetype, resumable=True)

    created_at= datetime.now().strftime("%Y%m%d%H%M%S")
    file_metadata={
        "name":f"{uploaded_file.filename} ({created_at})",
        "parents" : ['15MVTNBgY3hOXmHpwNiR1vMzOzMXpM3oN']
    }

    returned_fields="id, name, mimeType, webViewLink, exportLinks"
    
    upload_response=service.files().create(
        body = file_metadata, 
        media_body=media_body,  
        fields=returned_fields
    ).execute()

    file_link = upload_response['webViewLink']
    file_type = upload_response['mimeType'].split('/')[1]
    return create_new_doc_in_db(appnum=appnum, file_link=file_link, file_type=file_type)


def create_new_doc_in_db(appnum, file_link, file_type):
    new_doc = Document(app_num=appnum, link=file_link, doc_type=file_type)
    return {"response": new_doc.create()}
    
def fetch_documents(uin=None, app_num=None):
    results = []
    if uin is not None:
        app = Application(uin=uin)
        apps = app.fetch()
        for a in apps:
            p = Program(program_num = a.get("program_num"))
            p.auto_fill()
            d = Document(app_num=a.get("app_num"))
            links = d.fetch()
            for link in links:
                results.append({"program_name": p.program_name,
                                "doc_link": link.get("link")
                                })
        return jsonify(results)
    elif app_num is not None:
        doc = Document(app_num=app_num)
        links = doc.fetch()
        for link in links:
            results.append(link.get("link"))
        return jsonify({"links": results})
    else:
        abort(400)