# cravings
from setting import *
from food import *

if __name__ == '__main__':
	# run with "python3 cravings.py"
	print('-'*80)
	set = setting()
	ingr,exclude = find_food(set)
	recipe = recipe(ingr, exclude)
	describe(set, recipe)

	# print(recipe.get_label())