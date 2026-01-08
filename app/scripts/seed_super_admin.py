from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.constants.roles import SUPER_ADMIN

EMAIL="test@google.com"
PASSWORD="Admin@123"
MOBILE_NUMBER="0000000000"

def seed_super_admin():
    db: Session = SessionLocal()
    
    try:
        role = db.query(Role).filter(Role.name == SUPER_ADMIN).first()
        if not role:
            raise Exception("SUPER_ADMIN role not found")

        admin = db.query(User).filter(User.email == EMAIL).first()
        if admin:
            print("Super Admin already exists")
            return
    
        admin = User(
            first_name="Super",
            last_name="Admin",
            email=EMAIL,
            mobile_number=MOBILE_NUMBER,
            password=PASSWORD,
            role_id=role.id
        )
        
        db.add(admin)
        db.commit()
        print("Super Admin Created")
    
    finally:
        db.close()
    
if __name__ == "__main__":
    seed_super_admin()
