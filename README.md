# CSC394 Final Project Nutrition App

command to import recepies
docker-compose exec web python manage.py import_recipes "recipes.csv"

to import dieseases
docker-compose exec web python manage.py import_diseases "diseases.csv"

to import ingredients(5 parts)
docker-compose exec web python manage.py import_ingredients "food_nutrition_part1.csv"
.
.
.
docker-compose exec web python manage.py import_ingredients "food_nutrition_part5.csv"

