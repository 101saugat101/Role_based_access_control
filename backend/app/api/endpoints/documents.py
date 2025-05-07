from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.core.enums import RoleEnum
from app.api.handlers import documents_handler as handler

router = APIRouter()

@router.post("/documents/upload")
def upload_document(
    role: RoleEnum = Query(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    document = handler.handle_file_upload(role, file, db)
    return {"message": f"File uploaded by {role.value}", "document_id": str(document.id)}

@router.get("/documents/{doc_id}")
def view_document(doc_id: str, role: RoleEnum = Query(...), db: Session = Depends(get_db)):
    document = handler.handle_view_document(role, doc_id, db)
    return {
        "filename": document.filename,
        "uploaded_by": document.uploader_role,
        "assigned_to": document.assigned_to
    }

@router.delete("/documents/{doc_id}")
def delete_document(doc_id: str, role: RoleEnum = Query(...), db: Session = Depends(get_db)):
    return handler.handle_delete_document(role, doc_id, db)

@router.post("/documents/{doc_id}/assign")
def assign_document(doc_id: str, assign_to: RoleEnum, role: RoleEnum = Query(...), db: Session = Depends(get_db)):
    return handler.handle_assign_document(doc_id, assign_to, role, db)
