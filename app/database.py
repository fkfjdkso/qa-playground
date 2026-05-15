from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os

if os.getenv("LOCAL_DB") == "True":
    DB_HOST = os.getenv("DB_HOST", "db")
    DATABASE_URL = (
        f"postgresql+psycopg2://qa_user:qa_password@{DB_HOST}:5432/qa_playground"
    )
    engine = create_engine(DATABASE_URL)
else:
    load_dotenv(override=True)

    USER = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASSWORD")
    HOST = os.getenv("DB_HOST")
    DBNAME = os.getenv("DB")

    DATABASE_URL = URL.create(
        "postgresql+psycopg2",
        username=USER,
        password=PASSWORD,
        host=HOST,
        database=DBNAME,
        query={"sslmode": "require"},
    )

    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
    )


Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    with engine.connect() as connection:
        print("connection successful")
except Exception as e:
    print(f"failed to connect {e}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
