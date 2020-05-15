# setting for weather and date

import requests
import json
from datetime import date, datetime
from pytz import timezone
import sys
import holidays
from nltk.corpus import wordnet as wn
import random

class setting():
	def __init__(self):
		# retrieve weather, date, and time (and holiday if applicable)
		url = "https://api.climacell.co/v3/weather/realtime"
		querystring = {"lat":"40.730610","lon":"-73.935242","unit_system":"us","fields":"temp,weather_code","apikey":"uJFR9RCHgruTcTDPQHuGE8PkAnYtDgQ5"}
		response = requests.request("GET", url, params=querystring)
		resp_dict = json.loads(response.text)
		self.temp_tuple = resp_dict["temp"]['value'], resp_dict['temp']['units']
		self.code = resp_dict["weather_code"]['value']
		self.date = date.today()
		self.time = get_time("US/Eastern")
		self.weather = code_to_weather(self.code)
		self.warmth = get_warmth(self.temp_tuple)
		self.period = get_period(self.time)
		self.day = number_to_day(self.date.isoweekday())
		food_hols = get_food_holidays()
		self.is_food_hol = self.date in food_hols
		
		if self.is_food_hol:
			self.food_hol_code = food_hols[self.date]
		else:
			# get emotion from user
			self.emotion = get_emo_code()
		
		# 0 for normal weather, 1 for hot weather, 2 for cold weather
		self.harsh = get_harsh_code(self.temp_tuple, self.code)

def get_food_holidays():
	# used only cinco de mayo for this project
	food_holidays = holidays.HolidayBase()
	year = date.today().year
	food_holidays.append({date(year, 5, 5): 1})
	# can add additional holidays here
	return food_holidays

def get_harsh_code(temp_tuple, code):
	# returns int between 0-2
	temp = temp_tuple[0]
	weather = code.replace("_", " ").split()
	
	if temp > 104:
		return 1
	elif temp < 20 or ("heavy" in weather) or ("freezing" in weather) or ("tstorm" in weather):
		return 2
	else:
		return 0

def describe(set, recipe):
	describe_1(set)
	if not set.is_food_hol:
		describe_2(set, recipe)
	else:
		describe_hol()
	describe_3(recipe)

# Describes environmental setting
def describe_1(set):
	print("On a", set.warmth, set.weather, set.day, set.period)
	pass

# Describes emotional setting
def describe_2(set, recipe):
	e_code = set.emotion
	str = emocode_to_str(e_code)
	emo_noun = get_noun(str)
	verb = random_synonym(e_code)

	print("Have some", recipe.get_label(), "to", verb, "the", emo_noun)
	pass

def describe_3(recipe):
	print("Recipe:", recipe.get_url())

def describe_hol(recipe):
	print("Have some", recipe.get_label(), "to celebrate!")

def get_noun(word):
	related_nouns = []

	for lemma in wn.lemmas(wn.morphy(word, wn.ADJ), pos="a"):
		for related_form in lemma.derivationally_related_forms():
			for synset in wn.synsets(related_form.name(), pos=wn.NOUN):
				for noun in synset.lemmas():
					if noun.name() not in related_nouns:
						related_nouns.append(noun.name())

	if len(related_nouns) == 0:
		for lemma in wn.lemmas(wn.morphy(word, wn.VERB), pos="v"):
			for related_form in lemma.derivationally_related_forms():
				for synset in wn.synsets(related_form.name(), pos=wn.NOUN):
					for noun in synset.lemmas():
						if noun.name() not in related_nouns:
							related_nouns.append(noun.name())

	return related_nouns[random.randrange(len(related_nouns))]

def random_synonym(e_code):
	if e_code == 1:
		return get_synonym("celebrate")
	else:
		rand_syn = ["soothe","ease","relieve","alleviate"]
		return get_synonym(rand_syn[random.randrange(len(rand_syn))])

def emocode_to_str(code):
	switcher = {
		1: "happy",
		2: "sad",
		3: "worried",
		4: "angry"
	}
	str = switcher.get(code)
	return str

def code_to_weather(code):
	weather = code.replace("_", " ").split()
	if len(weather) > 1 and ("heavy" in weather or "light" in weather):
		weather = weather[-1:] + weather[:-1]
	if "tstorm" in weather:
		return "stormy"
	return (" ".join(weather))

def get_time(zone):
	tz = timezone(zone)
	time = datetime.now(tz).strftime("%H:%M:%S")
	print(time)
	return time

def get_period(time):
	hour = int(time.split(":")[0])

	if hour == 0:
		period = "midnight"
	elif 1 <= hour and hour <= 10:
		period = "morning"
	elif hour == 11 or hour == 12:
		period = "noon"
	elif 13 <= hour and hour <= 16:
		period = "afternoon"
	elif 17 <= hour and hour <= 19:
		period = "evening"
	else:
		period = "night"

	return period

def get_warmth(temp_tuple):
	temp = temp_tuple[0]

	if temp < 20:
		warmth = "freezing"
	elif 20 <= temp and temp <= 49:
		warmth = "cold"
	elif 50 <= temp and temp <= 74:
		warmth = "cool"
	elif 75 <= temp and temp <= 89:
		warmth = "warm"
	elif 90 <= temp and temp <= 104:
		warmth = "hot"
	else:
		warmth = "blazing hot"

	return warmth

def number_to_day(number):
	# works with isoweekday() method
	switcher = {
		1: "Monday",
		2: "Tuesday",
		3: "Wednesday",
		4: "Thursday",
		5: "Friday",
		6: "Saturday",
		7: "Sunday"
	}
	day = switcher.get(number)
	return day

def get_emo_code():
	print("Enter # of emotion:")
	print('1. Happy')
	print('2. Sad')
	print('3. Worried')
	print('4. Angry')
	print()
	emo_input = int(sys.stdin.readline().replace('\n', ''))
	if not 1 <= emo_input <= 4:
		print("Unable to read input. Please try again.")
		sys.exit()
	print('-'*80)

	return emo_input

def get_synonym(word):
	synonyms = []

	for synset in wn.synsets(word):
		for lemma in synset.lemmas():
			synonyms.append(lemma.name())

	return synonyms[random.randrange(len(synonyms))]