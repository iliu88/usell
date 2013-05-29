import os
import urllib
import webapp2

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

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler, BaseHandler):
    """
    This handler builds an item to put in the datastore and stores
    a photo in the blobstore.  It will redirect to the user's
    seller profile when it is done.
    """
    def post(self):
        self.setupUser()

        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]

        item = Item(itemName=self.request.get('itemName'), \
                    price=self.request.get('price'), \
                    blobKey_str = str(blob_info.key()), \
                    description=self.request.get('description'), \
                    seller = [self.user.key()],
                    category=self.request.get('category'), \
                    )

        item.put()            
        self.user.items.append(item.key())
        self.user.put()

        self.redirect('/seller_profile')

        #self.redirect('/view_photo/%s' % item.blobKey_str)        

# this is probably bad
config = {}
config['webapp2_extras.sessions'] = dict(secret_key='1234')        

application = webapp.WSGIApplication(
                                     [('/upload', UploadHandler)],
                                     config=config,                                     
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()