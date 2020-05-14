# generate recipe based on settings

import requests
import json
import random

class recipe(object):
	def __init__(self, title_or_ingredient, exclusions):
		url = "https://api.edamam.com/search"
		querystring = {"q":title_or_ingredient,"excluded":exclusions,"to":"3","app_id":"5003bb48","app_key":"e764f6502abe3c306441bbe5adc5649f"}
		self.response = requests.request("GET", url, params=querystring)

	def get_titles(self):
		result_dict = json.loads(self.response.text)
		for hit in result_dict["hits"]:
			print()
			print(hit['recipe']["label"], hit['recipe']['url'])
		
def find_food(set):
	if set.is_food_hol:
		code = set.food_hol_code
		hol = code_to_hol(code)

		if code == 1:
			print("Happy Cinco de Mayo!")
			return "tacos", None

	code = set.emotion

	if set.is_harsh:
		temp = set.temp_tuple[0]
		hot = True if temp > 70 else False

		if code == 0 or code == 1:
			# Neutral or happy
			if hot:
				print("Have an ice cream!")
				return "ice cream", None
			else:
				print("Have a nice bowl of warm soup!")
				return "soup", None

		elif code == 2:
			# Sad
			print("Some comfort food that will boost your mood!")
			if hot:
				# the omega-3 oils found in fish are linked to lower levels of depression
				return "fish", None
			else:
				# fermented food, such as kimchi
				# supports healthy gut functions resulting in better serotonin production => better mood
				# salmon not only has omega-3 oils but also rich in vitamin D, crucial in mood maintaining
				# return "salmon", None
				return "kimchi stew", None

		elif code == 3:
			# Worried
			print("Cast your worries aside with a delectable snack!")
			i = random.randrange(3)
			if hot:
				# nuts/seeds support brain function and reduce risk of depression
				# great snack for the worried
				random_snack = ['seeds','oats','nuts']
				return random_snack[i], None
			else:
				# quick easy warm snack for a grab-and-go
				random_snack = ['toast','bread','sandwich']
				return random_snack[i], None

		else:
			# Angry
			print("Calm down with some of these foods, just avoid certain ingredients!")
			random_food =['chicken','fish','beef','vegetables']
			i = random.randrange(3)
			return random_food[i], "coffee,tomatoes,chilli,wheat,milk"

	else:
		if code == 0 or code == 1:
			# Neutral or Happy
			print("Here are some ideas for food!")
			random_food =['chicken','fish','beef','vegetables']
			i = random.randrange(4)
			return random_food[i], None

		elif code == 2:
			# Sad
			print("Some comfort food that will boost your mood!")
			return "fish", None

		elif code == 3:
			# Worried
			print("Cast your worries aside with a delectable snack!")
			return "nuts", None
		
		else:
			# Angry
			print("Calm down with some of these foods, just avoid certain ingredients!")
			random_food =['chicken','fish','beef','vegetables']
			i = random.randrange(4)
			return random_food[i], "coffee,tomatoes,chilli,wheat,milk"

def code_to_hol(code):
	switcher = {
		1: "Cinco de Mayo"
	}
	hol = switcher.get(code)
	return hol

if __name__ == '__main__':
	new = recipe("this")

	# search for recipe based on feeling and weather (ingredients that help curb certain feelings, ingredients that feel good on certain weathers)
	# from recipe, take key ingredients and write short write up
