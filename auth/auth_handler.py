from datetime import datetime, timedelta
import time
from typing import Dict

import jwt

import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

JWT_SECRET = os.getenv("secret")  # setted in .env
JWT_ALGORITHM = os.getenv("algorithm") # setted in .env

def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(nickname: str, uid: str, timeout: int) -> Dict[str, str]:
    payload = {
        "nickname": nickname,
        "uid": uid,
        "exp": datetime.utcnow() + timedelta(seconds=timeout)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token: dict) -> dict:
    try:
        # token = token['access_token']
        res = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return res
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

if __name__ == "__main__":
    token = signJWT("test2", "102890172904", 30 * 24 * 60 * 60)
    print(token)
    # time.sleep(3)
    print(decodeJWT(token['access_token']))