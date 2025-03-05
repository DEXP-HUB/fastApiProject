from typing import Literal
from DataBase.postgre_sql import ConnectionDb, SelectUser, InsertUser, DeleteUser, UpdateUser
from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, Field, EmailStr
from authx import AuthX, AuthXConfig


class UserSchema(BaseModel):
    login: str = Field(default=None, max_length=20)
    password: str = Field(default=None, max_length=20)
    first_name: str = Field(default=None, max_length=15)
    last_name: str = Field(default=None, max_length=15)
    city: str = Field(default=None, max_length=20)
    address: str = Field(default=None, max_length=50)
    age: int = Field(default=None, ge=0, le=115)
    floor: int = Field(default=None, ge=0, le=163)
    apartament_number: int = Field(default=None, ge=0)
    id: int = Field(default=None, ge=0)
    data_registratsii: Literal['NOW()'] = Field(default=None)
    status: Literal['user', 'admin'] = Field(default=None)
    email: EmailStr = Field(default=None)


app = FastAPI(description='CRUD application')

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)



@app.get(
    path='/users', 
    description='Get all users',
    tags=['Get method'],
    dependencies=[Depends(security.access_token_required)]
    )
def get_users():
    db = ConnectionDb().connect(cursor_factory=RealDictCursor)  
    users = SelectUser().all_users(db)
    json = jsonable_encoder(users)
    return JSONResponse(content={ind: el for ind, el in enumerate(json)})


@app.get(
    path='/user/{id}',
    description='Get user by id',
    tags=['Get method']
    )
def get_user(id):
    db = ConnectionDb().connect(cursor_factory=RealDictCursor)
    user = SelectUser.select(db, id)
    json = jsonable_encoder(user)
    return JSONResponse(content=json)


@app.post(
    path='/registration', 
    description='Create new profile to db',
    tags=['Post method']
    )
def registration(user: UserSchema):
    db = ConnectionDb().connect()
    InsertUser().insert_all(db, dict(user))
    return JSONResponse(status_code=200, content={'info': 'Create new profile to db', 'status': 200})


@app.post(
    path='/login',
    description='Authentication user',
    tags=['Post method']
    )
def login(user: UserSchema):
    db = ConnectionDb().connect(cursor_factory=RealDictCursor)
    user_data = SelectUser.by_login(db, user.login)
    
    if user_data['password'] == user.password:
        token = security.create_access_token(uid='12345')
        response = JSONResponse({'token': token, 'status': 200, 'result': 'Password True'}, 200)
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return response
        
    raise HTTPException(401, 'Password false')

    
@app.delete(
    path='/delete/{id}', 
    description='Delete user from database',
    tags=['Delete method']
    )
def delete_user(id):
    db = ConnectionDb().connect()
    DeleteUser.by_id(db, id)
    return JSONResponse(content={'status': 200})


@app.api_route(
    path='/update', 
    methods=['put', 'path'], 
    description='Update user to database',
    tags=['Update method']
    )
def update_user(user: UserSchema):
    db = ConnectionDb().connect()
    UpdateUser.by_id(db, dict(user))
    return JSONResponse(content=jsonable_encoder(user))



    


