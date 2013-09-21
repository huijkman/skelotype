#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
from webapp2_extras import sessions

#This is needed to configure the session secret key
#Runs first in the whole application
myconfig_dict = {}
myconfig_dict['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key-bladibladibladibladibla',
}

session_password = 'wachtwoord'

# login
class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
 
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)
 
    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

# jinja
import jinja2

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'views')))


# web requests
class MainPage(BaseHandler):
    def get(self):
        pw = self.session.get('password')
        if pw != session_password :
            self.redirect('/login')
        else :
            template_values = {}

            template = jinja_environment.get_template('index.html')
            self.response.out.write(template.render(template_values))

class SubPage(BaseHandler):
    def get(self):
        pw = self.session.get('password')
        if pw != session_password :
            self.redirect('/login')
        else :
            template_values = {}

            template = jinja_environment.get_template('subpage.html')
            self.response.out.write(template.render(template_values))

class LogIn(BaseHandler):
    def get(self):
        if self.session.get('password'):
            del self.session['password']
        if not self.session.get('referrer'):
            self.session['referrer'] = \
                self.request.environ['HTTP_REFERER'] \
                if 'HTTP_REFERER' in self.request.environ \
                else '/'
        template_values = {
            }
        template = jinja_environment.get_template('login.html')
        self.response.out.write(template.render(template_values))
 
    def post(self):
        password = self.request.get('PasswordIsNeededForAccess')
        if password == session_password :
            self.session['password'] = password
            #logging.info("%s just logged in" % user)
            self.redirect('/')
        else :
            template_values = { 'message':'Nope! That wasn\'t it' }
            template = jinja_environment.get_template('login.html')
            self.response.out.write(template.render(template_values))


'''class ResultPage(webapp2.RequestHandler):
    def post(self):
        pw = self.request.get('InputPassword1')
        temp = ''
        if pw==password :
            temp = 'index.html'
        else :
            temp = 'wrong.html'
        template_values = {}

        template = jinja_environment.get_template(temp)
        self.response.out.write(template.render(template_values))'''

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sub', SubPage),
    ('/login',LogIn)
], config = myconfig_dict, debug=True)

