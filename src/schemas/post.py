from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    text: str
    group_id: Optional[int] = None

    @field_validator('text')
    @classmethod
    def text_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Text must not be empty')
        return v

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    text: Optional[str] = None

class Post(PostBase):
    id: int
    pub_date: datetime
    author_id: int
    image: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
