from watsonapi import WatsonAPI

def test1():
    test_file = open("text_test.txt")
    test_text = test_file.read()
    alchemyapi = WatsonAPI()
    response = alchemyapi.profile(test_text)
    print(response)

# Parameters: first_name, last_name, twitter_handle=None, mendeleyID=None, email=None, sciverseID=None, googleScholarID=None
def main():
        test1()

if __name__=="__main__":
        main()
