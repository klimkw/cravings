# cravings

from nltk.corpus import wordnet as wn
from setting import *
from food import *

def find_synonyms(word):
	synonyms = []

	for synset in wn.synsets(word):
		for lemma in synset.lemmas():
			synonyms.append(lemma.name())

	return set(synonyms)

if __name__ == '__main__':
	# run with "python3 cravings.py"
	print('-'*80)
	set = setting()
	describe(set)
	ingr,exclude = find_food(set)
	recipe = recipe(ingr, exclude)
	recipe.get_titles()