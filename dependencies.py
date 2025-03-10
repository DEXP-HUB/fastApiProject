from fastapi import HTTPException
from DataBase.postgre_sql import ConnectionDb
from Schemes.by_users import UserLoginSchema
from DataBase.postgre_sql import SelectUser
from psycopg2.extras import RealDictCursor


def auntification(login: str = UserLoginSchema, password: str = UserLoginSchema):
    db = ConnectionDb().connect(cursor_factory=RealDictCursor)
    user_data = SelectUser.by_login(db, login)

    if user_data == None or user_data['password'] != password:
        raise HTTPException(401, {'auntification': 'Incorrect password or login', 'status': 401})

    