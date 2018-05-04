import sys
from watsonapi import WatsonAPI
from ConfigParser import SafeConfigParser
import json

#tests personality features
def test1(test_text):
    watsonapi = WatsonAPI()
    response = watsonapi.profile(test_text)
    print(response)

#tests all alchemy features
def test2(test_text):
    watsonapi = WatsonAPI()
    response = watsonapi.alchemy(test_text)
    outfile = open('testfiles/test2_response.txt', 'w+')
    json.dump(response, outfile)
    print(json.dumps(response))
    outfile.close()

#tests choosing specific alchemy features
def test3(test_text):
    watsonapi = WatsonAPI()
    features = ['emotion', 'entities']
    response = watsonapi.alchemy(test_text, features)
    outfile = open('testfiles/test3_response.txt', 'w+')
    json.dump(response, outfile)
    print(json.dumps(response))
    outfile.close()

    


# Parameters: first_name, last_name, twitter_handle=None, mendeleyID=None, email=None, sciverseID=None, googleScholarID=None
def main():
    test_file = open("text_test.txt")
    test_text = test_file.read()
    test1(test_text)
    test2(test_text)
    test3(test_text)
    test_file.close()

if __name__=="__main__":
        main()
