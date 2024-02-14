import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    db_url: str
    async_db_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str
    test_db_url: str


def load():
    return Config(
        db_url=os.environ['SQLALCHEMY_DATABASE_URL'],
        async_db_url=os.environ['SQLALCHEMY_ASYNC_DATABASE_URL'],
        secret_key=os.environ['SECRET_KEY'],
        algorithm=os.environ['ALGORITHM'],
        access_token_expire_minutes=os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'],
        test_db_url=os.environ['TEST_SQLALCHEMY_DATABASE_URL'],
    )


my_config = load()
