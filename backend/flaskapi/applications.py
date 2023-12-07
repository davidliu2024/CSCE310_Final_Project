from flask import Blueprint, request
from db_interface.documents import Document
from toolkit.user_tools import *
from toolkit.college_student_tools import *
from toolkit.document_tools import *

bp = Blueprint("applications", __name__, url_prefix="/applications")

@bp.route('/<int:appnum>/document', methods = ['POST'])
@authenticate
def upload_document_by_appnum(appnum):
    uploaded_file=request.files.get("file")
    return upload_document(appnum=appnum, uploaded_file=uploaded_file)

@bp.route('/<int:docnum>/document', methods = ['DELETE'])
@authenticate
def upload_document_by_appnum(docnum):
    doc = Document(doc_num=docnum)
    response = doc.delete()
    return { "response": response }