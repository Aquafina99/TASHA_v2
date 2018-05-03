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

    def entities(self, flavor, data, options={}):
        """
        Extracts the entities for text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/entity-extraction/ 
        For the docs, please refer to: http://www.alchemyapi.com/api/entity-extraction/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        disambiguate -> disambiguate entities (i.e. Apple the company vs. apple the fruit). 0: disabled, 1: enabled (default)
        linkedData -> include linked data on disambiguated entities. 0: disabled, 1: enabled (default) 
        coreference -> resolve coreferences (i.e. the pronouns that correspond to named entities). 0: disabled, 1: enabled (default)
        quotations -> extract quotations by entities. 0: disabled (default), 1: enabled.
        sentiment -> analyze sentiment for each entity. 0: disabled (default), 1: enabled. Requires 1 additional API transction if enabled.
        showSourceText -> 0: disabled (default), 1: enabled 
        maxRetrieve -> the maximum number of entities to retrieve (default: 50)

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['entities']:
            return {'status': 'ERROR', 'statusInfo': 'entity extraction for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['entities'][flavor], {}, options)

    def keywords(self, flavor, data, options={}):
        """
        Extracts the keywords from text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/keyword-extraction/
        For the docs, please refer to: http://www.alchemyapi.com/api/keyword-extraction/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        keywordExtractMode -> normal (default), strict
        sentiment -> analyze sentiment for each keyword. 0: disabled (default), 1: enabled. Requires 1 additional API transaction if enabled.
        showSourceText -> 0: disabled (default), 1: enabled.
        maxRetrieve -> the max number of keywords returned (default: 50)

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['keywords']:
            return {'status': 'ERROR', 'statusInfo': 'keyword extraction for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['keywords'][flavor], {}, options)

    def concepts(self, flavor, data, options={}):
        """
        Tags the concepts for text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/concept-tagging/
        For the docs, please refer to: http://www.alchemyapi.com/api/concept-tagging/ 

        Available Options:
        maxRetrieve -> the maximum number of concepts to retrieve (default: 8)
        linkedData -> include linked data, 0: disabled, 1: enabled (default)
        showSourceText -> 0:disabled (default), 1: enabled

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['concepts']:
            return {'status': 'ERROR', 'statusInfo': 'concept tagging for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['concepts'][flavor], {}, options)

    def sentiment(self, flavor, data, options={}):
        """
        Calculates the sentiment for text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/sentiment-analysis/
        For the docs, please refer to: http://www.alchemyapi.com/api/sentiment-analysis/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        showSourceText -> 0: disabled (default), 1: enabled

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['sentiment']:
            return {'status': 'ERROR', 'statusInfo': 'sentiment analysis for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
	print(options)
        return self.__analyze(AlchemyAPI.ENDPOINTS['sentiment'][flavor], {}, options)

    def sentiment_targeted(self, flavor, data, target, options={}):
        """
        Calculates the targeted sentiment for text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/sentiment-analysis/
        For the docs, please refer to: http://www.alchemyapi.com/api/sentiment-analysis/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        target -> the word or phrase to run sentiment analysis on.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        showSourceText	-> 0: disabled, 1: enabled

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Make sure the target is valid
        if target is None or target == '':
            return {'status': 'ERROR', 'statusInfo': 'targeted sentiment requires a non-null target'}

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['sentiment_targeted']:
            return {'status': 'ERROR', 'statusInfo': 'targeted sentiment analysis for ' + flavor + ' not available'}

        # add the URL encoded data and target to the options and analyze
        options[flavor] = data
        options['target'] = target
        return self.__analyze(AlchemyAPI.ENDPOINTS['sentiment_targeted'][flavor], {}, options)

    def text(self, flavor, data, options={}):
        """
        Extracts the cleaned text (removes ads, navigation, etc.) for text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/text-extraction/
        For the docs, please refer to: http://www.alchemyapi.com/api/text-extraction/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        useMetadata -> utilize meta description data, 0: disabled, 1: enabled (default)
        extractLinks -> include links, 0: disabled (default), 1: enabled.

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['text']:
            return {'status': 'ERROR', 'statusInfo': 'clean text extraction for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['text'][flavor], options)

    def text_raw(self, flavor, data, options={}):
        """
        Extracts the raw text (includes ads, navigation, etc.) for a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/text-extraction/ 
        For the docs, please refer to: http://www.alchemyapi.com/api/text-extraction/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        none

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['text_raw']:
            return {'status': 'ERROR', 'statusInfo': 'raw text extraction for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['text_raw'][flavor], {}, options)

    def author(self, flavor, data, options={}):
        """
        Extracts the author from a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/author-extraction/
        For the docs, please refer to: http://www.alchemyapi.com/api/author-extraction/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Availble Options:
        none

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['author']:
            return {'status': 'ERROR', 'statusInfo': 'author extraction for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['author'][flavor], {}, options)

    def language(self, flavor, data, options={}):
        """
        Detects the language for text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/api/language-detection/ 
        For the docs, please refer to: http://www.alchemyapi.com/products/features/language-detection/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        none

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['language']:
            return {'status': 'ERROR', 'statusInfo': 'language detection for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['language'][flavor], {}, options)

    def title(self, flavor, data, options={}):
        """
        Extracts the title for a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/text-extraction/ 
        For the docs, please refer to: http://www.alchemyapi.com/api/text-extraction/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        useMetadata -> utilize title info embedded in meta data, 0: disabled, 1: enabled (default) 

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['title']:
            return {'status': 'ERROR', 'statusInfo': 'title extraction for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['title'][flavor], {}, options)

    def relations(self, flavor, data, options={}):
        """
        Extracts the relations for text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/relation-extraction/ 
        For the docs, please refer to: http://www.alchemyapi.com/api/relation-extraction/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        sentiment -> 0: disabled (default), 1: enabled. Requires one additional API transaction if enabled.
        keywords -> extract keywords from the subject and object. 0: disabled (default), 1: enabled. Requires one additional API transaction if enabled.
        entities -> extract entities from the subject and object. 0: disabled (default), 1: enabled. Requires one additional API transaction if enabled.
        requireEntities -> only extract relations that have entities. 0: disabled (default), 1: enabled.
        sentimentExcludeEntities -> exclude full entity name in sentiment analysis. 0: disabled, 1: enabled (default)
        disambiguate -> disambiguate entities (i.e. Apple the company vs. apple the fruit). 0: disabled, 1: enabled (default)
        linkedData -> include linked data with disambiguated entities. 0: disabled, 1: enabled (default).
        coreference -> resolve entity coreferences. 0: disabled, 1: enabled (default)  
        showSourceText -> 0: disabled (default), 1: enabled.
        maxRetrieve -> the maximum number of relations to extract (default: 50, max: 100)

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['relations']:
            return {'status': 'ERROR', 'statusInfo': 'relation extraction for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['relations'][flavor], {}, options)

    def category(self, flavor, data, options={}):
        """
        Categorizes the text for text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/text-categorization/
        For the docs, please refer to: http://www.alchemyapi.com/api/text-categorization/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        showSourceText -> 0: disabled (default), 1: enabled

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['category']:
            return {'status': 'ERROR', 'statusInfo': 'text categorization for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data

        return self.__analyze(AlchemyAPI.ENDPOINTS['category'][flavor], {}, options)

    def feeds(self, flavor, data, options={}):
        """
        Detects the RSS/ATOM feeds for a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/feed-detection/ 
        For the docs, please refer to: http://www.alchemyapi.com/api/feed-detection/

        INPUT:
        flavor -> which version of the call, i.e.  url or html.
        data -> the data to analyze, either the the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        none

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['feeds']:
            return {'status': 'ERROR', 'statusInfo': 'feed detection for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['feeds'][flavor], {}, options)

    def microformats(self, flavor, data, options={}):
        """
        Parses the microformats for a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/microformats-parsing/
        For the docs, please refer to: http://www.alchemyapi.com/api/microformats-parsing/

        INPUT:
        flavor -> which version of the call, i.e.  url or html.
        data -> the data to analyze, either the the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        none

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['microformats']:
            return {'status': 'ERROR', 'statusInfo': 'microformat extraction for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['microformats'][flavor], {}, options)

    def imageExtraction(self, flavor, data, options={}):
        """
        Extracts main image from a URL

        INPUT:
        flavor -> which version of the call (url only currently).
        data -> URL to analyze
        options -> various parameters that can be used to adjust how the API works, 
        see below for more info on the available options.

        Available Options:
        extractMode -> 
             trust-metadata  :  (less CPU intensive, less accurate)
             always-infer    :  (more CPU intensive, more accurate)
        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """
        if flavor not in AlchemyAPI.ENDPOINTS['image']:
            return {'status': 'ERROR', 'statusInfo': 'image extraction for ' + flavor + ' not available'}
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['image'][flavor], {}, options)

    def taxonomy(self, flavor, data, options={}):
        """
        Taxonomy classification operations.

        INPUT:
        flavor -> which version of the call, i.e.  url or html.
        data -> the data to analyze, either the the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.


        Available Options:
        showSourceText  -> 
            include the original 'source text' the taxonomy categories were extracted from within the API response
            Possible values:
                1 - enabled
                0 - disabled (default) 

        sourceText ->
            where to obtain the text that will be processed by this API call.

            AlchemyAPI supports multiple modes of text extraction:
                web page cleaning (removes ads, navigation links, etc.), raw text extraction 
                (processes all web page text, including ads / nav links), visual constraint queries, and XPath queries. 

            Possible values:
                cleaned_or_raw  : cleaning enabled, fallback to raw when cleaning produces no text (default)
                cleaned         : operate on 'cleaned' web page text (web page cleaning enabled)
                raw             : operate on raw web page text (web page cleaning disabled)
                cquery          : operate on the results of a visual constraints query 
                                  Note: The 'cquery' http argument must also be set to a valid visual constraints query.
                xpath           : operate on the results of an XPath query 
                                  Note: The 'xpath' http argument must also be set to a valid XPath query.

        cquery ->
            a visual constraints query to apply to the web page.

        xpath ->
            an XPath query to apply to the web page.

        baseUrl ->
            rel-tag output base http url (must be uri-argument encoded)

        OUTPUT:
        The response, already converted from JSON to a Python object. 

        """
        if flavor not in AlchemyAPI.ENDPOINTS['taxonomy']:
            return {'status': 'ERROR', 'statusInfo': 'taxonomy for ' + flavor + ' not available'}
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['taxonomy'][flavor], {}, options)

    def combined(self, flavor, data, options={}):
        """
        Combined call for page-image, entity, keyword, title, author, taxonomy,  concept.

        INPUT:
        flavor -> which version of the call, i.e.  url or html.
        data -> the data to analyze, either the the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        extract -> 
            Possible values: page-image, entity, keyword, title, author, taxonomy,  concept
            default        : entity, keyword, taxonomy,  concept

        disambiguate -> 
            disambiguate detected entities
            Possible values:
                1 : enabled (default)
                0 : disabled

        linkedData ->
            include Linked Data content links with disambiguated entities
            Possible values :
                1 : enabled (default)
                0 : disabled

        coreference ->
            resolve he/she/etc coreferences into detected entities
            Possible values:
                1 : enabled (default)
                0 : disabled

        quotations -> 
            enable quotations extraction
            Possible values:
                1 : enabled
                0 : disabled (default)

        sentiment ->
            enable entity-level sentiment analysis
            Possible values:
                1 : enabled
                0 : disabled (default)

        showSourceText -> 
            include the original 'source text' the entities were extracted from within the API response
            Possible values:
                1 : enabled
                0 : disabled (default)

        maxRetrieve ->
            maximum number of named entities to extract
            default : 50

        baseUrl -> 
            rel-tag output base http url


        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """
        if flavor not in AlchemyAPI.ENDPOINTS['combined']:
            return {'status': 'ERROR', 'statusInfo': 'combined for ' + flavor + ' not available'}
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['combined'][flavor], {}, options)

    def imageTagging(self, flavor, data, options={}):
        """

        INPUT:
        flavor -> which version of the call only url or image.
        data -> the data to analyze, either the the url or path to image.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.
        """
        if flavor not in AlchemyAPI.ENDPOINTS['imagetagging']:
            return {'status': 'ERROR', 'statusInfo': 'imagetagging for ' + flavor + ' not available'}
        elif 'image' == flavor:
            image = open(data, 'rb').read()
            options['imagePostMode'] = 'raw'
            return self.__analyze(AlchemyAPI.ENDPOINTS['imagetagging'][flavor], options, image)

        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['imagetagging'][flavor], {}, options)

    def faceTagging(self, flavor, data, options={}):
        """

        INPUT:
        flavor -> which version of the call only url or image.
        data -> the data to analyze, either the the url or path to image.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.
        """
        if flavor not in AlchemyAPI.ENDPOINTS['facetagging']:
            return {'status': 'ERROR', 'statusInfo': 'facetagging for ' + flavor + ' not available'}
        elif 'image' == flavor:
            image = open(data, 'rb').read()
            options['imagePostMode'] = 'raw'
            return self.__analyze(AlchemyAPI.ENDPOINTS['facetagging'][flavor], options, image)

        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['facetagging'][flavor], {}, options)

    # Emotion method was added manually.
    def emotion(self, flavor, data, options={}):
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
        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['emotion']:
            return {'status': 'ERROR', 'statusInfo': 'emotional analysis for ' + flavor + ' not available'}
        
        # add the data to the options and analyze
        options[flavor] = data

        return self.__analyze(AlchemyAPI.ENDPOINTS['emotion'][flavor], {}, options)

    def __analyze(self, endpoint, params, post_data=bytearray()):
        """
        HTTP Request wrapper that is called by the endpoint functions. This function is not intended to be called through an external interface. 
        It makes the call, then converts the returned JSON string into a Python object. 

        INPUT:
        url -> the full URI encoded url

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """
	print(self.apikey)
        # Add the API Key and set the output mode to JSON
        params['apikey'] = self.apikey
        params['outputMode'] = 'json'
        # Insert the base url

        post_url = ""
        try:
            post_url = AlchemyAPI.BASE_URL + endpoint + \
                '?' + urlencode(params).encode('utf-8')
	    print(post_url)
        except TypeError:
            post_url = AlchemyAPI.BASE_URL + endpoint + '?' + urlencode(params)

        results = ""
        try:
            results = self.s.post(url=post_url, data=post_data)
	    print(results.json())
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
        url = parser.get('watson', 'url')

        username = parser.get('watson', 'username') # service credentials required
        password = parser.get('watson', 'password') # service credentials required
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


