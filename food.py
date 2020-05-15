# generate recipe based on settings

import requests
import json
import random

class recipe(object):
	def __init__(self, title_or_ingredient, exclusions):
		url = "https://api.edamam.com/search"
		r_from = str(random.randrange(10))
		r_to = str(int(r_from)+1)
		querystring = {"q":title_or_ingredient,"excluded":exclusions,"from":r_from, "to":r_to,"app_id":"5003bb48","app_key":"e764f6502abe3c306441bbe5adc5649f"}
		self.response = requests.request("GET", url, params=querystring)

	def get_url(self):
		result_dict = json.loads(self.response.text)
		for hit in result_dict["hits"]:
			return (hit['recipe']['url'])

	def get_label(self):
		# get ingredients of first hit
		result_dict = json.loads(self.response.text)
		first_hit = result_dict["hits"][0]
		label = first_hit['recipe']['label']
		if 'recipe' in label:
			label.replace('recipe','')
		return label

		
def find_food(set):
	if set.is_food_hol:
		hol_code = set.food_hol_code
		return generate_food_hol(hol_code)

	e_code = set.emotion
	h_code = set.harsh

	return generate_food(e_code,h_code)

def generate_food_hol(hol_code):
	if hol_code == 1:
		print("Happy Cinco de Mayo!")
		return "tacos", None

	# add additional holidays here!
	return None

def generate_food(e_code,h_code):
	if e_code == 1:
		# happy
		if h_code == 1:
			# happy + hot
			return "ice cream", None
		elif h_code == 2:
			# happy + cold
			return "soup", None

		else:
			#happy + normal
			random_food =['chicken','fish','beef','vegetables']
			i = random.randrange(4)
			return random_food[i], None

	elif e_code == 2:
		# sad
		if h_code == 1:
			# sad + hot
			# the omega-3 oils found in fish are linked to lower levels of depression
			# salmon not only has omega-3 oils but also rich in vitamin D, crucial in mood maintaining
			return "salmon", None
		elif h_code == 2:
			# sad + cold
			# fermented food, such as kimchi
			# supports healthy gut functions resulting in better serotonin production => better mood
			# warm food brings comfort during cold weather
			return "kimchi stew", None
		else:
			# sad + normal
			return "fish", None

	elif e_code == 3:
		# worried
		i = random.randrange(3)
		if h_code == 1:
			# worried + hot
			# nuts/seeds support brain function and reduce risk of depression
			# great snack for the worried
			random_snack = ['seeds','oats','nuts']
			return random_snack[i], None
		elif h_code == 2:
			# worried + cold
			# quick easy warm snack for a grab-and-go
			random_snack = ['toast','bread','sandwich']
			return random_snack[i], None
		else:
			# worried + normal
			return "nuts", None

	else:
		# Angry
		random_food =['chicken','fish','beef','vegetables']
		i = random.randrange(3)
		return random_food[i], "coffee,tomatoes,chilli,wheat,milk"

if __name__ == '__main__':
	new = recipe("this")

	# search for recipe based on feeling and weather (ingredients that help curb certain feelings, ingredients that feel good on certain weathers)
	# from recipe, take key ingredients and write short write up
