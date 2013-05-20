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

class MainPage(BaseHandler):

    def get(self):

        item = Item(itemName="couch", \
                     price="24", \
                     description= "comfy", \
                     category="Books", \
                     )

        item.put()
        user = User(name="Sam Szuflita", \
                    profile_url="google.com", \
                    id="5", \
                    access_token="hello",
                    items = [item.key()]
            )

        user.put()
        item.seller = [user.key()]
        item.put()

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

        numArgs = len(self.request.arguments())

        if numArgs == self.SEARCH:
            # this is a search!
            self.redirect('/search=' + self.request.get('category') + '&' \
                + self.request.get('query'))




        
# this is probably bad
config = {}
config['webapp2_extras.sessions'] = dict(secret_key='1234')


application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     config=config,
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()