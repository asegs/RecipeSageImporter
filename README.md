### So your phone is running a bit hot?

#### Steps to import to RecipeSage

1. Run `python3 recipe.py {output_file_name.json}` (with an optional `tags.json` arg for tag mapping)*
2. Upload the resulting file to https://recipesage.com/#/settings/import as a JSON-LD file
3. ???

*When you run the script, you will be prompted for username and password.  This is just used to authenticate with RecipeBox since they don't expose any auth/public API.

If you use categories/tags on your recipes, they will be imported.
This script deals with duplicates by lowercasing, but if you want to filter out similar ones, you can run:

`recipes.py -t {tags.json}` and it will print the tags for you, taking into account all deduplicating it would do at runtime.

Then you can edit a `tags.json` file mapping similar tags to one specific tag.  So tidy!