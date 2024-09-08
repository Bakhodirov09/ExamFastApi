import time
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import APIRouter, status, HTTPException
from jose import jwt
from general import tashkent, SECRET_KEY, ALGORITHM, db_dependencies
from models import UsersModel
from schema import LoginSchema, RegisterSchema
import re

router = APIRouter(prefix='/users', tags=['Auth'])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Regexes
USERNAME_REGEX = re.compile(r'^[a-z0-9_-]{3,15}$')
PHONE_REGEX = re.compile(r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$')
EMAIL_REGEX = re.compile(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+')
async def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}


def create_access_token(username: str, user_id: int, role: str):
    encode = {"sub": username, "id": user_id, 'role': role}
    expires = datetime.now(tz=tashkent) + timedelta(hours=20)
    encode.update({"exp": expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def check_login_type(type: str):
    if re.fullmatch(USERNAME_REGEX, type):
        return 'username'
    elif re.fullmatch(PHONE_REGEX, type):
        return 'phone'
    elif re.fullmatch(EMAIL_REGEX, type):
        return 'email'
    return False


def authenticate_user(type: str, password: str, db: db_dependencies):
    user = None
    if type.startswith('u'):
        user = db.query(UsersModel).filter_by(username=type, password=password)
    elif type.startswith('e'):
        user = db.query(UsersModel).filter_by(email=type, password=password)
    elif type.startswith('p'):
        user = db.query(UsersModel).filter_by(phone_number=type, password=password)
    return user

@router.post('/login', status_code=status.HTTP_201_CREATED, response_model=dict)
async def login_account(user_request: LoginSchema, db: db_dependencies):
    login_type = check_login_type(user_request.login_type)
    user = authenticate_user(type=login_type, password=user_request.password, db=db)
    if user is not None:
        token = create_access_token(username=user.username, user_id=user.id, role=user.role)
        return {'token': token}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')

@router.post('/register', status_code=status.HTTP_200_OK)
async def user_registration(user_request: RegisterSchema, db: db_dependencies):
    try:
        user_request.password = bcrypt_context.hash(user_request.password)
        new_user = UsersModel(**user_request.dict())
        db.add(new_user)
        db.commit()
        return {'message': 'Successfully created'}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Bad request. Error: {e}')