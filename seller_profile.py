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

    FEED_LENGTH = 10
    user = None
    SEARCH = 2

    def get(self):
        self.setupUser()

        items = []
        keys = self.user.items

        for key in keys:
            items.append(db.get(key))
        
        dispItems = []
        for item in items:
            if item.seller != None:
                disp = self.itemToDisplayItem(item)
                dispItems.append(disp)
        
        path = os.path.join(os.path.dirname(__file__), 'seller_profile.html')
        values = {'items':dispItems}
        self.response.out.write(template.render(path,values))

    def post(self):
        self.get()

        numArgs = len(self.request.arguments())

        if numArgs == self.SEARCH:
            # this is a search!
            self.redirect('/search=' + self.request.get('category') + '&' \
                + self.request.get('query'))

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

application = webapp2.WSGIApplication(
                                     [('/seller_profile', SellerPage)],
                                     config=config,                                 
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()