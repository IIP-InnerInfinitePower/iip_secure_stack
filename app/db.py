from config import DATABASE_URL
from sqlalchemy import create_engine, text

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def test_db():
    with engine.connect() as conn:
        return conn.execute(text("SELECT 'db_ok'")).scalar()
