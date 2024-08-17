from datetime import datetime

from ninja import Schema
from typing import List

from .user_schema import UserOut


class CommentIn(Schema):
    content: str


class CommentOut(Schema):
    id: int
    author: UserOut
    content: str
    created_at: datetime
    blocked: bool
    replies: List['CommentOut'] = []

    class Config:
        from_attributes = True
