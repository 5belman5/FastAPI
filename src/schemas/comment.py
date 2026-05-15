from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    post_id: int

class Comment(CommentBase):
    id: int
    created: datetime
    author_id: int
    post_id: int

    model_config = ConfigDict(from_attributes=True)
