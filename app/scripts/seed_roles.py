from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.role import Role
from app.constants.roles import ALL_ROLES

def seed_roles():
    db: Session = SessionLocal()
    try:
        for role_name in ALL_ROLES:
            exists = db.query(Role).filter(Role.name == role_name).first()
            if not exists:
                db.add(Role(name=role_name))
                print(f"Added role : {role_name}")
        db.commit()
    
    finally:
        db.close()
    

if __name__ == "__main__":
    seed_roles()
            