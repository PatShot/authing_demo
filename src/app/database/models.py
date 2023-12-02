from sqlalchemy import TIMESTAMP, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email= Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    name = Column(String)
    display_handle = Column(String, default="user")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class ToDoTask(Base):
    __tablename__ = "todo"
    task_id = Column(Integer, primary_key=True, nullable=False)
    task_name = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(TIMESTAMP(timezone=True), nullable=False)
    priority = Column(Integer)
    status = Column(String, default="Pending")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
