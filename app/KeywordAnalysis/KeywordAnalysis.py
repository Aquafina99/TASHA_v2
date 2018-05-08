#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Diego Serrano
"""
from stop_words import get_stop_words
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
from six import iteritems
from datetime import date
from gensim import corpora



class KeywordAnalysis:
    num_topics = 100
    num_iterations = 20
    num_passes = 20
    num_workers = 3
    num_topics_per_doc = 5
    no_above = 0.25
    no_below = 5

    
    def loadTokenizedDocuments(self,documents):
        """ Creates a list of tokenized documents.
        This procedure removes stopwords, keeping only nouns and verbs in their lemmatized form.
        The function assumes the text is at the cell with index 4.
        
        Args: documents (json) json object that contains an array of collection of documents
        Returns: bool: List of documents represented as a list of tokens
        """
        docs = []
        # create English stop words list
        stopwords = get_stop_words('en')
        # create wordnet lemmatizer
        lemmatizer = WordNetLemmatizer()
        
        doc_counter = 0;
        
        for doc in documents['collection']:
            content = doc['content']
            doc_tokens = word_tokenize(content)
            
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
        
            if doc_counter % 100 == 0:
                print("  Processing document " + str(doc_counter))
        return docs

    def createDictionary(self, docs):
        """Creates a dictionary from a list of tokenized documents.  
        This procedure removes extremely popular and infrequent words.
        Args: docs (lst): List of tokenized documents
        Returns: bool: The dictionary
        """
        # turn our tokenized documents into a id <-> term dictionary
        dictionary = corpora.Dictionary(docs)
        #dictionary.save('dictionary.dct')
        
        # If a dictionary already exists, replace the previous two line by the following line
        # dictionary = corpora.Dictionary.load('dictionary.dct')
        
        freq = [doc_freq for word_id, doc_freq in iteritems(dictionary.dfs)]
        #self.plotHistogram(freq, x_label = 'Words', y_label = 'Frequency', title = 'Dictionary Histogram - Unfiltered', 
        #              bins = 100, output = 'dict-unfiltered.png')
        
        # remove very common words (appear in more than 25% of docs) and words with very low frequency (appear in less than 5 docs)
        dictionary.filter_extremes(no_above = NO_ABOVE, no_below = NO_BELOW)
        freq = [doc_freq for word_id, doc_freq in iteritems(dictionary.dfs)]
        #self.plotHistogram(freq, x_label = 'Words', y_label = 'Frequency', title = 'Dictionary Histogram - Filtered', 
        #              bins = 100, output = 'dict-filtered.png')
        
        return dictionary
    
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
