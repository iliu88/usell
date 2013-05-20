# File used to define the entity types within the data store.
# Data is stored hierarchically: all items belong to a user,
# all users belong to a network.

from google.appengine.ext import db, search

class Item(search.SearchableModel):
    itemName = db.StringProperty(required=False)
    price = db.StringProperty(required=False)
    description = db.StringProperty(required=False)
    # image = db.BlobProperty(default=None, required=False)
    category = db.StringProperty(required=False)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now_add=True)
    seller = db.ListProperty(db.Key)

class User(search.SearchableModel):
    id = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now=True)
    updated = db.DateTimeProperty(auto_now=True)
    name = db.StringProperty(required=True)
    profile_url = db.StringProperty(required=True)
    access_token = db.StringProperty(required=True)
    items = db.ListProperty(db.Key)

class DisplayItem():
    
    def __init__(self, id, itemName, price, sellerName, sellerURL, description):
        self.editLink = "/edit_item=" + str(id)
        self.itemName = itemName
        self.price = price
        self.sellerName = sellerName
        self.sellerURL = sellerURL
        self.description = description
