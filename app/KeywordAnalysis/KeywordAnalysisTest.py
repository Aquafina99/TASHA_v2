from KeywordAnalysis import KeywordAnalysis
import json
from pprint import pprint

#tests tokenized documents
def test1():
    with open('jsonfile_test.json') as f:
        data = json.load(f)
    keywordAnalysis = KeywordAnalysis()
    response = keywordAnalysis.loadTokenizedDocuments(data)  
    print(response)
    return response

#tests creating dictionary
def test2(docs):
    keywordAnalysis = KeywordAnalysis()
    response = keywordAnalysis.createDictionary(docs)
    print(response)

def main():
    docs = test1()
    test2(docs)

if __name__=="__main__":
        main()
