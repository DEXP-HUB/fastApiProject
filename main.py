from typing import Literal
from DataBase.postgre_sql import ConnectionDb, SelectUser, InsertUser, DeleteUser, UpdateUser
from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, Field, EmailStr


app = FastAPI(description='CRUD application')


class UserSchema(BaseModel):
    first_name: str = Field(max_length=15)
    last_name: str = Field(max_length=15)
    city: str = Field(max_length=20)
    address: str = Field(max_length=50)
    age: int = Field(ge=0, le=115)
    floor: int = Field(ge=0, le=163)
    apartament_number: int = Field(ge=0)
    id: int
    data_registratsii: Literal['NOW()']
    status: Literal['user', 'admin']
    email: EmailStr


@app.get(
        path='/users', 
        description='Get all users',
        tags=['Get method']
        )
def get_users():
    db = ConnectionDb().connect(cursor_factory=RealDictCursor)  
    users = SelectUser().select_all(db)
    json = jsonable_encoder(users)
    return JSONResponse(content={ind: el for ind, el in enumerate(json)})

    
@app.post(
        path='/insert', 
        description='Create user to database',
        tags=['Post method']
        )
def insert_user(user: UserSchema):
    db = ConnectionDb().connect()
    InsertUser().insert_all(db, dict(user))
    return JSONResponse(content={'status': 200})


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



    


