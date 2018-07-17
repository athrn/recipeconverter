# Recipe Converter
Convert all units in a recipe from US to metric or vice versa.

It is a working prototype with a limited command line interface. It has not been tested much yet.

## Features

* Handles some fractions, both as ascii or unicode characters and in plain text, i.e. 1 1/4 cups or 3¾.
* Automatically selects the "closest" unit in conversions. Currently, this is rather primitive.

## Example
The recipe with US units (http://www.foodista.com/recipe/WGMZ84YQ/peanut-butter-cookie-recipe):

````
Ingredients
4 cups Almond Flour
1 tsp baking soda
3/4 tsp fine grain sea salt
1 egg, beaten
1 1/3 cup Chunky All Natural Peanut Butter - with salt
1/2 cup Maple Syrup
Orange Vanilla Sugar

Preparation
1 Preheat Oven to 350 f.
2 Mix the first 3, dry, ingredients.
3 Fold in the beaten egg, peanut butter and maple syrup.
4 Roll dough into balls. F
5 latten with a cup dipped in Orange Vanilla Sugar and then mark with a fork dipped in the same sugar.
6 Bake for 10-12 minutes depending on how browned you like them.
````

is converted to "European" units as

````
Ingredients
9.5 dl Almond Flour
1.0 tsp baking soda
0.7 tsp fine grain sea salt
1 egg, beaten
3.2 dl Chunky All Natural Peanut Butter - with salt
1.2 dl Maple Syrup
Orange Vanilla Sugar

Preparation
1 Preheat Oven to 176.7 C.
2 Mix the first 3, dry, ingredients.
3 Fold in the beaten egg, peanut butter and maple syrup.
4 Roll dough into balls. F
5 latten with a cup dipped in Orange Vanilla Sugar and then mark with a fork dipped in the same sugar.
6 Bake for 10-12 minutes depending on how browned you like them.
````


## To Do:

* Test a lot more.
    * Round trip testing with real recipes.
* UK/Imperial units.
* Improve closest-unit function. Make it round trip safe 1 cup -> 2.4 dl -> 1 cup.
    * Preferred units. dl > cl.
    * Sometimes integer units should be preferred over fractions. 4 tbsp is better than 0.6 dl.
* Command line configuration. Units to include or exclude.


