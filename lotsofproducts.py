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
User1 = User(username="Yames Datalover", email="abc@efg.com")
session.add(User1)
session.commit()


# Create fake categories
Category1 = Category(name="Game",
                      user_id=1)
session.add(Category1)
session.commit()

Category2 = Category(name="Sport",
                      user_id=2)
session.add(Category2)
session.commit

Category3 = Category(name="Food",
                      user_id=1)
session.add(Category3)
session.commit()

Category4 = Category(name="Car",
                      user_id=1)
session.add(Category4)
session.commit()

Category5 = Category(name="Furniture",
                      user_id=1)
session.add(Category5)
session.commit()

# Populate a category with items for testing
# Using different users for items also
Item1 = Items(name="Sim Tower",
               dateCreated=datetime.datetime.now(),
               description="SimTower allows the player to build and manage the operations of a modern, multi-use skyscraper. They must plan where to place facilities in the tower that include restaurants, condominiums, offices, hotel rooms, retail stores and elevators.",
               category_id=1,
               user_id=1)
session.add(Item1)
session.commit()

Item2 = Items(name="Sim Ant",
               dateCreated=datetime.datetime.now(),
               description="SimAnt, the player plays the role of an ant in a colony of black ants in the back yard of a suburban home. The ant colony must battle against enemy red ants. The ultimate goal is to spread throughout the garden, into the house, and finally to drive out the red ants and human owners.",
               category_id=1,
               user_id=1)
session.add(Item2)
session.commit()

Item3 = Items(name="Sim Town",
               dateCreated=datetime.datetime.now(),
               description="The game structure of SimTown is similar to SimCity, but on a generally smaller and simplified scale, where players are tasked to craft a small town instead. Players are allocated a blank and flat tract of land, where they will be required to place homes, workplaces and civic buildings.",
               category_id=1,
               user_id=1)
session.add(Item3)
session.commit()

##############################

Item4 = Items(name="Tennis",
               dateCreated=datetime.datetime.now(),
               description="Best way to ensure optimal performance, aside from practice and matches. This is why we at Midwest Sports stocks such a mammoth collection. We want you to find the best racquet for your game. Select among technical options including head size, weight, and balance. Do you prefer comfort, control or power? You can also browse by price and brand.",
               category_id=2,
               user_id=1)
session.add(Item4)
session.commit()


Item5 = Items(name="Basketball",
               dateCreated=datetime.datetime.now(),
               description="Basketball is a limited-contact sport played on a rectangular court. While most often played as a team sport with five players on each side, three-on-three, two-on-two, and one-on-one competitions are also common.",
               category_id=2,
               user_id=1)
session.add(Item5)
session.commit()

Item6 = Items(name="Swimming",
               dateCreated=datetime.datetime.now(),
               description="Swimming is the self-propulsion of a person through fresh or salt water, usually for recreation, sport, exercise, or survival.",
               category_id=2,
               user_id=1)
session.add(Item6)
session.commit()

##############################

Item7 = Items(name="Hamburger",
               dateCreated=datetime.datetime.now(),
               description="A hamburger, beefburger or burger is a sandwich consisting of one or more cooked patties of ground meat, usually beef, placed inside a sliced bread roll or bun.",
               category_id=3,
               user_id=1)
session.add(Item7)
session.commit()


Item8 = Items(name="Fries",
               dateCreated=datetime.datetime.now(),
               description="French fries (North American English), chips (British and Commonwealth English),[1] finger chips (Indian English),[2] or French-fried potatoes are batonnet or allumette-cut deep-fried potatoes",
               category_id=3,
               user_id=1)
session.add(Item8)
session.commit()

Item9 = Items(name="Ramen",
               dateCreated=datetime.datetime.now(),
               description="a Japanese dish. It consists of Chinese-style wheat noodles served in a meat or (occasionally) fish-based broth, often flavored with soy sauce or miso, and uses toppings such as sliced pork.",
               category_id=3,
               user_id=1)
session.add(Item9)
session.commit()

##############################
Item10 = Items(name="Toyota",
               dateCreated=datetime.datetime.now(),
               description="Toyota is the world's market leader in sales of hybrid electric vehicles, and one of the largest companies to encourage the mass-market adoption of hybrid vehicles across the globe. Cumulative global sales of Toyota and Lexus hybrid passenger car models.",
               category_id=4,
               user_id=1)
session.add(Item10)
session.commit()


Item11 = Items(name="Honda",
               dateCreated=datetime.datetime.now(),
               description="Honda has been the world's largest motorcycle manufacturer since 1959,[2][3] as well as the world's largest manufacturer of internal combustion engines measured by volume, producing more than 14 million internal combustion engines each year.[4] Honda became the second-largest Japanese automobile manufacturer",
               category_id=4,
               user_id=1)
session.add(Item11)
session.commit()

Item12 = Items(name="Nissan",
               dateCreated=datetime.datetime.now(),
               description="In 2013, Nissan was the sixth largest automaker in the world.",
               category_id=4,
               user_id=1)
session.add(Item12)
session.commit()
##############################
Item13 = Items(name="Bed",
               dateCreated=datetime.datetime.now(),
               description="Most modern beds consist of a soft, cushioned mattress on a bed frame, the mattress resting either on a solid base, often wood slats, or a sprung base.",
               category_id=5,
               user_id=1)
session.add(Item13)
session.commit()


Item14 = Items(name="Chair",
               dateCreated=datetime.datetime.now(),
               description="A chair is a piece of furniture with a raised surface supported by legs, commonly used to seat a single person.",
               category_id=5,
               user_id=1)
session.add(Item14)
session.commit()

Item15 = Items(name="Table",
               dateCreated=datetime.datetime.now(),
               description="A table is an item of furniture with a flat top and one or more legs, used as a surface for working at, eating from or on which to place things.",
               category_id=5,
               user_id=1)
session.add(Item15)
session.commit()
##############################

print "Have fun!"
