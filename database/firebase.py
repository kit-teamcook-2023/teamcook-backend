# 민감한 정보를 가리기 위해 .env 활용
import os
from dotenv import load_dotenv

# firebase 사용을 위한 패키지 import
import firebase_admin
from firebase_admin import credentials, db, auth

# 현재 시각을 알 수 있는 패키지
from datetime import datetime

class Firebase:
    def __init__(self):
        load_dotenv(verbose=True)

        DB_URL=os.getenv("DB_URL")

        self._cred = credentials.Certificate('serviceAccountKey.json')
        firebase_admin.initialize_app(self._cred, {
            'databaseURL' : DB_URL
        })
        
        # self.dir = db.reference()

    def get_nickname(self, uid:str):
        user = auth.get_user(uid)
        return user.display_name

    def get_user_kakao(self, uid:str):
        try:
            nickname = self.get_nickname(uid)
            return True, nickname
        except:
            return False, ""

    def create_user(self, data: dict):
        uid = data['uid']
        nickname = data['nickname']

        try:
            user = auth.create_user(uid=uid)
            user_info = {
                'display_name': nickname,
                'custom_claims': {
                    'provider': 'kakao',
                    'image': 'https://www.kakaocorp.com/page/favicon.ico'
                },
            }
            auth.update_user(user.uid, **user_info)
        except:
            None
        
    def update_user(self, uid, nickname):
        user = auth.get_user(uid)
        print(uid)
        user_info = {
            'display_name': nickname,
            'custom_claims': {
                'provider': 'kakao',
                'image': 'https://www.kakaocorp.com/page/favicon.ico'
            },
        }
        auth.update_user(user.uid, **user_info)

    def delete_user(self, uid:str):
        try:
            db.reference(uid).delete()
            auth.delete_user(uid)
            return True
        except:
            return False


    # push data to firebase database
    # 회원가입 시 db에 저장되도록 함
    # def push(self, uid, type='', data='', date='', nickname=''):
    def push(self, uid, type, data):
        data_ref = db.reference(uid)

        # 테스트를 위해 yy-mm-dd-HH 시간 형식을 key값으로 활용
        # if date == '':
        #     date = datetime.today().strftime('%y-%m-%d-%H')

        if type == "gas":
            # date = data[0]
            # data = data[1]
            # if date == '':
            date = datetime.today().strftime('%y-%m-%d-%H')
            date_ref = data_ref.child(date)
            date_ref.child('gas').set(data)
        elif type == "elec":
            # date = data[0]
            # data = data[1]
            # if date == '':
            date = datetime.today().strftime('%y-%m-%d-%H')
            date_ref = data_ref.child(date)
            date_ref.child('elec').set(data)
        elif type == "ip":
            data_ref.child("ip").set(data)
        elif type == "nickname":
            data_ref.child("nickname").set(data)
        
    def push_nickname(self, nickname):
        data_ref = db.reference('nicknames')
        data_ref.child(nickname).set('')


    def setRating(self, data, date):
        key = 'rating'
        rating_ref = db.reference(key)
        date_ref = rating_ref.child(date)
        date_ref.set(data)


    # remove all user-data from firebase database
    def delete(self, uid):
        # 회원이 탈퇴하면 해당 유저의 data 모조리 삭제
        # data_ref = db.reference(uid)
        # data_ref.remove()

        # 코드 테스트 용도로 child만 삭제하도록 함
        data_ref = db.reference(uid)
        elec_ref = data_ref.child('elec')
        elec_ref.delete()

        auth.delete_user(uid)

    # search data witch front-end want
    def search(self, uid, month):
        data_ref = db.reference(uid)
        date_ref = data_ref.child(month)

        ret_data = {
            'gas': date_ref.child('gas').get(),
            'elec': date_ref.child('elec').get()
        }

        return ret_data

    def search_nickname(self, nickname):
        data_ref = db.reference('nicknames')
        data = data_ref.get().keys()

        if nickname in data:
            return True
        else:
            return False

    # only use at test
    def get_all(self):
        dir = db.reference()
        return dir.get()

    def get_user_ip(self, uid: str) -> str:
        dir = db.reference(uid)
        ip = dir.child("ip").get()
        ip = ip if ip[0:4] == "http" else "http://" + ip
        return ip

    def set_user_ip(self, uid: str, ip: str):
        dir = db.reference(uid)
        dir.child("ip").set(ip)

    def clear(self):
        dir = db.reference('test')
        dir.delete()