from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Product

engine = create_engine('sqlite:///product.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

# A DBSession() instance established all conversations with the  database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you are not happy about the changes, you can
# revert all of them back to the last commit by calling session.rollback()
session = DBSession()

# 1 veggie
cilantro = Product(name="Cilantro", category="Vegetables", description="A delicious veggie suits for any type of cooking.")

session.add(cilantro)
session.commit()

# 1 veggie
napa = Product(name="Napa Cabbage", category="Vegetables", description="Napa cabbage is suits for mainly soup as it has a sweet tastes infused in it.")

session.add(napa)
session.commit()

# 2 meat
ribeye = Product(name="Ribeye Steak", category="Meats", description="A very juicy cut of beef.")

session.add(ribeye)
session.commit()

# 2 meat
porkshoulder = Product(name="Pork Shoulder Blade", category="Meats", description="Very high fat cut of pork, suits for anything but being healthy.")

session.add(porkshoulder)
session.commit()

# 3 bread
bagel = Product(name="Bagel", category="Breads", description="Best for everyday's morning.")

session.add(bagel)
session.commit()

# 3 bread
whitebread = Product(name="White Bread", category="Breads", description="A generic white bread with nothing special about it.")

session.add(whitebread)
session.commit()

# 4 snack
cookie = Product(name="Cookie", category="Snacks", description="A generic cookie, but very delicious one at that.")

session.add(cookie)
session.commit()

# 5 dairies
milk = Product(name="Milk", category="Dairies", description="A delectable milk, from a delectable cows.")

session.add(milk)
session.commit()

# 6 fish
salmon = Product(name="Salmon", category="Fish", description="Anarctica cought salmon, not sure how it could get that far south.")

session.add(salmon)
session.commit()

# 7 spice
oregano = Product(name="Oregano", category="Spices", description="Oregano is perfect with Italian cuisine.")

session.add(oregano)
session.commit()

# 8 canned food
tuna = Product(name="Tuna Can", category="Canned Food", description="These canned food will stay tasty for centuries to come.")

session.add(tuna)
session.commit()


print("Add Many Products")
