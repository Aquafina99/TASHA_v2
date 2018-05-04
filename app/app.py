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
parser.add_argument('features', action='append')
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
    watsonapi = WatsonAPI()

    response = watsonapi.profile(content)

    return jsonify(response)

@app.route('/tasha/alchemy', methods=['POST', 'GET'])
@auth.login_required
def EmotionResult():
    """
    Returns language analysis based on watson natural language understanding 
    includes the following:
      - Emotions (anger, joy, fear, sadness, disgust) for given text,
      - Sentiment (positive/negative)
      - Entities
      - Keywords
      - Metadata
      - Relations
      - Concepts 
    If arguments include specific features, will only run the analysis listed
    @rtype: JSON
    @return: JSON that lists all alchemy analysis and their percentages. 
    """

    args = parser.parse_args()
    content = args['content']
    features = args.get('features', [])
    
    watsonapi = WatsonAPI()
    response = watsonapi.alchemy(content,features)

    if response['status'] == 'OK':
        return jsonify(response) # ['docEmotions'] key contains needed data


    return jsonify(response)

#required to run
if __name__ == '__main__':
    with app.app_context():
        cache.clear()
    app.run(debug=True)
    
