import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

user = os.getenv("USER")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")
host = os.getenv("HOST")
port = os.getenv("PORT")

URI = f"postgresql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(URI, echo=True, pool_size=5, max_overflow=0)
SessionLocal = sessionmaker(bind=engine)
