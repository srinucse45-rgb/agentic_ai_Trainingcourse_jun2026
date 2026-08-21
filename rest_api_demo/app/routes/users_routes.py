from pydantic import BaseModel
from fastapi import APIRouter
from app.services.users_service import (
    get_all_users,
    create_user,
    fetch_user_by_id,
    update_user_by_id,
)


# custom data type using pydantic basemodel
class User(BaseModel):
    name: str
    email: str
    phone: str


router = APIRouter(prefix="/api/v1/users")


# To list users  on localhost:8000/api/v1/users. - GET
@router.get("/")
def get_users():
    return get_all_users()


# To add user  on localhost:8000/api/v1/users. - POST
@router.post("/")
def add_user(user: User):  # capturing the req body
    print(user)
    return create_user(user)


# To get user by id  on localhost:8000/api/v1/users/1 - GET
@router.get("/{user_id}")  # user_id is url param
def get_user_by_id(user_id: str):
    print("Requested User Id :" + user_id)
    return fetch_user_by_id(user_id)


# To update user by id
@router.put("/{user_id}")  # user_id is url param
def update_user(user_id: str, user: User):
    print("Requested User Id :" + user_id)
    return update_user_by_id(user_id, user)
