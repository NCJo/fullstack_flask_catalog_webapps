# From database
from models import Base, User, Product

from flask import Flask, jsonify, request, url_for, abort, g, render_template

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, asc, desc

# Google authenticator
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask_httpauth import HTTPBasicAuth
from flask import make_response
import requests
import httplib2
import json

# Login Validation
from flask import session as login_session

### SET UP ###
auth = HTTPBasicAuth()

engine = create_engine('sqlite:///product.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

# CLIENT_ID = json.loads(
#     open('client_secrets.json', 'r').read())['web']['client_id']


# Route /
@app.route('/')
def showCatalog():
    catalog = session.query(Product).order_by(desc(Product.name)).group_by(Product.category)
    return render_template('main.html', catalog = catalog)

# Route /catalog/Meats/items -> show list of items
@app.route('/catalog/<product_category>/items')
def showItems(product_category):
    catalog = session.query(Product).order_by(desc(Product.name)).group_by(Product.category)
    items_list = session.query(Product).filter_by(category = product_category)
    return render_template('showItemsFromCategory.html', catalog = catalog, items = items_list )

# Route /catalog/Meats/Ribeye -> show description of the item
@app.route('/catalog/<product_category>/<item_name>')
def showDescription(product_category, item_name):
    catalog = session.query(Product).order_by(desc(Product.name)).group_by(Product.category)
    item_name = session.query(Product).filter_by(name = item_name)
    return render_template('showItemDescription.html', catalog = catalog, item = item_name)

# Route /catalog/(logged in)
# Route /catalog/Meats/Ribeye/(logged in) -> show edit and delete button
# Route /catalog/Meats/Ribeye/edit/(logged in) -> edit title:description:category
# Route /catalog/Meats/Ribeye/delete(logged in) -> Are you sure you want to delete
# Route /catalog.json -> provide JSON endpoint


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
