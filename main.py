#!/usr/bin/env python

import cgi
import os
import webapp2
import facebook
import urllib


from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

from google.appengine.ext.webapp import template
from google.appengine.api import memcache, urlfetch
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext import db, search, webapp


from basehandler import BaseHandler
from model import User, Item, DisplayItem

class MainPage(BaseHandler, blobstore_handlers.BlobstoreDownloadHandler):

    def get(self):

        self.setupUser()
        values = {}

        items = db.GqlQuery('SELECT * FROM Item '
            'ORDER BY updated '
            'LIMIT 10 '
            )
        
        dispItems = []
        for item in items:
            if item.seller != None:
                disp = self.itemToDisplayItem(item)
                dispItems.append(disp)

        values = {'items':dispItems}
        
        path = os.path.join(os.path.dirname(__file__), 'main.html')
        self.response.out.write(template.render(path,values))


    def post(self):
        numArgs = len(self.request.arguments())

        if numArgs == self.SEARCH:
            # this is a search!
            self.redirect('/search=' + self.request.get('category') + '&' \
                + self.request.get('query'))

        self.get()

# this is probably bad
config = {}
config['webapp2_extras.sessions'] = dict(secret_key='')


application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     config=config,
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()