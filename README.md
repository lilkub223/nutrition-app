# CSC394 Final Project Nutrition App

command to import recepies
docker-compose exec web python manage.py import_recipes "data/raw/recipes.csv"

to import dieseases
docker-compose exec web python manage.py import_diseases "data/raw/diseases.csv"

to import ingredients(5 parts)
docker-compose exec web python manage.py import_ingredients "data/raw/food_nutrition_part1.csv".

.
.
docker-compose exec web python manage.py import_ingredients "food_nutrition_part5.csv"

