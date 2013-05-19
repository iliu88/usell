import webapp2
import facebook
from google.appengine.ext import db
from webapp2_extras import sessions
from model import User, Item, DisplayItem


FACEBOOK_APP_ID = "284783798323209"
FACEBOOK_APP_SECRET = "488d93b118272ac03038445c1f4c3c15"

class BaseHandler(webapp2.RequestHandler):
    """Provides access to the active Facebook user in self.current_user
        
    The property is lazy-loaded on first access, using the cookie saved
    by the Facebook JavaScript SDK to determine the user ID of the active
    user. See http://developers.facebook.com/docs/authentication/ for
    more information.
    """
    user = None
    FEED_LENGTH = 10
    SEARCH = 2
    POST = 5

    @property
    def current_user(self):
        if self.session.get("user"):
            # User is logged in
            return self.session.get("user")
        else:
            # Either used just logged in or just saw the first page
            # We'll see here
            cookie = facebook.get_user_from_cookie(self.request.cookies,
                                                   FACEBOOK_APP_ID,
                                                   FACEBOOK_APP_SECRET)
            if cookie:
                # Okay so user logged in.
                # Now, check to see if existing user
                user = User.get_by_key_name(cookie["uid"])
                if not user:
                    # Not an existing user so get user info
                    graph = facebook.GraphAPI(cookie["access_token"])
                    profile = graph.get_object("me")
                    user = User(
                                key_name=str(profile["id"]),
                                id=str(profile["id"]),
                                name=profile["name"],
                                profile_url=profile["link"],
                                access_token=cookie["access_token"]
                                )
                    user.put()
                elif user.access_token != cookie["access_token"]:
                    user.access_token = cookie["access_token"]
                    user.put()
                # User is now logged in
                self.session["user"] = dict(
                                            name=user.name,
                                            profile_url=user.profile_url,
                                            id=user.id,
                                            access_token=user.access_token
                                            )
                return self.session.get("user")
        return None
    
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)
    
    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

    def write(self, s):
        self.response.out.write(s)

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
                    access_token = self.current_user["access_token"]
                    )
                self.user.put()

    def itemToDisplayItem(self, item):
        user = db.get(item.seller[0])
        disp = DisplayItem(id = item.key(),
            itemName = item.itemName,
            price = item.price,
            sellerName = user.name,
            sellerURL = user.profile_url,
            description = item.description
            )
        return disp

