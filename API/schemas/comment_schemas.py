from datetime import datetime

from ninja import Schema


class CommentIn(Schema):
    content: str


class CommentOut(Schema):
    id: int
    author: str
    content: str
    created_at: datetime
    blocked: bool
