import os
from uuid import uuid4
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.model.models import Permission, Role, Document
from app.core.enums import RoleEnum

UPLOAD_DIR = "./uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_role_permissions(role: RoleEnum, db: Session):
    role_obj = db.query(Role).filter(Role.name == role.value).first()
    if not role_obj:
        raise HTTPException(status_code=404, detail=f"Role '{role}' not found")
    perm = db.query(Permission).filter(Permission.role_id == role_obj.id).first()
    if not perm:
        raise HTTPException(status_code=403, detail="Permissions not set for this role")
    return perm

def handle_file_upload(role, file, db):
    perm = get_role_permissions(role, db)
    if not perm.upload:
        raise HTTPException(status_code=403, detail="Upload not allowed")

    unique_filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    document = Document(
        filename=file.filename,
        uploader_role=role.value,
        file_path=file_path
    )
    db.add(document)
    db.commit()

    return document

def handle_view_document(role, doc_id, db):
    document = db.query(Document).filter(Document.id == doc_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if role == RoleEnum.HR:
        return document
    elif document.uploader_role == role.value or document.assigned_to == role.value:
        return document
    else:
        raise HTTPException(status_code=403, detail="Access denied")

def handle_delete_document(role, doc_id, db):
    document = db.query(Document).filter(Document.id == doc_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if role == RoleEnum.HR or document.uploader_role == role.value:
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        db.delete(document)
        db.commit()
        return {"message": f"Document {doc_id} deleted by {role.value}"}
    else:
        raise HTTPException(status_code=403, detail="Delete not allowed")

def handle_assign_document(doc_id, assign_to, role, db):
    if role != RoleEnum.HR:
        raise HTTPException(status_code=403, detail="Only HR can assign documents")

    document = db.query(Document).filter(Document.id == doc_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    document.assigned_to = assign_to.value
    db.commit()

    return {"message": f"Document {doc_id} assigned to {assign_to.value}"}
