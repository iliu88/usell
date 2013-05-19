#!/usr/bin/env python

import cgi
import os
import xml.etree.cElementTree as etree
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users, search
import webapp2
from model import *

# Import for data storage
from google.appengine.ext import db
from basehandler import BaseHandler

class SearchPage(BaseHandler):

    user = None
    SEARCH = 2

    def get(self):
        self.setupUser()

        url = self.request.url.split("%3D")[1]
        category = url.split("&")[0]
        query = url.split("&")[1]

        results = Item.all().search(query.lower())

        dispItems = []
        for item in results:
            disp = self.itemToDisplayItem(item)
            dispItems.append(disp)

        values = {'query': query, \
        'items':dispItems}

        path = os.path.join(os.path.dirname(__file__), 'search.html')
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
                    access_token = self.current_user["access_token"])
                self.user.put()

    def itemToDisplayItem(self, item):
        user = db.get(item.seller[0])
        disp = DisplayItem(id = item.id
            itemName = item.itemName,
            price = item.price,
            sellerName = user.name,
            sellerURL = user.profile_url,
            description = item.description
            )
        return disp



# this is probably bad
config = {}
config['webapp2_extras.sessions'] = dict(secret_key='1234')

app = webapp2.WSGIApplication([('/search=.*', SearchPage)],
                                config=config,
                                debug=True)


def main():
    run_wsgi_app(app)


if __name__ == "__main__":
    main()