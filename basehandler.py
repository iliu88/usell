import webapp2
import facebook
from google.appengine.ext import db
from webapp2_extras import sessions
from model import User, Item, DisplayItem
from appengine_utilities import sessions


FACEBOOK_APP_ID = "284783798323209"
FACEBOOK_APP_SECRET = "488d93b118272ac03038445c1f4c3c15"

class BaseHandler(webapp2.RequestHandler):

    # current user, a User item
    # This will be configured by setupUser
    user = None

    # constants used to determine the kind of post:
    # either a SEARCH, triggered by the search button
    # or a POST or POST_PHOTO, triggered by the post portal
    SEARCH = 2
    POST = 5
    POST_PHOTO = 6
    FEED_LENGTH = 10
    
    def setupUser(self):
        self.session = sessions.Session()
        # configure user

        if self.session.get("userKey"):
            userKey = self.session["userKey"]["key"]
            self.user = db.get(userKey)
            return

        cookie = facebook.get_user_from_cookie(self.request.cookies,
                                               FACEBOOK_APP_ID,
                                               FACEBOOK_APP_SECRET)

        if cookie != None:
            print "fetching from fbk"
            graph = facebook.GraphAPI(cookie["access_token"])
            profile = graph.get_object("me")

            id = profile["id"]

            q = User.all().filter('id =', id)

            self.user = q.get()

            if self.user == None:
                self.user = User(id = profile["id"],
                    name = profile["name"],
                    profile_url = profile["link"],
                    access_token = cookie["access_token"],
                    items = [])

            self.user.access_token = cookie["access_token"]


            userKey = str(self.user.key())
            self.session["userKey"] = {"key":userKey}
            self.user.put()

        else:
            # redirection logic might go here
            print "no cookie was found"

    def write(self, s):
        self.response.out.write(s)

    def itemToDisplayItem(self, item):
        user = db.get(item.seller[0])
        disp = DisplayItem(id = item.key(),
            itemName = item.itemName,
            price = item.price,
            sellerName = user.name,
            sellerURL = user.profile_url,
            description = item.description,
            blobKey_str = item.blobKey_str
            )
        return disp

