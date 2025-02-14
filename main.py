from DataBase.postgre_sql import PostgreSql
from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from psycopg2.extras import RealDictCursor


app = FastAPI()


@app.get('/users')
def get_users():
    db = PostgreSql(
        'registration', 
        'postgres', 
        'lola2015', 
        '127.0.0.1', 
        '5432', 
        RealDictCursor
    )
    users = db.select("SELECT * FROM users.profiles;")
    json = jsonable_encoder(users)
    return JSONResponse(content=json)

    
@app.post('/insert')
def insert_user(data=Body()):
    db = PostgreSql(
        'registration', 
        'postgres', 
        'lola2015', 
        '127.0.0.1', 
        '5432'
    )
    db.insert(data)
    return JSONResponse(content={'status': 200})

