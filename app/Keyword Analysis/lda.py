# -*- coding: utf-8 -*-
"""
@author: Diego Serrano
"""
from stop_words import get_stop_words
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
from gensim import corpora
from gensim.models.ldamulticore import LdaMulticore
from six import iteritems
from datetime import date
import matplotlib.pyplot as plt
import csv
import mysql.connector

FILEPATH = '/home/dfserrano/Projects/sandbox/data/oilsands_clean.csv'
CONTENT_CELL_INDEX = 4;
NUM_TOPICS = 100
NUM_ITERATIONS = 20
NUM_PASSES = 20
NUM_WORKERS = 3
NUM_TOPICS_PER_DOC = 5

NO_ABOVE = 0.25 # if a word appears in more than NO_ABOVE % docs, it is removed
NO_BELOW = 5    # if a word appears in less than NO_BELOW docs, it is removed

DB_HOST = '127.0.0.1'
DB_USERNAME = 'ta_user'
DB_PASSWORD = 'MPQFoeayuW5zIDHq'
DB_NAME = 'text_analysis'

DEBUG = False
DEBUG_DOCS = 1000

if DEBUG: 
    NUM_TOPICS = 10

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

def loadTokenizedDocuments(filepath, content_cell_index):
    """Creates a list of tokenized documents.  
    
    This procedure removes stopwords, keeping only nouns and verbs in their lemmatized form.
    The function assumes the text is at the cell with index 4.

    Args:
        filepath (str): File path
        content_cell_index (int) Index where the content to be analyzed is located

    Returns:
        bool: List of documents represented as a list of tokens

    """
    docs = []

    # create English stop words list
    stopwords = get_stop_words('en')
    
    # create wordnet lemmatizer
    lemmatizer = WordNetLemmatizer()
    
    with open(filepath, 'rb') as csvfile:
        doc = csv.reader(csvfile, delimiter=',', quotechar='"')
        doc_counter = 0;
        
        for row in doc:
            doc_tokens = word_tokenize(row[content_cell_index].decode('utf-8'))
            
            # keep only nouns and verbs
            pos_tokens = pos_tag(doc_tokens)
            nouns_tokens = [word.lower() for (word, pos) in pos_tokens if pos.startswith('N') and len(word) > 1]
            verbs_tokens = [word.lower() for (word, pos) in pos_tokens if pos.startswith('V') and len(word) > 1]
            
            # remove stop words from tokens
            stopped_nouns_tokens = [token for token in nouns_tokens if not token in stopwords]
            stopped_verbs_tokens = [token for token in verbs_tokens if not token in stopwords]
            
            # lemmatize tokens
            lemmatized_nouns_tokens = [lemmatizer.lemmatize(token) for token in stopped_nouns_tokens]
            lemmatized_verbs_tokens = [lemmatizer.lemmatize(token, pos='v') for token in stopped_verbs_tokens]
            
            docs.append(lemmatized_nouns_tokens + lemmatized_verbs_tokens)
            
            doc_counter += 1
            if DEBUG and doc_counter >= DEBUG_DOCS: break
        
            if doc_counter % 100 == 0:
                print("  Processing document " + str(doc_counter))
            
    return docs


def createDictionary(docs, output = 'dictionary.dict'):
    """Creates a dictionary from a list of tokenized documents.  
    
    This procedure removes extremely popular and infrequent words.

    Args:
        filepath (lst): List of tokenized documents
        output (str): Filepath to store the dictionary

    Returns:
        bool: The dictionary

    """
    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(docs)
    dictionary.save('dictionary.dct')
    
    # If a dictionary already exists, replace the previous two line by the following line
    # dictionary = corpora.Dictionary.load('dictionary.dct')
    
    freq = [doc_freq for word_id, doc_freq in iteritems(dictionary.dfs)]
    plotHistogram(freq, x_label = 'Words', y_label = 'Frequency', title = 'Dictionary Histogram - Unfiltered', 
                  bins = 100, output = 'dict-unfiltered.png')
    
    #words_above = getWordsAboveFreq(dictionary, 2800)
    #words_below = getWordsBelowFreq(dictionary, 3)
    
    # remove very common words (appear in more than 25% of docs) and words with very low frequency (appear in less than 5 docs)
    dictionary.filter_extremes(no_above = NO_ABOVE, no_below = NO_BELOW)
    freq = [doc_freq for word_id, doc_freq in iteritems(dictionary.dfs)]
    plotHistogram(freq, x_label = 'Words', y_label = 'Frequency', title = 'Dictionary Histogram - Filtered', 
                  bins = 100, output = 'dict-filtered.png')
    
    return dictionary
    

def createLDAModel(docs, dictionary, num_topics = 100, iterations = NUM_ITERATIONS, 
                   passes = NUM_PASSES, workers = 3, output = 'lda_model'):
    """Creates the LDA model for the given documents.  

    Args:
        docs (lst): List of tokenized documents
        dictionary (lst): The dictionary
        num_topics (int): The number of topics to discover
        iterations (int): The number of iterations of the LDA method
        passes (int): The number of passes of the LDA method
        workers (int): The number of workers employed in the creation of the model
        output (str): Prefix used to store the model in a set of files

    Returns:
        ldamodel: The LDA model
    """
    
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in docs]
    
    # generate LDA model
    ldamodel = LdaMulticore(corpus, id2word = dictionary, num_topics = NUM_TOPICS, 
                            iterations = iterations, passes = passes, workers = workers)
    ldamodel.save(output + '_i' + str(iterations) + '_p' + str(passes) + '_T' + str(num_topics) + '.lda')
    
    return ldamodel
    
                  
def plotHistogram(data, x_label = "X", y_label = "Frequency", title = "", bins = 20, output = "output.png"):
    """Plots a histogram and stores it as a PNG file.  

    Args:
        data (array): Array of data
        x_label (str): Label of the X axis
        y_label (str): Label of the Y axis
        title (str): Title of the histogram
        bins (int): Bins of the histogram
        output (str): File name for the image file to be stored
    """
    plt.clf()
    plt.hist(data, bins = bins)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    
    plt.savefig(output)
    

def getWordsAboveFreq(dictionary, freq):
    """Returns the words above the given frequency.  

    Args:
        dictionary (lst): List of words in a dictionary
        freq (int): Minimum threshold
    
    Returns:
        dict: Dictionary of words and counts
    """
    return [(dictionary[word_id], doc_freq) for word_id, doc_freq in iteritems(dictionary.dfs) if doc_freq > freq]


def getWordsBelowFreq(dictionary, freq):
    """Returns the words below the given frequency.  

    Args:
        dictionary (lst): List of words in a dictionary
        freq (int): Maximum threshold
    
    Returns:
        dict: Dictionary of words and counts
    """
    return [(dictionary[word_id], doc_freq) for word_id, doc_freq in iteritems(dictionary.dfs) if doc_freq < freq]
    

def storeDocsInDatabase(docs, host = '127.0.0.1', username = 'ta_user', 
                        password = 'MPQFoeayuW5zIDHq', database = 'text_analysis'):
    """Stores the documents in the database.  

    Args:
        docs (lst): List of tokenized documents
        host (str): Database host
        username (str): Database username
        password (str): Database password
        database (str): Database name
    """
    cnx = mysql.connector.connect(host = host, user= username, password = password, database = database)
    
    add_document = ("INSERT INTO document "
                   "(id, date, content, dateline, journal, section, byline, doc_type, publication_type, contact, highlight, question, load_date) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
               
    doc_counter = 0;
    
    with open(FILEPATH, 'rb') as csvfile:
        doc = csv.reader(csvfile, delimiter=',', quotechar='"')
    
        for row in doc:
            year = int(row[0])
            month = monthToNum(row[1].lower())
            day = int(row[2]) if row[2] != '' else 1
            doc_date = date(year, month, day)
            dateline = row[3][0:255]
            content = row[4]
            journal = row[5][0:255]
            section = row[7][0:255]
            byline = row[8][0:255]
            doc_type = row[9][0:255]
            publication_type = row[10][0:255]
            contact = row[11][0:255]
            highlight = row[12][0:255]
            question = row[13][0:255]
            load_date = row[14][0:255]
            
            data_document = (doc_counter, doc_date, content, dateline, journal, section, byline, doc_type, publication_type, contact, highlight, question, load_date)
    
            cursor = cnx.cursor()
            cursor.execute(add_document, data_document)
            cnx.commit()        
            cursor.close()
            
            doc_counter += 1
            
            if doc_counter % 100 == 0:
                print("  Document " + str(doc_counter))
            
            if DEBUG and doc_counter >= DEBUG_DOCS: break
        
    cnx.close()


def storeTopicTermsInDatabase(ldamodel, dictionary, host = '127.0.0.1', username = 'ta_user', 
                              password = 'MPQFoeayuW5zIDHq', database = 'text_analysis'):
    """Stores topics and their terms in the database.  

    Args:
        ldamodel (ldamodel): The LDA model
        dictionary (lst): List of words in a dictionary
        host (str): Database host
        username (str): Database username
        password (str): Database password
        database (str): Database name
    """
    cnx = mysql.connector.connect(host = host, user= username, password = password, database = database)

    add_topic = ("INSERT INTO topic_term (topic_id, term, term_prob) VALUES (%s, %s, %s)")
    
    for topic_id in range(0, NUM_TOPICS):
        topic_terms = ldamodel.get_topic_terms(topic_id, topn = 10)
                
        for term_id, term_prob in topic_terms:
            data_topic = (topic_id, dictionary[term_id], float(term_prob))

            cursor = cnx.cursor()
            cursor.execute(add_topic, data_topic)
            cursor.close()
            
        if topic_id % 10 == 0:
            print("  Storing topic " + str(topic_id))
    
    cnx.commit()
    cnx.close()
    

def storeTop5DocTopicInDatabase(ldamodel, dictionary, docs, host = '127.0.0.1', username = 'ta_user', 
                              password = 'MPQFoeayuW5zIDHq', database = 'text_analysis'):
    """Stores the top-5 topics of a document.  

    Args:
        ldamodel (ldamodel): The LDA model
        dictionary (lst): List of words in a dictionary
        docs (lst): List of tokenized documents
        host (str): Database host
        username (str): Database username
        password (str): Database password
        database (str): Database name
    """
    cnx = mysql.connector.connect(host = host, user= username, password = password, database = database)

    add_document = ("INSERT INTO document_topics (document_id, topic1_id, topic1_prob, topic2_id, topic2_prob, topic3_id, topic3_prob, topic4_id, topic4_prob, topic5_id, topic5_prob) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    
    doc_counter = 0
        
    for doc in docs:
        doc_topics = ldamodel[dictionary.doc2bow(doc)]
        doc_topics.sort(key=lambda topic: topic[1], reverse=True)
        
        topic_ids = [None] * NUM_TOPICS_PER_DOC
        topic_probs = [None] * NUM_TOPICS_PER_DOC
        
        topic_counter = 0
        
        for topic in doc_topics:
            topic_ids[topic_counter] = topic[0]
            topic_probs[topic_counter] = float(topic[1])
            
            topic_counter += 1    
            if topic_counter >= NUM_TOPICS_PER_DOC: 
                break
            
        
        data_document = (doc_counter, topic_ids[0], topic_probs[0], topic_ids[1], topic_probs[1], 
                         topic_ids[2], topic_probs[2], topic_ids[3], topic_probs[3], topic_ids[4], topic_probs[4])

        cursor = cnx.cursor()
        cursor.execute(add_document, data_document)
        cursor.close()        
        cnx.commit()
        
        doc_counter += 1
        if doc_counter % 100 == 0:
            print("  Assigning topic to document " + str(doc_counter))
    
    update_document_date = ("UPDATE document_topics SET document_date = (SELECT date FROM document WHERE id = document_id)")
    cursor = cnx.cursor()
    cursor.execute(update_document_date, ())
    cursor.close()        
    cnx.commit()
    
    cnx.close()


def showDocsPerTopic(ldamodel, dictionary, docs):
    """Stores a histogram with the number of documents per topic.  

    Args:
        ldamodel (ldamodel): The LDA model
        dictionary (lst): List of words in a dictionary
        docs (lst): List of tokenized documents
    """       
    topics_freq = []
    for doc in docs:
        doc_topics = ldamodel[dictionary.doc2bow(doc)]
        doc_topics.sort(key=lambda topic: topic[1], reverse=True)
        
        topics_freq.append(doc_topics[0][0])
    
    plotHistogram(topics_freq, x_label = "Topics", y_label = "Doc. Frequency", title = "Docs. per Topic", bins = 100, output = "docs_per_topic.png")

def monthToNum(month):
    month = month.lower()    
    
    return {
        'january': 1,
        'february': 2,
        'march': 3,
        'april': 4,
        'may': 5,
        'june': 6,
        'july': 7,
        'august': 8,
        'september': 9,
        'october': 10,
        'november': 11,
        'december': 12
    }.get(month, 1)
   
# load oil sands documents
print ("Tokenizing documents...")
docs = loadTokenizedDocuments(FILEPATH, CONTENT_CELL_INDEX)

# creates dictionary from the documents
print ("Creating dictionary...")
dictionary = createDictionary(docs, output = 'dictionary.dict')

# creates LDA model
print ("Creating LDA model...")
ldamodel = createLDAModel(docs, dictionary, num_topics = NUM_TOPICS, iterations = NUM_ITERATIONS, 
                          passes = NUM_PASSES, workers = NUM_WORKERS, output = 'lda_model')

# stores relation of topics and terms
print ("Storing documents...")
storeDocsInDatabase(docs, host = DB_HOST, username = DB_USERNAME, 
                    password = DB_PASSWORD, database = DB_NAME)

# stores relation of topics and terms
print ("Storing the topics and associated terms...")
storeTopicTermsInDatabase(ldamodel, dictionary, host = DB_HOST, username = DB_USERNAME, 
                          password = DB_PASSWORD, database = DB_NAME)
                                  
# stores top-5 document topics
print ("Storing the top-5 topics for each document...")
storeTop5DocTopicInDatabase(ldamodel, dictionary, docs, host = DB_HOST, username = DB_USERNAME, 
                          password = DB_PASSWORD, database = DB_NAME)

# stores docs. per topic histogram
print ("Storing the top-5 topics for each document...")
showDocsPerTopic(ldamodel, dictionary, docs)