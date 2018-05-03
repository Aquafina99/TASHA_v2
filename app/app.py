#flask stuff
from flask import Flask, redirect, url_for, session, request, jsonify
from flask.ext import restful
from flask_oauthlib.client import OAuth
from flask_restful import reqparse
from flask_httpauth import HTTPBasicAuth
from werkzeug import secure_filename
import pycurl
import cStringIO
from bs4 import BeautifulSoup
import requests
from flask.ext.cache import Cache

#watson stuff
from watson_developer_cloud import AlchemyLanguageV1
from watsonapi import WatsonAPI
import json

#custom stuff
from readabilityScore import *
from ConfigParser import SafeConfigParser

app = Flask(__name__)
cache = Cache(config={'CACHE_TYPE': 'null'})
cache.init_app(app)
auth= HTTPBasicAuth()
app.debug = True

# Snippet taken the Flask documentation site: http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
app.config['UPLOAD_FOLDER'] = 'app/uploadFiles/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'bib', 'xls'])

parser = reqparse.RequestParser()
parser.add_argument('person_id', type=str)
parser.add_argument('content', type=str)

@auth.get_password	

#this it taken from Miguel Grinberg from http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask -----
#used for authorizing REST calls
def get_password(username):
    """
    Returns password given the correct username.
    Used for credential check to use APIs
    """
    #get variables from config file
    parser = SafeConfigParser()
    parser.read('config.ini')

    user =  parser.get('credentials', 'username')
    passwd = parser.get('credentials', 'password')

    if username == user:
        return passwd
    return None

@auth.error_handler
def unauthorized():
    """
    Returns JSON ERROR text if unauthorized use of API.
    """
    return jsonify({'Error': 'Unauthorized access!'})

@app.route('/tasha/test', methods=['POST'])
@auth.login_required
def loaddatabasetest():
    """
    Check if server is running properly

    @return: "Hello. Server is running."
    @rtype: string
    """
    args = parser.parse_args()
    return jsonify("Hello. Server is running.")

@app.route('/tasha/readability', methods=['POST','GET'])
@auth.login_required
def ReadabilityScore():
    """
    Get Readability Score of input
    @input: JSON with content and person_id
    @return: the readability scores
    @rtype: JSON
    """
    args = parser.parse_args()
    content = args['content'];
    readability = getReadabilityScore(content)
    return jsonify(readability)

@app.route('/tasha/syntax_error_count', methods=['POST','GET'])
@auth.login_required
def SyntaxMetric():
    """
    Get Syntax Error Count
    @input: JSON with content
    @return the syntax error count
    @rtype: JSON
    """
    args = parser.parse_args()
    content = args['content'];
    r = requests.post("http://162.246.157.115/checkDocument", data={'data': content})
    m  = r.text
    y = BeautifulSoup(m, "html5lib")
    return jsonify({"errors":len(y.results.findAll("error"))})

@app.route('/tasha/personality', methods=['POST', 'GET'])
@auth.login_required
def ProfileResult():
    """
    Returns profile of personality traits 
    for the given text data

    @rtype: JSON
    @return: JSON that contains personality insight
    """

    args = parser.parse_args()
    content = args['content'];
    # Create the AlchemyAPI Object    
    alchemyapi = WatsonAPI()

    file_name = content # this is the text file that we are passing through

    response = alchemyapi.profile(file_name)

    return jsonify(response) # ['word_count'], ['personality'], ['needs'], ['values']
                    # are the important keys that contain necessary data


@app.route('/tasha/sentiment', methods=['POST', 'GET'])
@auth.login_required
def SentimentResult():
    """
    Returns the overall sentiment analysis given a text file.

    @rtype: JSON
    @return: JSON that contains the overall
        sentiment analysis result.
    """

    args = parser.parse_args()
    content = args['content'];
    # Create the AlchemyAPI Object
    alchemyapi = AlchemyAPI()

    file_name = content # this is the file/url that we are passing through
    ftype = 'text' # can change to 'url' or 'html'
    response = alchemyapi.sentiment(ftype, file_name)
    print(response)
    if response['status'] == 'OK':
        return jsonify(response) # ['docSentiment'] key contains needed data


    return jsonify(response)



# KeywordSentimentResult intakes SoP text and
# returns important keywords and the sentiment & relevance
# of each keyword.
@app.route('/tasha/keywords', methods=['POST', 'GET'])
@auth.login_required
def KeywordSentimentResult():
    """
    Returns keywords with their sentiment and relevance,
    as well as the count for positive, neutral and negative
    keywords given a text file (default).

    @rtype: JSON
    @return: JSON that contains keywords, their
        sentiment, their relevance and counts of 
        positive, neutral and negative keywords.
    """

    args = parser.parse_args()
    content = args['content'];
    # Create the AlchemyAPI Object
    alchemyapi = AlchemyAPI()

    file_name = content # this is the file/url that we are passing through
    ftype = 'text' # can change to 'url' or 'html'
    response = alchemyapi.keywords(ftype, file_name, {'sentiment': 1})
   
    if response['status'] == 'OK':

        # count of +, n, - words
        positive = 0
        neutral = 0
        negative = 0

        response["typeCount"] = {}
        
        keyword_list = response["keywords"]

        for element in keyword_list:
      
            if element["sentiment"]["type"] == "positive":
                positive += 1
            elif element["sentiment"]["type"] == "neutral":
                neutral += 1
            elif element["sentiment"]["type"] == "negative":
                negative += 1

        response["typeCount"]["positive"] = positive
        response["typeCount"]["neutral"] = neutral
        response["typeCount"]["negative"] = negative

        return jsonify(response) # ['keywords'] key contains needed data
                                 # ['typeCount'] key contains the type count


    return jsonify('status Not OK')


# TargetedSentimentResult intakes SoP text and the target
# phrase and returns the sentiment of the target phrase.
@app.route('/tasha/targeted', methods=['POST', 'GET'])
@auth.login_required
def TargetedSentimentResult():
    """
    Returns sentiment analysis results on the
    given a selection of a text (within text).
    
    @rtype: JSON
    @return: JSON that contains the overall
        sentiment analysis result.
    """

    args = parser.parse_args()
    content = args['content'];
    # Create the AlchemyAPI Object
    alchemyapi = AlchemyAPI()

    # this is the target text that we want to analyze
    target = 'my undergraduate degree at UBC' 

    file_name = content # this is the file/url that we are passing through
    ftype = 'text' # can change to 'url' or 'html'
    response = alchemyapi.sentiment_targeted(ftype, file_name, target)

    if response['status'] == 'OK':
        return jsonify(response) # ['docSentiment'] key contains needed data


    return jsonify('status Not OK')


@app.route('/tasha/concepts', methods=['POST', 'GET'])
@auth.login_required
def ConceptResult():
    """
    Returns relevant concepts given a text file.

    To get keyword sentiment results, you can pass a string
    ('html' or 'url') indicating the file type (ftype) as a 
    parameter to get the sentiment result of those files.

    @rtype: JSON
    @return: JSON that lists all relevant concepts.
    """

    args = parser.parse_args()
    content = args['content'];
    # Create the AlchemyAPI Object
    alchemyapi = AlchemyAPI()

    file_name = content # this is the file/url that we are passing through
    ftype = 'text' # can change to 'url' or 'html'
    response = alchemyapi.concepts(ftype, file_name)

    if response['status'] == 'OK':
        return jsonify(response) # ['concepts'] key contains needed data


    return jsonify('status Not OK')


@app.route('/tasha/emotions', methods=['POST', 'GET'])
@auth.login_required
def EmotionResult():
    """
    Returns emotions (anger, joy, fear, sadness, disgust) 
    for the given text file

    To get emotion results, you can pass a string ('html'
    or 'url') indicating the file type (ftype) as a parameter
    to get the emotion result of those files.

    @rtype: JSON
    @return: JSON that lists emotions and their percentages. 
    """

    args = parser.parse_args()
    content = args['content'];
    ftype = args.get('ftype');
    # Create the AlchemyAPI Object    
    alchemyapi = AlchemyAPI()

    file_name = content # this is the file/url that we are passing through
    if ftype != 'html':
    	ftype = 'text' # can change to 'url' or 'html'
    response = alchemyapi.emotion(ftype, file_name)

    if response['status'] == 'OK':
        return jsonify(response) # ['docEmotions'] key contains needed data


    return jsonify(response)

#required to run
if __name__ == '__main__':
    with app.app_context():
        cache.clear()
    app.run(debug=True)
    
