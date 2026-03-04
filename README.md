# CSC394 Final Project Nutrition App

command to import recepies
docker-compose exec web python manage.py import_recipes "data/raw/recipes.csv"

to import dieseases
docker-compose exec web python manage.py import_diseases "data/raw/diseases.csv"

import ingredients 
docker-compose exec web python manage.py import_ingredients "data/raw/ingredients.csv"

import avoid foods
docker-compose exec web python manage.py import_disease_avoid_food "data/raw/disease_avoid_food.csv"

import super foods
docker-compose exec web python manage.py import_disease_super_food "data/raw/disease_super_food.csv"

import recipe ingredients table
docker-compose exec web python manage.py import_recipe_ingredients "data/raw/recipe_ingredients.csv"