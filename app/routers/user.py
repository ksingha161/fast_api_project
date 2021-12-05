from fastapi import status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from ..schemas import UserCreate, UserResponse
import psycopg2
from .. import models, utils
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate,db: Session = Depends(get_db)):
    password = utils.hash_password(user.password)
    user.password = password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'user with {id} does not exists')

    return user        