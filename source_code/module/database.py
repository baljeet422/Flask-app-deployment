import os
import pymysql
import json
from module.redis_client import redis_client


class Database:
    def connect(self):
        return pymysql.connect(  host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        charset="utf8mb4")

    def read(self, id):
        #redis
        cache_key = f"phonebook:{id}"

        cached_data = redis_client.get(cache_key)

        if cached_data:
            print("Serving from Redis Cache")
            return json.loads(cached_data)

        ###
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM phone_book order by name asc")
            else:
                cursor.execute(
                    "SELECT * FROM phone_book where id = %s order by name asc", (id,))

            result = cursor.fetchall()

            redis_client.setex(
                cache_key,
                300,
                json.dumps(result, default=str)
            )

            return result
        except:
            return ()
        finally:
            con.close()

    def insert(self, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO phone_book(name,phone,address) VALUES(%s, %s, %s)",
                           (data['name'], data['phone'], data['address'],))
            con.commit()
            ###
            redis_client.delete("phonebook:all")
            ###

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def update(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE phone_book set name = %s, phone = %s, address = %s where id = %s",
                           (data['name'], data['phone'], data['address'], id,))
            con.commit()
          ###
            redis_client.delete(f"phonebook:{id}")
           ###
            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def delete(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM phone_book where id = %s", (id,))
            con.commit()
            ####
            redis_client.delete(f"phonebook:{id}")
            ###

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()
