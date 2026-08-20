from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings


# Tạo engine kết nối MySQL
engine = create_engine(settings.DATABASE_URL)

# Tạo SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base cho các SQLAlchemy Model
Base = declarative_base()


# Dependency lấy database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
