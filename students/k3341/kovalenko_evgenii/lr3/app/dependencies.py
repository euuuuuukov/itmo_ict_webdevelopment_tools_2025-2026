from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from connection import get_session
from security import decode_access_token
from models import User


security = HTTPBearer()


def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security),
                     session: Session = Depends(get_session)) -> User:
    token = creds.credentials

    try:
        user_id = decode_access_token(token).get('sub')
        if user_id is None:
            raise HTTPException(status_code=401, detail='invalid token')
    except Exception as exc:
        print(f"Decode error: {exc}")
        raise HTTPException(status_code=401, detail='invalid token')

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='user not found')

    return user
