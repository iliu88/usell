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

    def get(self):
        self.setupUser()

        url = self.request.url.split("%3D")[1]
        category = url.split("&")[0]
        query = url.split("&")[1]

        results = Item.all().search(query.lower())
        results.filter("category =", category)

        dispItems = []
        for item in results:
            disp = self.itemToDisplayItem(item)
            dispItems.append(disp)

        values = {'query': query, \
        'items':dispItems}

        path = os.path.join(os.path.dirname(__file__), 'search.html')
        self.response.out.write(template.render(path,values))


    def post(self):

        numArgs = len(self.request.arguments())

        if numArgs == self.SEARCH:
            # this is a search!
            self.redirect('/search=' + self.request.get('category') + '&' \
                + self.request.get('query'))



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