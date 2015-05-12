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


# This is needed to make local development work with SSL.
# See http://stackoverflow.com/a/24066819/500584
# and https://code.google.com/p/googleappengine/issues/detail?id=9246 for more information.
#
# First, copy socket.py out of a standard python install and put it in your project as 'stdlib_socket.py'.
# Then, uncomment the lines below.
#
from google.appengine.tools.devappserver2.python import sandbox
sandbox._WHITE_LIST_C_MODULES += ['_ssl', '_socket']

import sys
import stdlib_socket
socket = sys.modules['socket'] = stdlib_socket

import webapp2
import requests
import gzip
from StringIO import StringIO


URL = "https://api.sandbox.braintreegateway.com:443/merchants/pgd875t7kmgp5q6x/transactions"
HEADERS = {
    'X-ApiVersion': '4',
    'Content-type': 'application/xml',
    'Authorization': 'Basic aHl6a2h4OGRtcDd4Zmc1aDoxZWZiN2YzMWM0ZjM1ODIwNmIxMjk4OTIzYWU0OGE2YQ==',
    'Accept': 'application/xml',
    'User-Agent': 'Braintree Python 3.5.0'
}
BODY = """
<transaction>
    <amount>10.00</amount>
    <type>sale</type>
    <credit_card>
        <expiration_date>05/2020</expiration_date>
        <number>4111111111111111</number>
    </credit_card>
</transaction>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        response = requests.post(URL, headers=HEADERS, data=BODY)
        # this is still gzipped data
        print response.content
        # what response.content should be
        print gzip.GzipFile(fileobj=StringIO(response.content)).read()
        # essentially what is blowing up in the braintree library
        response.text.encode('ascii')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
