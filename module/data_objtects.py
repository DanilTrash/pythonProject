from faker import Faker
from typing import Optional


class Account:
    username: str
    password: str
    user_agent: str = Faker().chrome()
    proxy: Optional[str] = None


class Post:
    pass


