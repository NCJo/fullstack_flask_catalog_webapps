import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()
# Generate secret key
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

# Users database
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    email = Column(String)
    password_hash = Column(String(64))

    # Encrypt the password
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    # Uses for verify password
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    # Generate token with expiration time
    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in = expiration)
        return s.dumps({'id': self.id })

    # Use for verify auth token
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid token, but expired
            return None
        except BadSignature:
            return None
        user_id = data['id']
        return user_id

# Product database
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="category")

    # JSON API inside Object database class
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
        'name' : self.name,
        'id' : self.id
        }

# Item Database
class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    dateCreated = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    description = Column(String(250))
    image = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    # When pass assign value to 'category', must pass a query object through it because of 'relationship'
    # Can access name of category by: item.category.name
    category = relationship(Category)
    # Mainly use for verify the ownership of item (for editing, deleting)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
        'name': self.name,
        'id': self.id,
        'description': self.description,
        'user_id': self.user_id
        }

####### INSERT AT THE END OF FILE #######
engine = create_engine('sqlite:///product.db')
Base.metadata.create_all(engine)
