from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmake
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()
# Generate secret key
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

# Users database
class User(Base)
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    username = Column(string(32), index=True)
    email = Column(String)
    password_hash = Column(String(64))

    # Encrypt the password
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    # Uses for verify password
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    # Genrate token with expiration time

    # Use for verify auth token

# Product database
class Product(Base):
    __tablename__ = 'product'

    id = column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    # JSON API inside Object database class
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
        'name' : self.name,
        'category' : self.category
        'price' : self.price
        }

####### INSERT AT THE END OF FILE #######
engine = create_engine('sqlite:///product.db')
Base.metadata.create_all(engine)
