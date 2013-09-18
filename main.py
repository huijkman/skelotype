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

import jinja2

password = 'wachtwoord'


jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'views')))

class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {}

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

class SubPage(webapp2.RequestHandler):
    def get(self):
        template_values = {}

        template = jinja_environment.get_template('subpage.html')
        self.response.out.write(template.render(template_values))

class LoginPage(webapp2.RequestHandler):
    def get(self):
        template_values = {}

        template = jinja_environment.get_template('login.html')
        self.response.out.write(template.render(template_values))

class ResultPage(webapp2.RequestHandler):
    def post(self):
        pw = self.request.get('InputPassword1')
        temp = ''
        if pw==password :
            temp = 'index.html'
        else :
            temp = 'wrong.html'
        template_values = {}

        template = jinja_environment.get_template(temp)
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/sub', SubPage),
    ('/main',MainPage),
    ('/result',ResultPage)
], debug=True)

