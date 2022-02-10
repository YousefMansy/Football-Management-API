from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.footballfantasyapi.core.config import settings

connection_uri = settings.SQLALCHEMY_DATABASE_URI
if connection_uri.startswith("postgres://"):
    connection_uri = connection_uri.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    connection_uri,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
