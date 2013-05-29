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

class EditPage(BaseHandler):
    """
    This handler is responsible for the edit page (when a user
    wants to edit an item already stored in the datastore).
    It displays the same postPortal, but with the fields
    set to the old values of the item.
    The url of this page will be of the form
    /edit_item=.*
    Here .* is the item's key.
    """

    def get(self):
        self.setupUser()

        # parse the item key from the URL
        itemKey = self.request.url.split("%3D")[1]
        item = db.get(itemKey)
        
        # pass the item object to the template
        values = {'items':item}
        path = os.path.join(os.path.dirname(__file__), 'edit_page.html')
        self.response.out.write(template.render(path,values))

    def post(self):
        numArgs = len(self.request.arguments())
        
        if numArgs == self.POST:
            # Retrieve item 
            itemKey = self.request.url.split("%3D")[1]
            item = db.get(itemKey)

            # Resave all the information of the item
            item.itemName = self.request.get('itemName')
            item.price = self.request.get('price')
            item.description = self.request.get('description')
            item.category = self.request.get('category')
            # Saves in datastore again
            item.put()
        
            # Redirect sell profile page
            self.redirect('/seller_profile')
    
        if numArgs == self.SEARCH:
            # this is a search
            self.redirect('/search=' + self.request.get('category') + '&' \
                + self.request.get('query'))

        
# this is probably bad
config = {}
config['webapp2_extras.sessions'] = dict(secret_key='1234')


application = webapp.WSGIApplication(
                                     [('/edit_item=.*', EditPage)],
                                     config=config,
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()