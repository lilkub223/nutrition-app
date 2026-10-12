# Nutrition App | CSC 394 Team Project

A nutrition planning application built with Django, PostgreSQL, and Docker for
DePaul University's CSC 394 course. Features include recipe browsing, dietary
restrictions, disease-related food information, nutrition and weight goals,
meal and workout logs, grocery lists, and daily and weekly summaries.

## Project Origin and Team Credit

This is Kaamil Khan's public portfolio copy of a collaborative class project,
published with the team's permission. The application was developed by the team;
this repository does not represent solo authorship.

Original repository: [DePaul-CSC-394-801-2026/nutrition-app-team-3](https://github.com/DePaul-CSC-394-801-2026/nutrition-app-team-3)
(private; access is required).

Contributors, based on the original repository's commit history:

- [rspocins](https://github.com/rspocins)
- [Rheema Ayyash](https://github.com/rheema-ayyash)
- [Kaamil Khan](https://github.com/lilkub223)
- [Riley Oleson](https://github.com/roleson31)
- [dhrutikamin](https://github.com/dhrutikamin)
- [Mikolaj Kubowicz](https://github.com/MikolajKubowicz)

The original main branch's commit authors, messages, and contribution history are
retained. Before publication, embedded credentials, cached Python bytecode, and
a historical local database were removed from this copy's history. As a result,
commit IDs differ from those in the original repository.

## My Contributions: Kaamil Khan

Based on the original commits, my work included:

- Building the goals page with nutrition targets, weight tracking, and custom goals.
- Improving goal completion behavior, weight goal saving, and multiple-disease selection.
- Updating the database schema, models, migrations, and CSV import commands.
- Adding dietary restriction and quote data, models, and import support.
- Expanding disease and food datasets and correcting ingredient references and CSV headers.

## Local Development

This repository contains a class project and local development configuration.
It is not a production deployment or a source of medical advice.

With Docker and Docker Compose installed:

```sh
docker compose up --build -d
docker compose exec web python manage.py migrate
```

Once PostgreSQL is ready and migrations complete, open http://localhost:8000.
The commands below import the project's sample datasets.

Email uses Django's console backend by default. SMTP credentials must be supplied
through environment variables when explicitly enabling SMTP. A development
secret key is generated at startup unless `DJANGO_SECRET_KEY` is set; set a
stable private value in the application environment for persistent sessions.
Never reuse credentials from the original private repository.

No new software license is granted by this portfolio copy. The original
repository did not include a license; contributor and third-party rights remain
with their respective holders.

## Original Development Notes

The team's original import commands and sample-data notes are retained below.

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


docker-compose exec web python manage.py import_recipes "data/raw/recipes.csv"
docker-compose exec web python manage.py import_diseases "data/raw/diseases.csv"
docker-compose exec web python manage.py import_ingredients "data/raw/ingredients.csv"
docker-compose exec web python manage.py import_recipe_ingredients "data/raw/recipe_ingredients.csv"
docker-compose exec web python manage.py import_disease_avoid_food "data/raw/disease_avoid_food.csv"
docker-compose exec web python manage.py import_disease_super_food "data/raw/disease_super_food.csv"

from django.contrib.auth.models import User
from recipes.models import DailyLog, MealEntry, WorkoutEntry
from datetime import date, timedelta
import random

user = User.objects.first()  # change this to target a specific user

for i in range(7):
    log_date = date.today() - timedelta(days=i)
    calories = round(random.uniform(1500, 2500), 1)
    protein = round(random.uniform(50, 150), 1)
    carbs = round(random.uniform(150, 350), 1)
    fats = round(random.uniform(40, 100), 1)
    burned = round(random.uniform(0, 500), 1)
    log, created = DailyLog.objects.get_or_create(
        user=user,
        date=log_date,
        defaults={
            'total_calories': calories,
            'total_protein': protein,
            'total_carbs': carbs,
            'total_fats': fats,
            'total_burned': burned,
            'calorie_goal': 2000,
        }
    )
    if created:
        MealEntry.objects.create(
            daily_log=log,
            meal_name=f'Sample Meal',
            calories=calories,
            protein=protein,
            carbs=carbs,
            fats=fats,
        )
        WorkoutEntry.objects.create(
            daily_log=log,
            workout_type=random.choice(['cardio', 'strength', 'walking', 'running']),
            calories_burned=burned,
        )
        print(f'Created log for {log_date}')
    else:
        print(f'Log already exists for {log_date}, skipping.')


from django.contrib.auth.models import User
from recipes.models import DailyLog, MealEntry, WorkoutEntry
from datetime import date, timedelta
import random
user = User.objects.first()  # change to target a specific user
workout_counts = random.sample(range(1, 11), 7)
for i in range(7):
    log_date = date.today() - timedelta(days=i)
    calories = round(random.uniform(1500, 2500), 1)
    protein = round(random.uniform(50, 150), 1)
    carbs = round(random.uniform(150, 350), 1)
    fats = round(random.uniform(40, 100), 1)
    burned = round(random.uniform(0, 500), 1)
    log, created = DailyLog.objects.update_or_create(
        user=user,
        date=log_date,
        defaults={
            'total_calories': calories,
            'total_protein': protein,
            'total_carbs': carbs,
            'total_fats': fats,
            'total_burned': burned,
            'calorie_goal': 2000,
        }
    )
    MealEntry.objects.filter(daily_log=log).delete()
    WorkoutEntry.objects.filter(daily_log=log).delete()
    MealEntry.objects.create(
        daily_log=log,
        meal_name=f'Sample Meal',
        calories=calories,
        protein=protein,
        carbs=carbs,
        fats=fats,
    )
    num_workouts = workout_counts[i]
    for _ in range(num_workouts):
        WorkoutEntry.objects.create(
            daily_log=log,
            workout_type=random.choice(['cardio', 'strength', 'walking', 'running']),
            calories_burned=round(random.uniform(100, 500), 1),
        )
    print(f'{"Created" if created else "Updated"} log for {log_date} with {num_workouts} workouts')
