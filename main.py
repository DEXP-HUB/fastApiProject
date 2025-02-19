from DataBase.postgre_sql import ConnectionDb, SelectUser, InsertUser, DeleteUser, UpdateUser
from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from psycopg2.extras import RealDictCursor


app = FastAPI()


@app.get('/users')
def get_users():
    db = ConnectionDb().connect(cursor_factory=RealDictCursor)  
    users = SelectUser().select_all(db)
    json = jsonable_encoder(users)
    return JSONResponse(content={ind: el for ind, el in enumerate(json)})

    
@app.post('/insert')
def insert_user(data=Body()):
    db = ConnectionDb().connect()
    InsertUser().insert_all(db, data)
    return JSONResponse(content={'status': 200})


@app.delete('/delete/{id}')
def delete_user(id):
    db = ConnectionDb().connect()
    DeleteUser.delete_by_id(db, id)
    return JSONResponse(content={'status': 200})


@app.put('/update')
def update_user(data=Body()):
    db = ConnectionDb().connect()
    UpdateUser.update_by_id(db, data)
    return JSONResponse(content={'status': 200})
    
    


