import psycopg2


class PostgreSql:
    @classmethod
    def __init__(cls, dbname, user, password, host, port, cursor_factory=None):
        cls.conn = psycopg2.connect(
            dbname=dbname, 
            user=user, 
            password=password, 
            host=host, 
            port=port,
            cursor_factory=cursor_factory
        )


    @classmethod
    def select(cls, respon):
        with cls.conn as conn:
            with conn.cursor() as cur:
                cur.execute(respon)
                result = cur.fetchall()
        return result      


    @classmethod
    def insert(cls, data):
        with cls.conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO users.profiles (
                        first_name, last_name, email, status, city,
                        address, age, floor, apartament_number, data_registratsii
                    ) VALUES (
                        %(first_name)s, %(last_name)s, %(email)s,
                        %(status)s, %(city)s, %(address)s, %(age)s,
                        %(floor)s, %(apartament_number)s, %(data_registratsii)s
                    )""", data
                )
        

