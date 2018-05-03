
import json
import datetime
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import webapp2
import urllib

# Googles auth 2.0 endpoint: https://accounts.google.com/o/oauth2/v2/auth
# This endpoint is ONLY accessable through https (plain http connections are refused)
# Token Exchange/Refresh endpoint: https://www.googleapis.com/oauth2/v4/token

clientID = '983009773849-t8np7njstssp0r4i48m1jalmvi9mvmpa.apps.googleusercontent.com'
clientSecret = 'JPjU8iM_zuCspkcqfUy1JKbA'

plusURL = 'https://www.googleapis.com/plus/v1'

class oAuthHandler(webapp2.RequestHandler):
    def get(self):

        code = self.request.get('code')
        state = self.request.get('state')
        serverPath = 'https://www.googleapis.com/oauth2/v4/token'

        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': clientID,
            'client_secret': clientSecret,
            'redirect_uri': 'http://localhost:8080/oauth'
        }
        form_data = urllib.urlencode(payload)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        result = urlfetch.fetch(
            url=serverPath, 
            payload=form_data, 
            method=urlfetch.POST,
            headers=headers
        )

        if result.status_code == 200:

            self.response.headers["Content-Type"] = "application/json"
            results = json.loads(result.content)
            token = 'Bearer ' + results['access_token']

            requestURL = plusURL + '/people/me'

            result = urlfetch.fetch(
                url=requestURL,
                headers={'Authorization': token}
            )
            if result.status_code == 200:

                account = json.loads(result.content)
                fName = account['name']['familyName']
                lName = account['name']['givenName']
                accountURL = account['url']

                self.response.headers["Content-Type"] = "application/json"
                #self.response.write(result.content)
                self.response.write("First Name:  " + fName + '\n')
                self.response.write("Last Name:   " + lName + '\n')
                self.response.write("Plus Account:" + accountURL + '\n')

            else:
                self.response.status = result.status_code

        else:
            self.response.status = result.status_code



class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')



class startPageHandler(webapp2.RequestHandler):
    def get(self):

        url = 'https://accounts.google.com/o/oauth2/v2/auth'
        respType = 'response_type=code'
        client_id = 'client_id=' + clientID
        redirect_uri = 'redirect_uri=http://localhost:8080/oauth'
        scope = 'scope=email'
        state = 'state=secretGeneratedString0101'

        requestURL = url + '?' + respType + '&' + client_id + '&' + redirect_uri + '&' + scope + '&' + state

        result = urlfetch.fetch(requestURL)
        if result.status_code == 200:
            self.response.write(result.content)

        else:
            self.response.status = result.status_code




class test1Page(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, Test Page 1!')






app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/oauth', oAuthHandler),
    ('/start', startPageHandler),
    ('/test1', test1Page)


], debug=True)
