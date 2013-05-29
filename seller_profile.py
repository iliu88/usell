#!/usr/bin/env python

import cgi
import os
import webapp2
import facebook

from google.appengine.ext.webapp import template
from google.appengine.api import memcache, urlfetch
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext import db, search, webapp


from basehandler import BaseHandler
from model import User, Item, DisplayItem

class SellerPage(BaseHandler):
    """
    This handler builds the seller_profile page, whic
    displays each item belonging to the current user.
    It also creates links through which the user can
    update and edit their items.
    """
    def get(self):
        self.setupUser()

        values = {}

        if self.user != None:
            items = []
            keys = self.user.items

            for key in keys:
                items.append(db.get(key))
            
            dispItems = []
            for item in items:
                if item.seller != None:
                    disp = self.itemToDisplayItem(item)
                    dispItems.append(disp)

            values = {'items':dispItems}
        
        path = os.path.join(os.path.dirname(__file__), 'seller_profile.html')
        self.response.out.write(template.render(path,values))

    def post(self):
        self.get()

        numArgs = len(self.request.arguments())

        if numArgs == self.SEARCH:
            # this is a search!
            self.redirect('/search=' + self.request.get('category') + '&' \
                + self.request.get('query'))


# this is probably bad
config = {}
config['webapp2_extras.sessions'] = dict(secret_key='')

application = webapp2.WSGIApplication(
                                     [('/seller_profile', SellerPage)],
                                     config=config,                                 
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()