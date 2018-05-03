from getSentiment import *
from alchemyapi import AlchemyAPI
import time


file1 = open("happy.txt", "r") # opened file
list1 = file1.readlines() #list of lines
file2 = open("depression.txt", "r") #opened file
list2 = file2.readlines() # list of lines
file3 = open("personality.txt", "r") #opened file
list3 = file3.readlines() # list of lines


text1 = " ".join(list1) #string
text2 = " ".join(list2) # string
text3 = "I had dinner."
text4 = ""
text5 = " ".join(list3) # string

url = "www.google.com"


def testSentimentResult():
    """
    Performs unit test on SentimentResult function
    """
    
    # Test happy text, sad text, neutral text, no text and url cases
    response1 = SentimentResult(text1)
    response2 = SentimentResult(text2)
    response3 = SentimentResult(text3)
    response4 = SentimentResult(text4)
    response5 = SentimentResult(url, 'url')

    #print(response1['docSentiment'])
    print(response1)
    print(response2)
    print(response3)
    print(response4)

    # Test if watson worked
    assert(response1['status'] == 'OK'), "did not return ['status'] == OK"
    assert(response2['status'] == 'OK'), "did not return ['status'] == OK"
    assert(response3['status'] == 'OK'), "did not return ['status'] == OK"
    assert(response4 == 'status Not OK'), "status returned ok for empty text"
    assert(response5['status'] == 'OK'), "did not return ['status'] == OK"

    # Test watson's functionality / viability
    assert(response1['docSentiment']['score'] > response2['docSentiment']['score']), "text1 has lower score than text2 == bad :("
    assert(response1['docSentiment']['type'] == "positive"), "text1's sentiment is not positive == bad"
    assert(response2['docSentiment']['type'] == "negative"), "text2's sentiment is not negative == bad"
    assert(response3['docSentiment']['type'] == "neutral"), "text3's sentiment is not neutral == bad"


def testKeywordSentimentResult():
    """
    Performs unit test on KeywordSentimentResult function
    """
    
    # Test happy text, sad text, neutral text, no text and url cases
    response1 = KeywordSentimentResult(text1)
    response2 = KeywordSentimentResult(text2)
    response3 = KeywordSentimentResult(text3)
    response4 = KeywordSentimentResult(text4)
    response5 = KeywordSentimentResult(url, 'url')

    #print(response1['keywords'])
    #print(response1['typeCount'])
    #print(response1)
    #print(response2)
    #print(response3)
    #print(response4)

    # Test if watson worked
    assert(response1['status'] == 'OK'), "did not return ['status'] == OK"
    assert(response2['status'] == 'OK'), "did not return ['status'] == OK"
    assert(response3['status'] == 'OK'), "did not return ['status'] == OK"
    assert(response4 == 'status Not OK'), "status returned ok for empty text"
    assert(response5['status'] == 'OK'), "did not return ['status'] == OK"


def testTargetedSentimentResult():
    """
    Performs unit test on TargetedSentimentResult function
    """
    # targets must exist in document
    target1 = "happy"
    target2 = "depression"
    target3 = "Agumon digivole to... Greymon!"
    
    # Test happy text, sad text, neutral text, no text and url cases
    response1 = TargetedSentimentResult(text1, target1)
    response2 = TargetedSentimentResult(text2, target2)
    response3 = TargetedSentimentResult(text3, "dinner")
    response4 = TargetedSentimentResult(text4, target1)
    response5 = TargetedSentimentResult(url, target3, 'url')

    #print(response1['docSentiment'])

    # Test if watson worked
    assert(response1['status'] == 'OK'), "did not return ['status'] == OK"
    assert(response2['status'] == 'OK'), "did not return ['status'] == OK"
    assert(response3['status'] == 'OK'), "did not return ['status'] == OK"
    assert(response4 == 'status Not OK'), "status returned ok for empty text"
    assert(response5 == 'status Not OK'), "Agumon digivoles to... Greymon! exists in Google"

    # Test watson's functionality / viability
    assert(response1['docSentiment']['score'] > response2['docSentiment']['score']), "text1 has lower score than text2 == bad :("
    assert(response1['docSentiment']['type'] == "positive"), "text1's sentiment is not positive == bad"
    assert(response2['docSentiment']['type'] == "negative"), "text2's sentiment is not negative == bad"


def testConceptResult():
    """
    Performs unit test on ConceptResult function
    """

    # Test happy text, sad text, neutral text, no text and url cases
    response1 = ConceptResult(text1)
    response2 = ConceptResult(text2)
    response3 = ConceptResult(text3)
    response4 = ConceptResult(text4)
    response5 = ConceptResult(url, 'url')

    #print(ConceptResult(text5))

    # Test if watson worked
    assert(response1['status'] == 'OK'), "did not return ['status'] == OK"
    assert(response2['status'] == 'OK'), "did not return ['status'] == OK"
    assert(response3['status'] == 'OK'), "did not return ['status'] == OK"
    assert(response4 == 'status Not OK'), "status returned ok for empty text"
    assert(response5['status'] == 'OK'), "did not return ['status'] == OK"

    #print(response1['concepts'])


def testEmotionResult():
    """
    Performs unit test on EmotionResult function
    """

    response1 = EmotionResult('hello')
    response2 = EmotionResult('hello')
    response3 = EmotionResult('hello')
    response4 = EmotionResult('hello')
    response5 = EmotionResult(url, 'url')

    # Test if watson worked
    print(response1)
    print(response2)
    print(response3)
    print(response4)
    print(response5)

    assert(response1['status'] == 'OK'), "did not return ['status'] == OK"
    assert(response2['status'] == 'OK'), "did not return ['status'] == OK"
    assert(response3['status'] == 'OK'), "did not return ['status'] == OK"
    assert(response4 == 'status Not OK'), "status returned ok for empty text"
    assert(response5['status'] == 'OK'), "did not return ['status'] == OK"

    # Test watson's functionality / viabilityha
    assert(response1['docEmotions']['joy'] > response1['docEmotions']['sadness']), "text1 (happy.txt)'s emotion joy < sadness, which is bad :("
    assert(response2['docEmotions']['sadness'] > response2['docEmotions']['joy']), "text2 (depression.txt)'s emotion joy > sadness, which is bad :("


def testProfileResult():
    """
    Performs unit test on ProfileResult function
    """
    response1 = ProfileResult(text5) # long text (over 100 words)
    #response2 = ProfileResult(text4) # no text
    #response3 = ProfileResult(text1) #short text (less than 100 words)

    print(response1)
    #print(response2)
    #print(response3)

    assert(response1['word_count'] > 100), "word count was less than 100 words for long text. == not True"
    assert(response1['personality']), "Personality analysis does not exist. == bad"
    assert(response1['needs']), " Consumer Needs analysis does not exist. == bad"
    assert(response1['values']), " Values analysis does not exist. == bad"

    #assert(response2['error']), "Returned no error despite having no text. == bad"
    #assert(response3['error']), "Returned no error despite length < 100. == bad"




def main():

    testSentimentResult()
    #testKeywordSentimentResult()
    #testTargetedSentimentResult()
    #testConceptResult()
    #testEmotionResult()
    #testProfileResult()

    # Note: sometimes will report this: HTTPConnectionPool(host='access.alchemyapi.com', port=80): Max retries exceeded with url: /calls/text/TextGetEmotion?apikey=22c9c5bce96775adc4a2ffaef79251de9eb2a4dd&outputMode=json (Caused by <class 'httplib.BadStatusLine'>: '')
    print("All tests ended successfully. Cheers! :D")

    file1.close()
    file2.close()
    file3.close()

if __name__ == "__main__":
    main()
