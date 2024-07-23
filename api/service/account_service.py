import secrets
import base64
import uuid
import jwt
from werkzeug.exceptions import Unauthorized
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext

from config import cfg
from model.account import Account, AccountStatus
from service.errors.account import (
    AccountLoginError,
    AccountAlreadyRegister
)



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


class AccountService:
    @staticmethod
    def create_account(email: str,
                       name: str,
                       password: str = None,
                       ) -> Account:
        """create account"""
        if Account.by_email(email) is not None:
            raise AccountAlreadyRegister(f"Accoutn {email} has already register")
        account = Account()
        account.email = email
        account.name = name

        if password:
            # generate password salt
            salt = secrets.token_bytes(16)
            base64_salt = base64.b64encode(salt).decode()

            # encrypt password with salt
            password_hashed = get_password_hash(password)
            account.password = password_hashed
            account.password_salt = base64_salt
        account.user_id = "valor:{}".format(uuid.uuid4())
        account.status = AccountStatus.UNINITIALIZED.value
        account.initialized_at = datetime.now()
        account.last_active_at = datetime.now()
        account.add()
        return account

    @staticmethod
    def authenticate(email: str, password: str) -> Account:
        """authenticate account with email and password"""
        account = Account.by_email(email)
        if not account:
            raise AccountLoginError('Invalid email or password.')
        if account.status == AccountStatus.BANNED.value or account.status == AccountStatus.CLOSED.value:
            raise AccountLoginError('Account is banned or closed.')

        if account.status == AccountStatus.PENDING.value:
            account.status = AccountStatus.ACTIVE.value
            account.initialized_at = datetime.now(timezone.utc).replace(tzinfo=None)
            account.update()

        if account.password is None or not verify_password(password, account.password):
            raise AccountLoginError('Invalid email or password.')
        return account

    @staticmethod
    def create_access_token(data: dict, expires_delta = timedelta(minutes=300)):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=300)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cfg.SECRET_KEY, algorithm=cfg.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_access_token(access_token: str):
        try:
            return jwt.decode(access_token, cfg.SECRET_KEY, algorithms=cfg.ALGORITHM)
        except jwt.exceptions.InvalidSignatureError:
            raise Unauthorized('Invalid token signature.')
        except jwt.exceptions.DecodeError:
            raise Unauthorized('Invalid token.')
        except jwt.exceptions.ExpiredSignatureError:
            raise Unauthorized('Token has expired.')

    
    @staticmethod
    def load_user(user_id: str) -> Account:
        account = Account.by_user_id(user_id)
        if not account:
            return None

        if account.status in [AccountStatus.BANNED.value, AccountStatus.CLOSED.value]:
            raise Unauthorized("Account is banned or closed.")

        if datetime.now(timezone.utc).replace(tzinfo=None) - account.last_active_at > timedelta(minutes=10):
            account.last_active_at = datetime.now(timezone.utc).replace(tzinfo=None)
            account.update()

        return account
