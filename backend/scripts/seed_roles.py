import uuid
from sqlalchemy.orm import Session
from app.database.database import SessionLocal, engine
from app.model import models

models.Base.metadata.create_all(bind=engine)

def seed_roles():
    db: Session = SessionLocal()

    roles = [
        {"name": "HR", "share": True, "edit": True, "delete": False, "upload": True},
        {"name": "IT", "share": True, "edit": True, "delete": True, "upload": True},
        {"name": "Management", "share": True, "edit": False, "delete": False, "upload": False},
        {"name": "Electronics", "share": False, "edit": True, "delete": True, "upload": True},
        {"name": "Networking", "share": False, "edit": False, "delete": True, "upload": True},
    ]

    for role_info in roles:
        role_id = uuid.uuid4()
        role = models.Role(id=role_id, name=role_info["name"])
        db.add(role)
        db.commit()
        db.refresh(role)

        perm = models.Permission(
            id=uuid.uuid4(),
            role_id=role.id,
            share=role_info["share"],
            edit=role_info["edit"],
            delete=role_info["delete"],
            upload=role_info["upload"]
        )
        db.add(perm)
        db.commit()

    db.close()
    print("✅ Roles and permissions seeded!")

if __name__ == "__main__":
    seed_roles()
