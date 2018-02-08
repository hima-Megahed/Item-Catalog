from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   jsonify,
                   url_for,
                   flash)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Item, Category
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

engine = create_engine('sqlite:///itemCatalogs.db')
Base.metadata.bind = engine

database_session = sessionmaker(bind=engine)
session = database_session()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


# ---------------------- Application Routing ----------------------
@app.route('/')
def main_page():
    """This function renders main page"""
    '''if 'username' in login_session:
        print(login_session['username'])
        login_session.clear()'''
    categories = session.query(Category).all()
    last_added_items = session.query(Item).order_by(Item.id.desc()).limit(10)
    last_items_cats = {}
    for index in range(10):
        cat = session.query(Category).filter_by(id=last_added_items[index].
                                                category_id).first()
        last_items_cats[index] = last_added_items[index], cat.name
    return render_template('categories.html', categories=categories,
                           items_added=last_items_cats)


@app.route('/<path:category>/Items')
def show_category(category):
    """This function shows specific category based on it's name"""
    category = session.query(Category).filter_by(name=category).first()
    items = session.query(Item).filter_by(category=category).all()
    return render_template('category_items.html', category=category,
                           items=items)


@app.route('/catalog.json/')
def catalogs_json():
    """This Function Return JSON Object for all data"""
    my_cats = {}
    categories = session.query(Category).order_by(Category.id)
    for category in categories:
        items = session.query(Item).filter_by(category=category).\
            order_by(Item.id)
        category.items = items
        my_cats[category] = {}

    return jsonify(categories=[get_categories(cat) for cat in my_cats])


@app.route('/<path:category>/<path:item>')
def get_description(category, item):
    """This function Gets the details about item"""
    category = session.query(Category).filter_by(name=category).first()
    item = session.query(Item).filter_by(category=category, name=item).first()
    return render_template('item_description.html', item=item,
                           category=category)


@app.route('/Category/New', methods=['GET', 'POST'])
def add_category():
    """This function Adds new Category"""
    if 'username' in login_session:
        if request.method == 'POST' and request.form['name']:
            user = get_user_info(login_session['user_id'])
            new_category = Category(name=request.form['name'], owner=user)
            session.add(new_category)
            session.commit()
            return redirect(url_for('main_page'))
        else:
            return render_template('new_category.html')
    else:
        return redirect(url_for('show_login'))


@app.route('/<path:category>/Edit', methods=['GET', 'POST'])
def edit_category(category):
    """This function Edit existing Category"""
    if 'username' in login_session:
        if login_session['user_id'] == \
           get_category_owner(category):
            cat = session.query(Category).filter_by(name=category).first()
            if request.method == 'POST':
                if request.form['name']:
                    cat.name = request.form['name']
                    session.add(cat)
                    session.commit()
                return redirect(url_for('main_page'))
            else:
                return render_template('edit_category.html', category=cat)
        else:
            flash("snap! You are NOT Authorized To Edit this Category")
            flash("Create a category so that you can edit or delete")
            return redirect(url_for('add_category'))
    else:
        return redirect(url_for('show_login'))


@app.route('/<path:category>/Delete', methods=['GET', 'POST'])
def delete_category(category):
    """This function Delete Specific Category"""
    if 'username' in login_session:
        if login_session['user_id'] == \
                get_category_owner(category):
            cat = session.query(Category).filter_by(name=category).first()
            if request.method == 'POST':
                session.delete(cat)
                session.commit()
                return redirect(url_for('main_page'))
            else:
                return render_template('delete_category.html', category=cat)
        else:
            flash("snap! You are NOT Authorized To Delete this Category")
            flash("Create a category so that you can edit or delete")
            return redirect(url_for('add_category'))
    else:
        return redirect(url_for('show_login'))


@app.route('/Items/New', methods=['GET', 'POST'])
def add_item():
    """This Function Adds new item"""
    if 'username' in login_session:
        if request.method == 'POST':
            selected_category_name = request.form.get('categories')
            category = session.query(Category).filter_by(
                name=selected_category_name).first()
            user = get_user_info(login_session['user_id'])
            new_item = Item(name=request.form['name'],
                            description=request.form['description'],
                            category=category, owner=user)
            session.add(new_item)
            session.commit()
            return redirect(url_for('show_category', category=category.name))
        else:
            categories = session.query(Category).all()
            return render_template('new_item.html', categories=categories)
    else:
        return redirect(url_for('show_login'))


@app.route('/<category_name>/<path:item>/Edit', methods=['GET', 'POST'])
def edit_item(category_name, item):
    """This function Edit an existing item"""
    if 'username' in login_session:
        if login_session['user_id'] == \
                get_item_owner(item, category_name):
            if request.method == 'POST':
                selected_category_name = request.form.get('categories')
                new_category = session.query(Category).filter_by(
                    name=selected_category_name).first()
                old_category = session.query(Category).filter_by(
                    name=category_name).first()
                edited_item = session.query(Item).filter_by(category=old_category,
                                                            name=item).first()
                edited_item.name = request.form['name']
                edited_item.description = request.form['description']
                edited_item.category = new_category
                session.add(edited_item)
                session.commit()
                return redirect(url_for('get_description', item=edited_item.name,
                                        category=new_category.name))
            else:
                categories = session.query(Category).all()
                category = session.query(Category).filter_by(name=category_name).\
                    first()
                item = session.query(Item).filter_by(category=category,
                                                     name=item).first()
                return render_template('edit_item.html', categories=categories,
                                       item=item)
        else:
            flash("snap! You are NOT Authorized To Edit this Item")
            flash("Create an Item so that you can edit or delete")
            return redirect(url_for('add_item'))
    else:
        return redirect(url_for('show_login'))


@app.route('/<path:category>/<path:item>/Delete', methods=['GET', 'POST'])
def delete_item(category, item):
    """This function delete an item"""
    if 'username' in login_session:
        if login_session['user_id'] == \
                get_item_owner(item, category):
            if request.method == 'POST':
                category = session.query(Category).filter_by(
                    name=category).first()
                item = session.query(Item).filter_by(category=category,
                                                     name=item).first()
                session.delete(item)
                session.commit()
                return redirect(url_for('show_category', category=category.name))
            else:
                category = session.query(Category).filter_by(
                    name=category).first()
                item = session.query(Item).filter_by(category=category,
                                                     name=item).first()
                return render_template('delete_item.html', category=category,
                                       item=item)
        else:
            flash("snap! You are NOT Authorized To Edit this Item")
            flash("Create an Item so that you can edit or delete")
            return redirect(url_for('add_item'))
    else:
        return redirect(url_for('show_login'))


@app.route('/login')
def show_login():
    """This function renders Login page"""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/google_connect', methods=['POST'])
def google_connect():
    """This function handles 3rd party Authorization with GOOGLE"""
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        print("CLIENT ID:", CLIENT_ID)
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user'
                                            ' is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)

    login_session['user_id'] = user_id
    print(user_id)
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:' \
              ' 150px;-webkit-border-radius: 150px;-moz-border-radius: ' \
              '150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print('done!')
    return output


@app.route('/google_disconnect')
def google_disconnect():
    """This function Disconnect 3rd party Authorization with GOOGLE"""
    access_token = login_session.get('access_token')
    if access_token is None:
        print ('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % \
          login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        '''del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']'''
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given'
                                            ' user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/facebook_connect', methods=['POST'])
def facebook_connect():
    """This function handles 3rd party Authorization with FACEBOOK"""
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print("access token received %s ") % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=' \
          'fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange' \
          '_token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange
        we have to split the token first on commas and select the first index
        which gives us the key : value for the server access token then we
        split it on colons to pull out the actual token value and replace the
        remaining quotes with nothing so that it can be used directly in
        the graph api calls '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,' \
          'id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&' \
          'redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:' \
              ' 150px;-webkit-border-radius: 150px;-moz-border-radius:' \
              ' 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/facebook_disconnect')
def facebook_disconnect():
    """This function Disconnect 3rd party Authorization with FACEBOOK"""
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s'\
          % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/disconnect')
def disconnect():
    """This function handles disconnecting from the app"""
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            google_disconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            facebook_disconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        if 'user_id' in login_session:
            del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('main_page'))
    else:
        flash("You were not logged in")
        return redirect(url_for('main_page'))


# ---------------------- Helper Functions ----------------------
def get_categories(category):
    """Helper function return serializable object"""
    return {
        'Category id': category.id,
        'Category name': category.name,
        'Category items': [item.serialize for item in category.items]
    }


def create_user(login_session_p):
    """This function Creates new user and stores it"""
    new_user = User(username=login_session_p['username'],
                    email=login_session_p['email'],
                    picture=login_session_p['picture'])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session_p['email']).one()
    return user.id


def get_user_info(user_id):
    """This function retrieves user info"""
    user = session.query(User).filter_by(id=user_id).one()
    return user


def get_category_owner(category):
    """This function retrieves category owner id"""
    # noinspection PyBroadException
    try:
        cat = session.query(Category).filter_by(name=category).first()
        return cat.user_id
    except Exception:
        return None


def get_item_owner(item, category_name):
    """This function retrieves item owner id"""
    # noinspection PyBroadException
    try:
        category = session.query(Category).filter_by(
            name=category_name).first()
        item = session.query(Item).filter_by(category=category,
                                             name=item).first()
        return item.user_id
    except Exception:
        return None


def get_user_id(email):
    """This function returns user id"""
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


if __name__ == '__main__':
    app.secret_key = 'secret-key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
