from DataBase.postgre_sql import ConnectionDb, SelectUser, InsertUser, DeleteUser, UpdateUser
from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from psycopg2.extras import RealDictCursor


app = FastAPI(description='CRUD application')


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
def insert_user(data=Body()):
    db = ConnectionDb().connect()
    InsertUser().insert_all(db, data)
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
def update_user(data=Body()):
    db = ConnectionDb().connect()
    UpdateUser.by_id(db, data)
    return JSONResponse(content=data)


    
    


