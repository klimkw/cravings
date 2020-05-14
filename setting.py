# setting for weather and date

import requests
import json
from datetime import date, datetime
from pytz import timezone
import sys
import holidays

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
		
		self.is_harsh = harsh(self.temp_tuple, self.code)

def get_food_holidays():
	# used only cinco de mayo for this project
	food_holidays = holidays.HolidayBase()
	year = date.today().year
	food_holidays.append({date(year, 5, 5): 1})
	# can add additional holidays here
	return food_holidays

def harsh(temp_tuple, code):
	# returns boolean
	temp = temp_tuple[0]
	if temp < 20 or temp > 104:
		return True

	weather = code.replace("_", " ").split()
	if ("heavy" in weather) or ("freezing" in weather) or ("tstorm" in weather):
		return True

	return False

def describe(set):
	describe_env(set)
	if not set.is_food_hol:
		describe_emo(set)

# Describes environmental setting
def describe_env(set):
	print("It's a", set.warmth, set.weather, set.day, set.period)
	pass

# Describes emotional setting
def describe_emo(set):
	str = emocode_to_str(set.emotion)
	print("You are feeling", str)
	pass

def emocode_to_str(code):
	switcher = {
		0: "neutral",
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

# def describe_setting(weather):
	
# 	# switch_weather = {
# 	# 	1: "clouds drift",
# 	# 	2: "wind blows",
# 	# 	3: "sun shines",
# 	# 	4: "snow falls",
# 	# 	5: "rain pours",
# 	# }

# 	# switch_sun = {
# 	# 	1: "sun rises and the ",
# 	# 	2: "sun begins to set and the ",
# 	# }

# 	# return "As the sun "

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
	print('0. Neutral')
	print('1. Happy')
	print('2. Sad')
	print('3. Worried')
	print('4. Angry')
	print()
	emo_input = int(sys.stdin.readline().replace('\n', ''))
	if not 0 <= emo_input <= 6:
		print("Unable to read input. Please try again.")
		sys.exit()
	print('-'*80)

	return emo_input
