"""
Analyzes an SOP to obtain readability scores as json data
"""

import sys
import json
from readability_score.calculators.ari import *
from readability_score.calculators.colemanliau import *
from readability_score.calculators.dalechall import *
from readability_score.calculators.flesch import *
from readability_score.calculators.fleschkincaid import *
from readability_score.calculators.smog import *

def getReadabilityScore(sopText):
	"""
	Get Readability Score of text
	@param sopText: the SOP text
	@type sopText: string
	@return: the readability scores
	@rtype: json
	"""

	# create a readability dictionary to gather readability score calculated by different calculators
	readability_dict = {}
	readability_dict['ari'] = {}
	readability_dict['colemanliau'] = {}
	readability_dict['dalechall'] = {}
	readability_dict['fleschkincaid'] = {}
	readability_dict['flesch'] = {}
	readability_dict['smog'] = {}

	# calculate ARI scores
	ari = ARI(sopText, locale='en_GB')

	# save calculated ARI scores into the dictionary
	readability_dict['ari']['us_grade'] = ari.us_grade
	readability_dict['ari']['min_age'] = ari.min_age
	readability_dict['ari']['scores'] = ari.scores
	# reset file for further processing

	# calculate Coleman-Liau scores
	cl = ColemanLiau(sopText, locale='en_GB')

	readability_dict['colemanliau']['us_grade'] = cl.us_grade
	readability_dict['colemanliau']['min_age'] = cl.min_age
	readability_dict['colemanliau']['scores'] = cl.scores

	# calculate DaleChall scores
	dc = DaleChall(sopText, simplewordlist=open('DaleChallEasyWordList.txt').read(), locale='en_GB')

	readability_dict['dalechall']['readingindex'] = dc.readingindex
	readability_dict['dalechall']['us_grade'] = dc.us_grade
	readability_dict['dalechall']['min_age'] = dc.min_age
	readability_dict['dalechall']['scores'] = dc.scores

	# calculate Flesch scores
	f = Flesch(sopText, locale='en_GB')

	readability_dict['flesch']['scores'] = f.scores
	readability_dict['flesch']['reading_ease'] = f.reading_ease

	# calculate Flesch-Kincaid scores
	fk = FleschKincaid(sopText, locale='en_GB')

	readability_dict['fleschkincaid']['us_grade'] = fk.us_grade
	readability_dict['fleschkincaid']['min_age'] = fk.min_age
	readability_dict['fleschkincaid']['scores'] = fk.scores

	# calculate SMOG scores
	smaug = SMOG(sopText, locale='en_GB')

	readability_dict['smog']['us_grade'] = smaug.us_grade
	readability_dict['smog']['min_age'] = smaug.min_age
	readability_dict['smog']['scores'] = smaug.scores

	# convert dictionary to json object to be passed
	json_data = readability_dict
	return json_data
