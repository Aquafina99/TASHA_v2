#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Diego Serrano
"""
from stop_words import get_stop_words

class KeywordAnalysis:
    num_topics = 100
    num_iterations = 20
    num_passes = 20
    num_workers = 3
    num_topics_per_doc = 5
    no_above = 0.25
    no_below = 5

    
    def loadTokenizedDocuments(documents):
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
        
        for row in documents['docs']:
            content = row['content']
            doc_tokens = word_tokenize(content.decode('utf-8'))
            
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
        print(docs)
        return docs

