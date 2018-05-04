#!/usr/bin/env python

from __future__ import print_function

import requests
from ConfigParser import SafeConfigParser

try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
    from urllib.parse import urlencode
except ImportError:
    from urlparse import urlparse
    from urllib2 import urlopen
    from urllib import urlencode
    import json

class WatsonAPI:
    # Setup the endpoints
    # Source for web API calls for emotional analysis: http://www.alchemyapi.com/api/api-calls-emotion-analysis 2016-11-17

    # The base URL for all endpoints
    BASE_URL = 'http://access.alchemyapi.com/calls'

    s = requests.Session()

    def __init__(self):
        """	
        Initializes the SDK so it can send requests to AlchemyAPI for analysis.
        It loads the API key from api_key.txt and configures the endpoints.
        """

        import sys
        try:
            # Open the config file and get api key
            parser = SafeConfigParser()
            parser.read('config.ini')
            key = parser.get('api_key', 'api_key') 
            if key == '':
                # The key file should't be blank
                print(
                    'API Key is blank. Please register for an API key')
                sys.exit(0)
            else:
                # setup the key
                self.apikey = key
        except Exception as e:
            print(e)

    # New alchemy analysis.
    def alchemy(self, text, options={}):
        """
        Provides emotional analysis of the text for text, a URL or HTML.

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        None at the moment.


        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """
        parser = SafeConfigParser()
        parser.read('config.ini')
        base_url = parser.get('alchemy', 'base_url')
        features = parser.get('alchemy', 'features')
        username = parser.get('alchemy', 'username') # service credentials required
        password = parser.get('alchemy', 'password') # service credentials required

        url = ("%s&%s" % (base_url, features)) 
        results = ""
        try:
            results = requests.post(url, auth=(username, password), headers = {"Content-type": "text/plain", 'Accept':'application/json'}, data=text)
        except Exception as e:
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'network-error'}
        try:
            return results.json()
        except Exception as e:
            if results != "":
                print(results)
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'parse-error'}


    def profile(self, text):
        """Returns the profile by doing a POST to /v3/profile with text

           Sources:
           http://www.ibm.com/watson/developercloud/doc/personality-insights/
           http://www.ibm.com/watson/developercloud/personality-insights/api/v3/
 
        """
        # url for personality insights to obtain personality information.

        parser = SafeConfigParser()
        parser.read('config.ini')
        url = parser.get('personality', 'url')

        username = parser.get('personality', 'username') # service credentials required
        password = parser.get('personality', 'password') # service credentials required
        results = ""
        try:
            results = requests.post(url, auth=(username, password), headers = {"Content-type": "text/plain", 'Accept':'application/json'}, data=text)
        except Exception as e:
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'network-error'}
        try:
            return results.json()
        except Exception as e:
            if results != "":
                print(results)
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'parse-error'}
