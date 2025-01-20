### So your phone is running a bit hot?

#### Steps to import to RecipeSage

1. Sign in to https://www.recipebox.com/users/recipes
2. In the inspector, save the response from GET
	https://api.recipebox.com/v1/users/recipes
3. Wherever you saved it, run `python3 recipe.py {saved_file_name.json} {output_file_name.json}` (with an optional `tags.json` arg for tag mapping)
4. Upload the resulting file to https://recipesage.com/#/settings/import as a JSON-LD file
5. ???

If you use categories/tags on your recipes, they will be imported.
This script deals with duplicates by lowercasing, but if you want to filter out similar ones, you can run:

`recipes.py -t {saved_file_name.json} {tags.json}` and it will print the tags for you, taking into account all deduplicating it would do at runtime.

Then you can edit a `tags.json` file mapping similar tags to one specific tag.  So tidy!