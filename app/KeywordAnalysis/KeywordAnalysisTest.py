from KeywordAnalysis import KeywordAnalysis
import json
from pprint import pprint

#tests personality features
def test1():
    with open('jsonfile_test.json') as f:
        data = json.load(f)
    keywordAnalysis = KeywordAnalysis()
    response = keywordAnalysis.loadTokenizedDocuments(data)  
    print(response)

def main():
    test1()

if __name__=="__main__":
        main()
