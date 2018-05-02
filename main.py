
import datetime
from google.appengine.ext import ndb
import webapp2



class oAuthHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('OAuth page!')



class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')








app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/oauth', oAuthHandler)
], debug=True)
