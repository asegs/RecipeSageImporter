import json
import uuid
import sys

HELP_MESSAGE = "recipes.py [input filename] [output filename] (tag mappings) \nrecipes.py -t [input_filename] // Prints your tags"

def get_recipes_from_file(input_filename):
	body = json.load(open(input_filename))
	return body['data']['recipes']

def get_all_tags(input_filename):
	tag_set = set()
	recipes = get_recipes_from_file(input_filename)
	for recipe in recipes:
		for tag in recipe['categories']:
			tag_set.add(tag.lower())

	tag_list = list(tag_set)
	tag_list.sort()
	return tag_list

if len(sys.argv) == 3 and sys.argv[1] == '-t':
	# Parse for tags
	tags = get_all_tags(sys.argv[2])
	for tag in tags:
		print(tag)
	sys.exit(0)



if len(sys.argv) < 3:
	print(HELP_MESSAGE)
	sys.exit(0)

input_filename = sys.argv[1]
output_filename = sys.argv[2]

TAG_MAP = {}
if len(sys.argv) == 4:
	TAG_MAP = json.load(open(sys.argv[3]))



def map_tag(tag):
	tag = tag.lower()
	if tag in TAG_MAP:
		return TAG_MAP[tag]
	return tag

def add_key(old, new, val, new_key):
	if val is not None:
		new[new_key] = val


def old_to_new(recipe):
	new_recipe = {}
	new_recipe['recipeCategory'] = [map_tag(tag) for tag in recipe['categories']]
	new_recipe['recipeIngredient'] = recipe['ingredients']
	new_recipe['recipeInstructions'] = [{'@type': 'HowToStep', 'text': instruction} for instruction in recipe['instructions']]
	new_recipe['datePublished'] = recipe['createdAt']
	new_recipe['name'] = recipe['name']
	new_recipe['comment'] = [{
        "@type": "Comment",
        "name": "Author Notes",
        "text": recipe.get('notes', '')
      }]
	new_recipe['isBasedOn'] = recipe['url']
	new_recipe['@context'] = 'http://schema.org'
	new_recipe['@type'] = "Recipe"

	new_recipe['totalTime'] = ""
	new_recipe['favorite'] = False
	new_recipe['slug'] = ''
	new_recipe['slugId'] = ''
	new_recipe['identifier'] = str(uuid.uuid4())

	add_key(recipe, new_recipe, recipe.get('notes', ''), 'notes')
	add_key(recipe, new_recipe, recipe.get('description', ''), 'description')
	add_key(recipe, new_recipe, recipe.get('ingredients', []), 'components')
	add_key(recipe, new_recipe, [recipe.get('image', '')], 'image')
	add_key(recipe, new_recipe, recipe.get('prepTime', ''), 'prepTime')
	add_key(recipe, new_recipe, recipe.get('cookTime', ''), 'cookTime')
	add_key(recipe, new_recipe, recipe.get('yield', ''), 'yield')

	return new_recipe


recipes = get_recipes_from_file(input_filename)

new_recipes = [old_to_new(r) for r in recipes]

with open(output_filename, 'w') as outfile: 
    json.dump(new_recipes, outfile)


