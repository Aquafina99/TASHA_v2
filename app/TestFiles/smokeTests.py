from __future__ import print_function
from alchemyapi import AlchemyAPI
import json

demo_url = 'http://www.google.com'

# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()

print('Processing url: ', demo_url)
print('')

response = alchemyapi.sentiment('url', demo_url)

if response['status'] == 'OK':
    print('## Response Object ##')
    print(json.dumps(response, indent=4))

    print('')
    print('## Document Sentiment ##')
    print('type: ', response['docSentiment']['type'])
    print('')


    if 'score' in response['docSentiment']:
        print('score: ', response['docSentiment']['score'])
else:
    print('Error in sentiment analysis call: ', response['statusInfo'])

'''
response = alchemyapi.author('url', demo_url)

if response['status'] == 'OK':
    print('## Response Object ##')
    print(json.dumps(response, indent=4))

    print('')
    print('## Author ##')
    print('author: ', response['author'].encode('utf-8'))
    print('')
else:
    print('Error in author extraction call: ', response['statusInfo'])
'''

print('Processing url: ', demo_url)
print('')

response = alchemyapi.text('url', demo_url)

if response['status'] == 'OK':
    print('## Response Object ##')
    print(json.dumps(response, indent=4))

    print('')
    print('## Text ##')
    print('text: ', response['text'].encode('utf-8'))
    print('')
else:
    print('Error in text extraction call: ', response['statusInfo'])

