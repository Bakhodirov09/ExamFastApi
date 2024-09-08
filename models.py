from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text


class UsersModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, null=True)
    phone_number = Column(String, null=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    gander = Column(String, default='MAN')
    role = Column(String)


class BooksModel(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text, nullable=True)
    creator_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

class WishListModel(Base):
    __tablename__ = 'wish-list'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'))
