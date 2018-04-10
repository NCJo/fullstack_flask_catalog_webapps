# From database
from models import Base, User, Product

from flask import Flask, jsonify, request, url_for, abort, g, render_template, redirect, flash
import os
import random, string

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

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

####### OAUTH2 GOOGLE Login #######
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('clientOauth.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    """ Handles the Google+ sign-in process on the server side.
    Server side function to handle the state-token and the one-time-code
    send from the client callback function following the seven steps of the
    Google+ sign-in flow. See the illustrated flow on
    https://developers.google.com/+/web/signin/server-side-flow.
    Returns:
        When the sign-in was successful, a html response is sent to the client
        signInCallback-function confirming the login. Otherwise, one of the
        following responses is returned:
        200 OK: The user is already connected.
        401 Unauthorized: There is either a mismatch between the sent and
            received state token, the received access token doesn't belong to
            the intended user or the received client id doesn't match the web
            apps client id.
        500 Internal server error: The access token inside the received
            credentials object is not a valid one.
    Raises:
        FlowExchangeError: The exchange of the one-time code for the
            credentials object failed.
    """
    # Confirm that the token the client sends to the server matches the
    # state token that the server sends to the client.
    # This roundship verification helps ensure that the user is making the
    # request and and not a maliciousscript.
    # Using the request.args.get-method, the code examines the state token
    # passed in and compares it to the state of the login session. If thesse
    # two do not match, a response message of an invalid state token is created
    # and returned to the client. No further authentication will occur on the
    # server side if there was a mismatch between these state token.
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid State Token'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # If the above statement is not true -> proceed and collect the
    # one-time code from the server with the request.data-function.
    code = request.data
    # 5) The Server tries to exchange the one-time code for an access_token and
    # an id_token (credentials object).
    # 6) When successful, Google returns the credentials object. Then the
    # server is able to make its own API calls, which can be done while the
    # user is offline.
    try:
        # Create an oauth_flow object and add clients secret key information
        # to it.
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        # Postmessage specifies that this is the one-time-code flow that my
        # server will be sending off
        oauth_flow.redirect_uri = 'postmessage'
        # The exchange is initiated with the step2_exchange-function passing in
        # the one-time code as input.
        # The step2_exchange-function of the flow-class exchanges an
        # authorization (one-time) code for an credentials object.
        # If all goes well, the response from Google will be an object which
        # is stored under the name credentials.
        credentials = oauth_flow.step2_exchange(code)
    # If an error happens along the way, then this FlowExchangeError is thrown
    # and sends the response as an JSON-object.
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to Upgrade the Authorization Code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # After the credentials object has been received. It has to be checked if
    # there is a valid access token inside of it.
    access_token = credentials.access_token
    # If the token is appended to the following url, the Google API server can
    # verify that this is a valid token for use.
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    # Create a JSON get-request containing the url and access-token and store
    # the result of this request in a variable called result
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, send a 500 internal
    # server error is send to the client.
    # If the if-statement isn't true then the access token is working.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is used for the intended user.
    # Grab the id of the token in my credentials object and compare it to the
    # id returned by the google api server. If these two ids do not match, then
    # I do not have the correct token and should return an error.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID does not match given user ID"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # If the client ids do not match, then app is trying to use a
    # client_id that doesn't belong to it. So I shouldn't allow for this.
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's Client ID does not Match App's"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check if the user is already logged in
    # ! Credentials shouldn't been stored in the session
    # Do not: stored_credentials = login_session.get('credentials')
    # TODO: Delete above comment when everything works
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    print stored_credentials
    print stored_gplus_id
    # So assuming that none of these if-statements were true, I now have a valid
    # access token and my user is successfully able to login to my server.
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current User is Already Connected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    ### After pass all the checks ###
    ### store the access token in the session for later use ###
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    response = make_response(json.dumps('Successfully connected Users', 200))

    # Use the google plus API to get some more information about the user.
    # Here, a message is send off to the google API server with the access
    # token requesting the user info allowed by the token scope and store it in
    # an object called data.
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt':'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    # Data should have all of the values listed on
    # https://developers.google.com/+/api/openidconnect/getOpenIdConnect#response
    # filled in, so long as the user specified them in their account. In the
    # following, the users name, picture and e-mail address are stored in the
    # login session.
    try:
        login_session['username'] = data['name']
        login_session['email'] = data['email']
    except:
        # If can't find these params, print what is in the login_session
        for i in data:
            print(i)

    # TODO: uncomment
    # If user doesn't exist, make a new one.
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    # 7) If the above worked, a html response is returned confirming the login
    # to the Client.
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<h2>'
    output += login_session['email']
    output += '</h2>'
    flash("You are now logged in as %s" % login_session['username'])
    return output

# Disconnect Google User
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['credentials']

    # Ensure to only disconnect a connected user
    if access_token is None:
        response =make_response(json.dumps('Current User Not Connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Execute HTTP Get request to revoke current token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['credentials']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session
        try:
            del login_session['credentials']
            del login_session['gplus_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']
        except:
            print "Remaining items in login_session:"
            for i in login_session:
                print i

        flash("You've successfully logged out")
        return redirect(url_for('showCatalog'))
    else:
        # If the given toekn was invalid, do the following
        response = make_response(json.dumps("Failed to revoke token for given user"), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


####### END #######


####### OAUTH2 authentication #######
@auth.verify_password
def verify_password(username_or_token, password):
    '''
    Use token or password to verify with database
    Return true token is matched or password associated with username is correct
    '''
    # Try to check for token before username
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id = user_id).one()
    # No token, so now checking username
    else:
        user = session.query(User).filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


####### END #######


# Route /
@app.route('/')
@app.route('/catalog')
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

####### CREATE UNIQUE INSTANCE FOR EACH UNIQUE USERS #######
def getUserID(email):
    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None

def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return user

def createUser(login_session):
    newUser = User(username = login_session['username'], email = login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email = login_session['email']).one()
    return user.id
####### END #######


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
