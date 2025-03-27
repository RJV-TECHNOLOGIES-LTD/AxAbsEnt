from fastapi import APIRouter
from AxAbsEnt.sql_registry.init import get_engine, get_session
from AxAbsEnt.sql_registry.models import Dimension

router = APIRouter()

@router.get("/dimensions")
def list_dimensions():
    session = get_session(get_engine())
    return session.query(Dimension).all()

@router.get("/dimension/{code}")
def get_dimension(code: str):
    session = get_session(get_engine())
    return session.query(Dimension).filter_by(code=code).first()
