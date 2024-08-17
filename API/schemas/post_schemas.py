from datetime import datetime

from ninja import Schema


class PostIn(Schema):
    title: str
    content: str


class PostOut(Schema):
    id: int
    author: str
    title: str
    content: str
    created_at: datetime
