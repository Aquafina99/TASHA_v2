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
    
#tests creating lda model
def test3(docs, dictionary):
    keywordAnalysis = KeywordAnalysis()
    response = keywordAnalysis.createLDAModel(docs, dictionary)
    print(response)

def main():
    docs = test1()
    dictionary = test2(docs)
    response = test3(docs, dictionary)
    print(response)

if __name__=="__main__":
        main()
