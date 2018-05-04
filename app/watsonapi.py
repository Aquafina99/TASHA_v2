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
    s = requests.Session()

    def alchemy(self, text, features=[]):
        """
        Provides IBM Natural Language Understanding analysis of the text for text, a URL or HTML.

        INPUT:
        text -> the data to analyze.
        features -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
         concepts
         categories
         emotion
         entities
         keywords
         metadata
         relations
         semantic_roles
         sentiment

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """
        parser = SafeConfigParser()
        parser.read('config.ini')
        base_url = parser.get('alchemy', 'base_url')
        if not features:
            features = parser.get('alchemy', 'features')
        else:
            features = ','.join(features) 
        username = parser.get('alchemy', 'username') # service credentials required
        password = parser.get('alchemy', 'password') # service credentials required

        url = ("%s&features=%s" % (base_url, features)) 
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
           Provides IBM Personality analysis of the text for text.

           INPUT:
           text -> the data to analyze.

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
