#!/usr/bin/env python

import cgi
import os
import webapp2
import facebook

from google.appengine.ext.webapp import template
from google.appengine.api import memcache, urlfetch
from google.appengine.ext.webapp.util import run_wsgi_app
<<<<<<< HEAD
from google.appengine.api import users, search
import webapp2

## dummy config to enable registering django template filters
#os.environ[u'DJANGO_SETTINGS_MODULE'] = u'conf'
##
#from google.appengine.dist import use_library
#use_library('django', '1.2')
#
#from django.template.defaultfilters import register
#from django.utils import simplejson as json
#from functools import wraps
#from google.appengine.api import urlfetch, taskqueue
#from google.appengine.ext import db, webapp
#from google.appengine.ext.webapp import util, template 
#from google.appengine.runtime import DeadlineExceededError
#from random import randrange
#from uuid import uuid4
#import Cookie
#import base64
#import cgi
##import conf
#import datetime
#import hashlib
#import hmac
#import logging
#import time
#import traceback
#import urllib


from model import *

# Import for data storage
from google.appengine.ext import db
=======
from google.appengine.api import users
from google.appengine.ext import db, search, webapp


from basehandler import BaseHandler
from model import User, Item, DisplayItem

class MainPage(BaseHandler):

    FEED_LENGTH = 10
    user = None
    SEARCH = 2

    def get(self):
        self.setupUser()

        items = db.GqlQuery('SELECT * FROM Item '
            'ORDER BY updated DESC '
            'LIMIT ' + str(self.FEED_LENGTH) + ' ')
        
        dispItems = []
        for item in items:
            if item.seller != None:
                disp = self.itemToDisplayItem(item)
                dispItems.append(disp)
        
        path = os.path.join(os.path.dirname(__file__), 'main.html')
        values = {'items':dispItems}
        self.response.out.write(template.render(path,values))

    def post(self):
        self.get()
>>>>>>> sam's-branch


        numArgs = len(self.request.arguments())

        if numArgs == self.SEARCH:
            # this is a search!
            self.redirect('/search=' + self.request.get('category') + '&' \
                + self.request.get('query'))

<<<<<<< HEAD
class MainPage(webapp.RequestHandler):
    def get(self):
        sellposts = db.GqlQuery(
                             'SELECT * FROM Item '
                             'ORDER BY when DESC '
                             'LIMIT 3 ')
        values = {'sellposts':sellposts}
        
        #  Uncomment this to delete all material in data store
        # db.delete(sellposts)

        path = os.path.join(os.path.dirname(__file__), 'main.html')
        self.response.out.write(template.render(path,values))

    def post(self):
        item = Item(itemName=self.request.get('itemName'), \
                         price=self.request.get('price'), \
                         description=self.request.get('description'), \
                         image=self.request.get('image'), \
                         category=self.request.get('category'), )
        # Puts it in the data store
        item.put()
        
        # Redirect user to main page
        self.redirect('/')
        
#_USER_FIELDS = u'name,email,picture,friends'
#class User(db.Model):
#    user_id = db.StringProperty(required=True)
#    access_token = db.StringProperty(required=True) #fb OAUTH access token
#    name = db.StringProperty(required=True)
#    picture = db.StringProperty(required=True)
#    email = db.StringProperty()
#    friends = db.StringListProperty()
#    dirty = db.BooleanProperty()
#    created = db.DateTimeProperty(auto_now_add=True)
#    updated = db.DateTimeProperty(auto_now=True)
#
#    def refresh_data(self):
#        """Refresh this user's data using the Facebook Graph API"""
#        me = Facebook().api(u'/me',
#                            {u'fields': _USER_FIELDS, u'access_token': self.access_token})
#        self.dirty = False
#        self.name = me[u'name']
#        self.email = me.get(u'email')
#        self.picture = me[u'picture']
#        self.friends = [user[u'id'] for user in me[u'friends'][u'data']]
#        return self.put()
#
#
#class FacebookApiError(Exception):
#    def __init__(self, result):
#        self.result = result
#    
#    def __str__(self):
#        return self.__class__.__name__ + ': ' + json.dumps(self.result)
#
#
#class Facebook(object):
#    """Wraps the Facebook specific logic"""
#    def __init__(self, app_id=conf.FACEBOOK_APP_ID,
#                 app_secret=conf.FACEBOOK_APP_SECRET):
#        self.app_id = app_id
#        self.app_secret = app_secret
#        self.user_id = None
#        self.access_token = None
#        self.signed_request = {}
#    
#    def api(self, path, params=None, method=u'GET', domain=u'graph'):
#        """Make API calls"""
#        if not params:
#            params = {}
#        params[u'method'] = method
#        if u'access_token' not in params and self.access_token:
#            params[u'access_token'] = self.access_token
#        result = json.loads(urlfetch.fetch(
#                                           url=u'https://' + domain + u'.facebook.com' + path,
#                                           payload=urllib.urlencode(params),
#                                           method=urlfetch.POST,
#                                           headers={
#                                           u'Content-Type': u'application/x-www-form-urlencoded'})
#                            .content)
#        if isinstance(result, dict) and u'error' in result:
#            raise FacebookApiError(result)
#        return result
#    
#    def load_signed_request(self, signed_request):
#        """Load the user state from a signed_request value"""
#        try:
#            sig, payload = signed_request.split(u'.', 1)
#            sig = self.base64_url_decode(sig)
#            data = json.loads(self.base64_url_decode(payload))
#            
#            expected_sig = hmac.new(
#                                    self.app_secret, msg=payload, digestmod=hashlib.sha256).digest()
#            
#            # allow the signed_request to function for upto 1 day
#            if sig == expected_sig and \
#                data[u'issued_at'] > (time.time() - 86400):
#                    self.signed_request = data
#                    self.user_id = data.get(u'user_id')
#                    self.access_token = data.get(u'oauth_token')
#        except ValueError, ex:
#            pass # ignore if can't split on dot
#    
#    @property
#    def user_cookie(self):
#        """Generate a signed_request value based on current state"""
#        if not self.user_id:
#            return
#        payload = self.base64_url_encode(json.dumps({
#                                                    u'user_id': self.user_id,
#                                                    u'issued_at': str(int(time.time())),
#                                                    }))
#        sig = self.base64_url_encode(hmac.new(
#                                              self.app_secret, msg=payload, digestmod=hashlib.sha256).digest())
#        return sig + '.' + payload
#    
#    @staticmethod
#    def base64_url_decode(data):
#        data = data.encode(u'ascii')
#        data += '=' * (4 - (len(data) % 4))
#        return base64.urlsafe_b64decode(data)
#    
#    @staticmethod
#    def base64_url_encode(data):
#        return base64.urlsafe_b64encode(data).rstrip('=')
#
#
#class CsrfException(Exception):
#    pass
#
#
#class BaseHandler(webapp.RequestHandler):
#    facebook = None
#    user = None
#    csrf_protect = True
#    
#    def initialize(self, request, response):
#        """General initialization for every request"""
#        super(BaseHandler, self).initialize(request, response)
#        
#        try:
#            self.init_facebook()
#            self.init_csrf()
#            self.response.headers[u'P3P'] = u'CP=HONK'  # iframe cookies in IE
#        except Exception, ex:
#            self.log_exception(ex)
#            raise
#    
#    def handle_exception(self, ex, debug_mode):
#        """Invoked for unhandled exceptions by webapp"""
#        self.log_exception(ex)
#        self.render(u'error',
#                    trace=traceback.format_exc(), debug_mode=debug_mode)
#    
#    def log_exception(self, ex):
#        """Internal logging handler to reduce some App Engine noise in errors"""
#        msg = ((str(ex) or ex.__class__.__name__) +
#               u': \n' + traceback.format_exc())
#        if isinstance(ex, urlfetch.DownloadError) or \
#            isinstance(ex, DeadlineExceededError) or \
#            isinstance(ex, CsrfException) or \
#            isinstance(ex, taskqueue.TransientError):
#                logging.warn(msg)
#        else:
#            logging.error(msg)
#    
#    def set_cookie(self, name, value, expires=None):
#        """Set a cookie"""
#        if value is None:
#            value = 'deleted'
#            expires = datetime.timedelta(minutes=-50000)
#        jar = Cookie.SimpleCookie()
#        jar[name] = value
#        jar[name]['path'] = u'/'
#        if expires:
#            if isinstance(expires, datetime.timedelta):
#                expires = datetime.datetime.now() + expires
#            if isinstance(expires, datetime.datetime):
#                expires = expires.strftime('%a, %d %b %Y %H:%M:%S')
#            jar[name]['expires'] = expires
#        self.response.headers.add_header(*jar.output().split(u': ', 1))
#    
#    def render(self, name, **data):
#        """Render a template"""
#        if not data:
#            data = {}
#        data[u'js_conf'] = json.dumps({
#                                      u'appId': conf.FACEBOOK_APP_ID,
#                                      u'canvasName': conf.FACEBOOK_CANVAS_NAME,
#                                      u'userIdOnServer': self.user.user_id if self.user else None,
#                                      })
#        data[u'logged_in_user'] = self.user
#        data[u'message'] = self.get_message()
#        data[u'csrf_token'] = self.csrf_token
#        data[u'canvas_name'] = conf.FACEBOOK_CANVAS_NAME
#        self.response.out.write(template.render(
#                                                os.path.join(
#                                                             os.path.dirname(__file__), 'templates', name + '.html'),
#                                                data))
#    
#    def init_facebook(self):
#        """Sets up the request specific Facebook and User instance"""
#        facebook = Facebook()
#        user = None
#        
#        # initial facebook request comes in as a POST with a signed_request
#        if u'signed_request' in self.request.POST:
#            facebook.load_signed_request(self.request.get('signed_request'))
#            # we reset the method to GET because a request from facebook with a
#            # signed_request uses POST for security reasons, despite it
#            # actually being a GET. in webapp causes loss of request.POST data.
#            self.request.method = u'GET'
#            self.set_cookie(
#                            'u', facebook.user_cookie, datetime.timedelta(minutes=1440))
#        elif 'u' in self.request.cookies:
#            facebook.load_signed_request(self.request.cookies.get('u'))
#        
#        # try to load or create a user object
#        if facebook.user_id:
#            user = User.get_by_key_name(facebook.user_id)
#            if user:
#                # update stored access_token
#                if facebook.access_token and \
#                    facebook.access_token != user.access_token:
#                        user.access_token = facebook.access_token
#                        user.put()
#                # refresh data if we failed in doing so after a realtime ping
#                if user.dirty:
#                    user.refresh_data()
#                # restore stored access_token if necessary
#                if not facebook.access_token:
#                    facebook.access_token = user.access_token
#            
#            if not user and facebook.access_token:
#                me = facebook.api(u'/me', {u'fields': _USER_FIELDS})
#                try:
#                    friends = [user[u'id'] for user in me[u'friends'][u'data']]
#                    user = User(key_name=facebook.user_id,
#                                user_id=facebook.user_id, friends=friends,
#                                access_token=facebook.access_token, name=me[u'name'],
#                                email=me.get(u'email'), picture=me[u'picture'])
#                    user.put()
#                except KeyError, ex:
#                    pass # ignore if can't get the minimum fields
#        
#        self.facebook = facebook
#        self.user = user
#    
#    def init_csrf(self):
#        """Issue and handle CSRF token as necessary"""
#        self.csrf_token = self.request.cookies.get(u'c')
#        if not self.csrf_token:
#            self.csrf_token = str(uuid4())[:8]
#            self.set_cookie('c', self.csrf_token)
#        if self.request.method == u'POST' and self.csrf_protect and \
#            self.csrf_token != self.request.POST.get(u'_csrf_token'):
#                raise CsrfException(u'Missing or invalid CSRF token.')
#    
#    def set_message(self, **obj):
#        """Simple message support"""
#        self.set_cookie('m', base64.b64encode(json.dumps(obj)) if obj else None)
#    
#    def get_message(self):
#        """Get and clear the current message"""
#        message = self.request.cookies.get(u'm')
#        if message:
#            self.set_message()  # clear the current cookie
#            return json.loads(base64.b64decode(message))
#
#
#def user_required(fn):
#    """Decorator to ensure a user is present"""
#    @wraps(fn)
#    def wrapper(*args, **kwargs):
#        handler = args[0]
#        if handler.user:
#            return fn(*args, **kwargs)
#        handler.redirect(u'/')
#    return wrapper

############################################################


application = webapp.WSGIApplication(
                                     [('/', MainPage)],                                     
=======
    def setupUser(self):
        if self.current_user != None:
            id = self.current_user["id"]    
            q = User.all().filter('id =', id)

            self.user = q.get()

            if self.user == None:
                self.user = User(id = self.current_user["id"],
                    name = self.current_user["name"],
                    profile_url = self.current_user["profile_url"],
                    items = [],
                    access_token = self.current_user["access_token"]
                    )
                self.user.put()

    def itemToDisplayItem(self, item):
        user = db.get(item.seller[0])
        disp = DisplayItem(itemName = item.itemName,
            price = item.price,
            sellerName = user.name,
            sellerURL = user.profile_url,
            description = item.description
            )
        return disp

        
# this is probably bad
config = {}
config['webapp2_extras.sessions'] = dict(secret_key='1234')


application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     config=config,
>>>>>>> sam's-branch
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()