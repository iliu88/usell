# File used to define the entity types within the data store.
# Data is stored hierarchically: all items belong to a user,
# all users belong to a network.

from google.appengine.ext import db
from google.appengine.ext import search

class Item(search.SearchableModel):
    # Item Name
    itemName = db.StringProperty(required=False)
    # Price of Item
    price = db.StringProperty(required=False)
    # Description of Item
    description = db.StringProperty(required=False)
    # Image of item
    image = db.StringProperty(required=False)
    # Category of item
    category = db.StringProperty(required=False)
    
    # Identifies when message was posted
    when = db.DateTimeProperty(auto_now_add=True)


# An object representing a network (a college/university/other
# community group if we include non-colleges)
class Network(db.Model):
    name = db.StringProperty()
    # some form of token


# An object representing a user of our application
class User(db.Model):
    firstName = db.StringProperty()
    lastName = db.StringProperty()
    # fb_id_token
    # items in marketplace
    # reviews

    # return full name
    def fullName(self):
        return self.firstName + " " + self.lastName



