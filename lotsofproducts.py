from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from models import *

engine = create_engine('sqlite:///product.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Delete Categories if exisitng.
session.query(Category).delete()
# Delete Items if exisitng.
session.query(Items).delete()
# Delete Users if exisitng.
session.query(User).delete()

# Create fake users
User1 = User(username="Jay Norman", email="abc@efg.com")
session.add(User1)
session.commit()


# Create fake categories
Category1 = Category(name="Football",
                      user_id=1)
session.add(Category1)
session.commit()

Category2 = Category(name="Cars",
                      user_id=2)
session.add(Category2)
session.commit

Category3 = Category(name="Snacks",
                      user_id=1)
session.add(Category3)
session.commit()

Category4 = Category(name="Gadgets",
                      user_id=1)
session.add(Category4)
session.commit()

Category5 = Category(name="Food",
                      user_id=1)
session.add(Category5)
session.commit()

# Populate a category with items for testing
# Using different users for items also
Item1 = Items(name="Football Boots",
               dateCreated=datetime.datetime.now(),
               description="Shoes to play football in.",
               image="http://bit.ly/2qHbHxd",
               category_id=1,
               user_id=1)
session.add(Item1)
session.commit()

Item2 = Items(name="Football Shirt",
               dateCreated=datetime.datetime.now(),
               description="Shirt to play football in.",
               image="http://bit.ly/2pb59qn",
               category_id=1,
               user_id=1)
session.add(Item2)
session.commit()

Item3 = Items(name="Football",
               dateCreated=datetime.datetime.now(),
               description="A Football.",
               image="http://bit.ly/2pJSPR1",
               category_id=1,
               user_id=1)
session.add(Item3)
session.commit()

print "Your database has been populated with fake data!"
