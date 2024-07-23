from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.responses import Response
from datetime import datetime, timedelta
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from service.account_service import AccountService
from service.errors.account import AccountAlreadyRegister
from extensions.ext_redis import redis_client
from config import cfg
from model.account import Account, AccountStatus


class User(BaseModel):
    email: str
    password: str
    remember_me: bool = True

router = APIRouter(
    prefix='',
    tags = ['auth']
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")


@router.post("/login")
async def login_for_access_token(user: User):
    try:
        account = AccountService.authenticate(email=user.email, password=user.password)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=cfg.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AccountService.create_access_token(
        data={"user_id": account.user_id}, expires_delta=access_token_expires
    )
    return {
        'result': 'success',
        'data': access_token
    }

@router.post('/signup')
def register_for_new_account(name: str, email: str, password: str):
    try:
        account = AccountService.create_account(email, name, password)
        access_token_expires = timedelta(minutes=cfg.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AccountService.create_access_token(
                data={"user_id": account.user_id}, expires_delta=access_token_expires
            )
        return {
            'result': 'success',
            'data': access_token
        }
    except AccountAlreadyRegister:
        return Response(content="User already exists",
                        status_code=status.HTTP_409_CONFLICT,
                        media_type="text/plain",
                        )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    print("token", print(token))
    account = AccountService.decode_access_token(token)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return account


async def get_current_active_user(
    account: Annotated[Account, Depends(get_current_user)],
):
    if account.status == AccountStatus.CLOSED.value:
        raise HTTPException(status_code=400, detail="Inactive user")
    return account