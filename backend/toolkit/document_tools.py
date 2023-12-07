from db_interface.documents import Document
from io import BytesIO
from googleapiclient.http import MediaIoBaseUpload
from datetime import datetime
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
    