from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from src.users.schema import UserRegisterSchema, UserLoginSchema
from src.users.model import UserModel
from sqlalchemy.orm import session
from database import get_db
from src.utils.auth_utils import get_password_hash, verify_password
import uuid
from utils.auth_utils import create_access_token, get_current_user

user_router = APIRouter()


@user_router.post('/register')
def create_user(
    schema : UserRegisterSchema,
    db : session = Depends(get_db)
):
    
    db_user = db.query(UserModel).filter(UserModel.email == schema.email, UserModel.is_deleted == False).first()

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already Exist"
        )
    
    hashed_password = get_password_hash(schema.password)
    
    new_user = UserModel(
        id = str(uuid.uuid4()),
        name = schema.name,
        email = schema.email,
        password = hashed_password,
        role = "customer"
    )

    db.add(new_user)
    db.commit()

    return{
        "user" : new_user.id,
        "status" : status.HTTP_201_CREATED,
        "message" : "User created successfully"
    }

@user_router.post('admin/register')
def create_admin_user(
    schema : UserRegisterSchema,
    db : session = Depends(get_db)
):
    
    db_user = db.query(UserModel).filter(UserModel.email == schema.email, UserModel.is_deleted == False).first()

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already Exist"
        )
    
    hashed_password = get_password_hash(schema.password)
    
    new_user = UserModel(
        id = str(uuid.uuid4()),
        name = schema.name,
        email = schema.email,
        password = hashed_password,
        role = "admin"
    )

    db.add(new_user)
    db.commit()

    return{
        "user" : new_user.id,
        "status" : status.HTTP_201_CREATED,
        "message" : "User created successfully"
    }


@user_router.post("/login")
def login_user(
        schema : UserLoginSchema, 
        db : session = Depends(get_db)
):
    
    db_user = db.query(UserModel).filter(UserModel.email == schema.email).first()

    if not db_user and verify_password(schema.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="wrong email or password"
        )
    
    access_token = create_access_token(db_user.id, db_user.role)

    return{
        "access_token" : access_token,
        "status" : status.HTTP_202_ACCEPTED,
    }

@user_router.get("/get_current")
def read_current_user(current_user : dict = Depends(get_current_user)):
    return current_user


    
