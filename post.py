#!/usr/bin/env python

import cgi
import os
import xml.etree.cElementTree as etree
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp, blobstore
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users, search
import webapp2
from model import *
import datetime

# Import for data storage
from google.appengine.ext import db
from basehandler import BaseHandler

class PostPage(BaseHandler):

    def get(self):
        self.setupUser()

        uploadURL = blobstore.create_upload_url('/upload')
        values = {'uploadURL': uploadURL}

        path = os.path.join(os.path.dirname(__file__), 'post.html')
        self.response.out.write(template.render(path,values))

    def post(self):

        # need to handle different kind of requests D:
        self.get()

        numArgs = len(self.request.arguments())

        if numArgs == self.SEARCH:
            # this is a search!
            self.redirect('/search=' + self.request.get('category') + '&' \
                + self.request.get('query'))

        """else:
            # this is a post
            item = Item(itemName=self.request.get('itemName'), \
                     price=self.request.get('price'), \
                     description=self.request.get('description'), \
                     category=self.request.get('category'), \
                     seller= [self.user.key()]
                     )
            i = self.request.get('image')
            print i
            i2 = i.encode('utf-8')
            item.image = db.Blob(i2)
            item.put()

            self.user.items.append(item.key())
            self.user.put()
            self.redirect('/seller_profile')"""






# this is probably bad
config = {}
config['webapp2_extras.sessions'] = dict(secret_key='1234')        

application = webapp.WSGIApplication(
                                     [('/post', PostPage)],
                                     config=config,                                     
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()