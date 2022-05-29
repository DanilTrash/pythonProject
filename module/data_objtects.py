import os
import sqlite3
from dataclasses import dataclass
from random import choice
from typing import Optional


@dataclass
class Account:
    username: str
    password: str
    phone: str
    user_agent: str = None
    proxy: Optional[str] = None


class Database:
    def __init__(self):
        self.con = sqlite3.connect(r'C:\Users\KIEV-COP-4\Desktop\twitter_project\database.sqlite')
        self.cur = self.con.cursor()

    def select(self, query: str):
        self.cur.execute(query)
        return self.cur.fetchall()

    def selectone(self, query: str):
        self.cur.execute(query)
        return self.cur.fetchone()

    def update(self, query: str):
        pass

    def insert(self, query: str):
        pass

    def delete(self, query: str):
        pass


def random_photo() -> str:
    storage_path = r'C:\Users\KIEV-COP-4\Pictures\images'
    return rf'{storage_path}\{choice(os.listdir(storage_path))}'


def generated_text() -> str:
    db = Database()
    captions = db.select('select distinct  caption from posting_data_oae where caption is not null')
    locations = db.select('select distinct  location from posting_data_oae where location is not null')
    tags = db.select('select distinct hashtags from posting_data_oae where hashtags is not null')

    tweet = None
    while tweet is None:
        caption = choice(captions)[0]
        location = choice(locations)[0]
        tweet_tags = [choice(tags)[0] for _ in range(5)]
        result = '\n'.join([caption, location] + tweet_tags)
        if len(result) < 280:
            tweet = result
    return tweet


class Post:
    text: str = None
    photo_path: str = None

    def __init__(self):
        self.photo_path: str = random_photo()
        self.text: str = generated_text()

    def __repr__(self) -> str:
        return f'photo_path={self.photo_path}\n\n{self.text}'
