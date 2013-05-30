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
import datetime

# Import for data storage
from google.appengine.ext import db
from basehandler import BaseHandler
from google.appengine.ext import blobstore

class PostPage(BaseHandler):
    """
    This class handles the postPortal, where users can post items
    to the datastore.  It passes the item data to the UploadHandler
    which stores the item in the datastore and the photo in the
    Blobstore.
    """

    def get(self):
        self.setupUser()
        path = os.path.join(os.path.dirname(__file__), 'post.html')
        
        upload_url = blobstore.create_upload_url('/upload')
        # For image uploading 
        values = {'upload_url':upload_url}
        
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
config['webapp2_extras.sessions'] = dict(secret_key='1234')        

application = webapp.WSGIApplication(
                                     [('/post', PostPage)],
                                     config=config,                                     
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()