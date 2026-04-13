from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Engine é a conexão com o banco de dados
engine = create_engine(DATABASE_URL)

# SessionLocal é uma fábrica de sessões — cada request da API abre uma sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# Dependency: abre uma sessão por request e fecha ao terminar
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
