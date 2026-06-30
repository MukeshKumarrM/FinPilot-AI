from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User

EMAIL = "admin@finpilot.com"
PASSWORD = "Admin123!"
FULL_NAME = "Admin"

db = SessionLocal()
try:
    existing = db.query(User).filter(User.email == EMAIL).first()
    if existing:
        print(f"User already exists: id={existing.id}, email={existing.email}")
    else:
        user = User(
            email=EMAIL,
            hashed_password=get_password_hash(PASSWORD),
            full_name=FULL_NAME,
            is_admin=True,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Created user: id={user.id}, email={user.email}, is_admin={user.is_admin}")
finally:
    db.close()