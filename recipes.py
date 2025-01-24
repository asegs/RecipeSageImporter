import json
import uuid
import sys

from login import get_recipes_with_login

HELP_MESSAGE = "recipes.py [output filename] (tag mappings)\nrecipes.py -t (tag mappings) // Prints your tags"
TAG_MAP = {}

def map_tag(tag):
    tag = tag.lower()
    if tag in TAG_MAP:
        return TAG_MAP[tag]
    return tag


def get_recipes_from_web():
    web_recipes = get_recipes_with_login()
    if not web_recipes:
        sys.exit(1)
    return web_recipes['data']['recipes']

def get_all_tags():
    tag_set = set()
    recipes = get_recipes_from_web()
    for recipe in recipes:
        for tag in recipe['categories']:
            tag_set.add(map_tag(tag))

    tag_list = list(tag_set)
    tag_list.sort()
    return tag_list


if len(sys.argv) >= 2 and sys.argv[1] == '-t':
    # Parse for tags
    tags = get_all_tags()
    for tag in tags:
        print(tag)
    sys.exit(0)

if len(sys.argv) == 3:
    TAG_MAP = json.load(open(sys.argv[2]))

if len(sys.argv) < 2:
    print(HELP_MESSAGE)
    sys.exit(0)

output_filename = sys.argv[1]


def add_key(old, new, val, new_key):
    if val is not None:
        new[new_key] = val


def old_to_new(recipe):
    new_recipe = {}
    new_recipe['recipeCategory'] = [map_tag(tag) for tag in recipe['categories']]
    new_recipe['recipeIngredient'] = recipe['ingredients']
    new_recipe['recipeInstructions'] = [{'@type': 'HowToStep', 'text': instruction} for instruction in
                                        recipe['instructions']]
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
    add_key(recipe, new_recipe, recipe.get('yield', ''), 'recipeYield')

    return new_recipe


recipes = get_recipes_from_web()

new_recipes = [old_to_new(r) for r in recipes]

with open(output_filename, 'w') as outfile:
    json.dump(new_recipes, outfile)
