import cgi
import os
import xml.etree.cElementTree as etree
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.api import search
import webapp2
import logging
from model import Item


html = """
    <html>
    <head>
    <style>
    
    *{
    padding:0;
    margin:0 auto;
    }
    
    #wrapper {
    width:100%;    
    }
    
    #header{
    height:80px;
    background-color:#3b5998;
    width:100%;
    }
    
    #content{
    width:100%;
    background-color:#3b5998;
    }
    
    </style>
    </head>
    
    <div id="wrapper">
    <div id="header"></div>
    <p style = "font-size:35px; color:white;
    font-weight:bold; font-family:tahoma;text-shadow: 2px 2px 2px #085a00;
    background-color:#3b5998;" align = "center">
    Welcome to USellit!
    <p>
    <p style="font-family:tahoma; color:white; background-color:#3b5998;font-size:20px;"  align = "center">
    Don't Want it? Sell it!</p>
    <p style="font-family:tahoma; color:#3b5998; background-color:#3b5998;font-size:14px;">Don't Want it? Sell it!</p>
    </div>
    <p style="color:white;">a</p>

   <head>
    <style>
    
    .wrap {
        width: 100%
    }
    
    ul {
    list-style-type:circle;
    position:absolute;
    top:12em;
    left:4em;
    margin:0;
    padding:4px;
    vertical-align:left;
    font-family:tahoma;
    }
    </style>
    </head>
    
    <body>
        <div class = "wrap">
    <div>
    <ul>
        <li><a href="/">Home</a></li>
        <li><a href="#sellers">Seller Profiles</a></li>
        <li><a href="/sell">Post an Item to Sell!</a></li>
        <li><a href="/search">Search</a></li>            
    </ul>
    </div>
    <div>


    <p align = "center" style="color:#3b5998;font-family:tahoma;"> <b> Search for an item </p>
    <form align = "center" action ="/search" method="post">
        <div><textarea name="query" rows = "3" cols="50"></textarea></div>
        <div><input type = "submit" value="Search for Item!"></div>
    </form>
</body>

    </html"""

book1 = Item(itemName="harry potter", \
                         price="20", \
                         description="good book", \
                         image= None, \
                         category="Books")

book1.put()

book2 = Item(itemName="the bible", \
                         price="20", \
                         description="good book", \
                         image= None, \
                         category="Books")

book2.put()

book3 = Item(itemName="sherlock holmes", \
                         price="20", \
                         description="good book", \
                         image= None, \
                         category="Books")

book3.put()

book4 = Item(itemName="flowers for algernon", \
                         price="20", \
                         description="good book", \
                         image= None, \
                         category="Books")

book4.put()

book5 = Item(itemName="mmmm foood", \
                         price="20", \
                         description="good book", \
                         image= None, \
                         category="Books")

book5.put()

class SearchPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write(html)

  def post(self):
    q = self.request.get('query').lower()
    self.response.out.write('Query: ' + q + '</br>')
    results = Item.all().search(q)

    for r in results:
        self.response.out.write(r.itemName + '</br>')





app = webapp2.WSGIApplication([('/search', SearchPage)],
                            debug=True)


def main():
    run_wsgi_app(app)


if __name__ == "__main__":
    main()