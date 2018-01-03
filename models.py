from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
import random
import string


Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits)
                     for x in range(32))


class User(Base):
    """User entity"""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False)
    picture = Column(String)
    email = Column(String, index=True, nullable=False)
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Category(Base):
    """Category entity"""
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    @property
    def serialize(self):
        """Return object data in easily serializabale format"""
        return {
            'id': self.id,
            'name': self.name
        }


class Item(Base):
    """Item entity"""
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    description = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        """Return object data in easily serializabale format"""
        return {
            'Item id': self.id,
            'Item name': self.name,
            'Item description': self.description,
            'Item Cat_Id': self.category_id
        }


engine = create_engine('sqlite:///itemCatalogs.db')

Base.metadata.create_all(engine)
