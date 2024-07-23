from typing import Optional
import enum
from pydantic import ConfigDict

from sqlmodel import Field, SQLModel, DateTime, Session, select, AutoString
from extensions.ext_database import engine

class AccountStatus(str, enum.Enum):
    PENDING = 'pending'
    UNINITIALIZED = 'uninitialized'
    ACTIVE = 'active'
    BANNED = 'banned'
    CLOSED = 'closed'


class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(default="")
    name: str = Field(default="")
    password: str = Field(default="")
    email: str = Field(default="")
    password_salt: str = Field(default="")
    status: str = Field(default=None)
    initialized_at: DateTime = Field(default=None, sa_type=AutoString)
    last_active_at: DateTime = Field(default=None, sa_type=AutoString)
    __table_args__ = {'extend_existing': True}
    model_config = ConfigDict(arbitrary_types_allowed=True) 

    @classmethod
    def by_email(cls, email):
        with Session(bind=engine) as sess:
            statement = select(cls).where(cls.email == email)
            account = sess.exec(statement).first()
            return account

    @classmethod
    def by_user_id(cls, user_id):
        with Session(bind=engine) as sess:
            statement = select(cls).where(cls.user_id == user_id)
            account = sess.exec(statement).first()
            return account

    @classmethod
    def all(cls, session):
        return session.exec(select(cls)).all()

    def add(self):
        with Session(bind=engine) as sess:
            sess.add(self)
            sess.commit()
            sess.refresh(self)
    
    def update(self):
        with Session(bind=engine) as sess:
            sess.add(self)
            sess.commit()
            sess.refresh(self) 

SQLModel.metadata.create_all(engine)