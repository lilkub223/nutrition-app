# Nutrition App

A nutrition planning web app for people managing chronic diseases. Users can explore recipes, identify foods associated with their conditions, and track meals, nutrition targets, and weight goals in one place.

Built with Django and PostgreSQL as a team project for DePaul University's CSC 394 course.

## Features

- **Disease-based nutrition:** Select health conditions, explore related food information, and view nutrition target ranges based on selected diseases.
- **Recipe discovery:** Browse and search recipes, adjust serving sizes, and save meals with ingredient and nutrition details.
- **Personal profiles:** Manage dietary restrictions, selected conditions, and weight information.
- **Goals and progress:** Set calorie and macronutrient targets, track weight, and manage custom goals.
- **Daily and weekly summaries:** Log meals and workouts and review nutrition totals over time.
- **Grocery lists:** Build a grocery list from saved recipes.

## Tech Stack

| Layer | Technologies |
| --- | --- |
| Backend | Python, Django |
| Frontend | Django templates, HTML, CSS, JavaScript |
| Database | PostgreSQL |
| Development | Docker, Docker Compose |
| Data loading | CSV datasets and Django management commands |

## Getting Started

### Prerequisites

- Git
- Docker with Docker Compose
- Available ports `8000`, `5432`, `9200`, and `9300`

### 1. Clone the repository

```sh
git clone https://github.com/lilkub223/nutrition-app.git
cd nutrition-app
```

### 2. Start the application

```sh
docker compose up --build -d
```

The Compose stack includes the Django app, PostgreSQL, and an Elasticsearch service. Wait for PostgreSQL to be ready before running migrations. You can check its status with `docker compose logs db`.

```sh
docker compose exec web python manage.py migrate
```

### 3. Load the datasets

Run these commands in order so recipes, ingredients, diseases, and dietary restrictions exist before their relationships are imported:

```sh
docker compose exec web python manage.py import_recipes data/raw/recipes.csv
docker compose exec web python manage.py import_ingredients data/raw/ingredients.csv
docker compose exec web python manage.py import_diseases data/raw/diseases.csv
docker compose exec web python manage.py import_dietary_restrictions
docker compose exec web python manage.py import_recipe_ingredients data/raw/recipe_ingredients.csv
docker compose exec web python manage.py import_disease_avoid_food data/raw/disease_avoid_food.csv
docker compose exec web python manage.py import_disease_super_food data/raw/disease_super_food.csv
docker compose exec web python manage.py import_dietary_restriction_ingredients
docker compose exec web python manage.py import_dietary_restriction_recipes
docker compose exec web python manage.py import_quotes
```

### 4. Open the app

Visit [localhost:8000](http://localhost:8000), create an account, and set up your profile to start exploring recipes and tracking goals.

To stop the application while keeping the database volume:

```sh
docker compose down
```

### Configuration

For a consistent local secret key across restarts, set `DJANGO_SECRET_KEY` in a root `.env` file before starting the app. Otherwise, a temporary key is generated at startup.

Email messages print to the application logs by default. To enable the configured Gmail SMTP service, set `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`, `EMAIL_HOST_USER`, and `EMAIL_HOST_PASSWORD` in `.env`.

## Project Structure

```text
nutrition_project/           Django settings and URL routing
recipes/                     Models, views, migrations, and app templates
recipes/management/commands/ CSV import commands
main/                        Shared templates, styles, and images
data/raw/                    Recipe, ingredient, disease, and dietary datasets
docker-compose.yml           Local services and configuration
```

## My Contributions

**Kaamil Khan**

- Built the goals page with nutrition targets, weight tracking, and custom goals.
- Added support for multiple selected diseases and improved goal completion and weight tracking behavior.
- Updated database models, migrations, and CSV import commands for the nutrition schema.
- Added dietary restriction and quote models, datasets, and import support.
- Expanded disease and food datasets and fixed CSV headers and ingredient references.

## Team

- [Kaamil Khan](https://github.com/lilkub223)
- [Rheema Ayyash](https://github.com/rheema-ayyash)
- [Riley Oleson](https://github.com/roleson31)
- [Mikolaj Kubowicz](https://github.com/MikolajKubowicz)
- [rspocins](https://github.com/rspocins)
- [dhrutikamin](https://github.com/dhrutikamin)

Developed for CSC 394 at DePaul University. [Original team repository](https://github.com/DePaul-CSC-394-801-2026/nutrition-app-team-3).
