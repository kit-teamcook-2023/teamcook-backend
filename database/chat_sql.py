import pymysql as sql
import os
from dotenv import load_dotenv
import datetime

class ChatSQL():
    def __init__(self):
        load_dotenv(verbose=True)
        self._connect_database()
        
    def __del__(self):
        self._con.close()

    def _connect_database(self):
        try:
            self._con.close()
        except:
            None
            
        self._con = sql.connect(
                host='localhost', 
                user=os.getenv("MYSQL_ID"), 
                password=os.getenv("MYSQL_PW"), 
                db=os.getenv("MYSQL_DB_CHAT"), 
                charset='utf8mb4'
            )

    def healthcheck(func):
        def wrapper(self, *args, **kwargs):
            try:
                self._con.ping()
            except sql.OperationalError as e:
                if e.args[0] == 2006:
                    self._connect_database()
            return func(self, *args, **kwargs)
        return wrapper

    @healthcheck
    # 메시지 백업
    def backup_message(self, room_address: str, message: str, sender: str):
        try:
            with self._con.cursor() as cursor:
                # chat_log 테이블에 메시지 백업
                sql = "INSERT INTO chat_log (room_name, message, sender) VALUES (%s, %s, %s)"
                cursor.execute(sql, (room_address, message, sender))
            self._con.commit()
        except Exception as e:
            print(f"Error occurred during message backup: {e}")
            self._con.rollback()

    @healthcheck
    def room_exisits(self, room_address: str) -> bool:
        with self._con.cursor() as cursor:
            sql = f"""SELECT COUNT(*) FROM room_info WHERE `room_name`='{room_address}'"""
            cursor.execute(sql)
            res = cursor.fetchone()
        return True if res[0] == 1 else False

    @healthcheck
    def create_room(self, room_address: str):
        try:
            with self._con.cursor() as cursor:
                sql = f"""INSERT INTO room_info(room_name) VALUES ('{room_address}')"""
                cursor.execute(sql)
            self._con.commit()
        except:
            None

    @healthcheck
    def get_previous_chat(self, chatting_room_id: str):
        try:
            res = []
            with self._con.cursor() as cursor:
                sql = f"""SELECT * FROM chat_log WHERE `room_name`='{chatting_room_id}'"""
                cursor.execute(sql)
                chats = cursor.fetchall()

                for chat in chats:
                    res.append({
                        "sender": chat[2],
                        "message": chat[3],
                        "time": chat[4]
                    })
        except:
            pass
        return res