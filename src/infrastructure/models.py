from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'auth_user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    email = Column(String(254), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(150))
    last_name = Column(String(150))
    is_staff = Column(Integer, default=0)
    is_active = Column(Integer, default=1)
    is_superuser = Column(Integer, default=0)
    last_login = Column(DateTime)
    date_joined = Column(DateTime, default=datetime.utcnow)

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")

class Group(Base):
    __tablename__ = 'posts_group'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)

    posts = relationship("Post", back_populates="group")

class Post(Base):
    __tablename__ = 'posts_post'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    pub_date = Column(DateTime, default=datetime.utcnow, index=True)
    author_id = Column(Integer, ForeignKey('auth_user.id'), nullable=False)
    group_id = Column(Integer, ForeignKey('posts_group.id'))
    image = Column(String(100))

    author = relationship("User", back_populates="posts")
    group = relationship("Group", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = 'posts_comment'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created = Column(DateTime, default=datetime.utcnow, index=True)
    author_id = Column(Integer, ForeignKey('auth_user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts_post.id'), nullable=False)

    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

class Follow(Base):
    __tablename__ = 'posts_follow'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('auth_user.id'), nullable=False)
    following_id = Column(Integer, ForeignKey('auth_user.id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'following_id', name='unique_follow'),
    )
