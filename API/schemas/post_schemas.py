from datetime import datetime
from typing import List

from ninja import Schema

from .comment_schemas import CommentOut
from .user_schema import UserOut


class PostIn(Schema):
    title: str
    content: str


class PostOut(Schema):
    id: int
    author: UserOut
    title: str
    content: str
    created_at: datetime
    comments: List[CommentOut] = []

    class Config:
        from_attributes = True
