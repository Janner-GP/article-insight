from fastapi import Depends
from sqlmodel import Session, create_engine
from core.config.environments import DATABASE_URL

engine = create_engine(url=DATABASE_URL)

# Generador de sesión
def get_session():
    with Session(engine) as session:
        yield session

def get_session_db(session: Session = Depends(get_session)) -> Session:
    return session