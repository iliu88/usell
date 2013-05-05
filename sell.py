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


class MainPage(webapp.RequestHandler):
    def get(self):
        sellposts = db.GqlQuery(
                             'SELECT * FROM Item '
                             'ORDER BY when DESC '
                             'LIMIT 3 ')
        values = {'sellposts':sellposts}
        
        #  Uncomment this to delete all material in data store
        # db.delete(sellposts)

        path = os.path.join(os.path.dirname(__file__), 'sell.html')
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
        

application = webapp.WSGIApplication(
                                     [('/sell', MainPage)],                                     
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()