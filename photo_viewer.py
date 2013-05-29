from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app

class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, photo_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            self.send_blob(photo_key)

application = webapp.WSGIApplication([('/view_photo/([^/]+)?', ViewPhotoHandler)
                                     ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()