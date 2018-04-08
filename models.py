from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
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
    username = Column(String(32), index=True)
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
class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
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
        'category' : self.category,
        'price' : self.price,
        }

####### INSERT AT THE END OF FILE #######
engine = create_engine('sqlite:///product.db')
Base.metadata.create_all(engine)
