from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

database_url = settings.DATABASE_URL
engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=engine)