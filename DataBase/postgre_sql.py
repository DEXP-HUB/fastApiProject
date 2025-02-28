import psycopg2


class ConnectionDb:
    def connect(self, cursor_factory=None):
        self.conn = psycopg2.connect(
            dbname='registration', 
            user='postgres', 
            password='lola2015', 
            host='127.0.0.1', 
            port='5432',
            cursor_factory=cursor_factory
        )
        
        return self.conn
    

class SelectUser:
    @classmethod
    def select_all(cls, connect):
        cls.conn = connect

        with cls.conn as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users.profiles;")
                result = cur.fetchall()

        return result
    

    @classmethod
    def select(cls, connect, id):
        cls.conn = connect
        cls.id = id

        with cls.conn as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM users.profiles WHERE id = {cls.id};")
                result = cur.fetchone()

        return result

    

class InsertUser:
    @classmethod
    def insert_all(cls, connect, data):
        cls.conn = connect

        with cls.conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users.profiles (
                        first_name, last_name, email, status, city,
                        address, age, floor, apartament_number, data_registratsii
                    ) VALUES (
                        %(first_name)s, %(last_name)s, %(email)s,
                        %(status)s, %(city)s, %(address)s, %(age)s,
                        %(floor)s, %(apartament_number)s, %(data_registratsii)s
                    )
                    """, data
                )


class DeleteUser:
    @classmethod
    def by_id(cls, connect, id):
        cls.conn = connect

        with cls.conn as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM users.profiles WHERE id = {id};")


class UpdateUser:
    @classmethod
    def by_id(cls, connect, data):
        cls.conn = connect
        param = [f"{key} = %({key})s" for key in data.keys() if key != 'id']

        with cls.conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"UPDATE users.profiles SET {', '.join(param)} WHERE id = %(id)s;", data
                )

  

