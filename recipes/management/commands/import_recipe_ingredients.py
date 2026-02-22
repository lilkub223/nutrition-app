from django.core.management.base import BaseCommand
import csv
from recipes.models import Recipe_Ingredients


class Command(BaseCommand):
    help = "Import recipe_ingredients mapping from CSV"

    def add_arguments(self, parser):
        parser.add_argument("csvpath")

    def handle(self, *args, **opts):
        path = opts["csvpath"]
        count = 0

        with open(path, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)

            for row in reader:
                pk = int(row.get("id", 0) or 0)
                recipe_id = int(row.get("recipe_id", 0) or 0)
                ingredient_id = int(row.get("ingredient_id", 0) or 0)

                if not pk or not recipe_id or not ingredient_id:
                    continue

                Recipe_Ingredients.objects.update_or_create(
                    recipe_ingredient_id=pk,
                    defaults={
                        "recipe_id_id": recipe_id,
                        "ingredient_id_id": ingredient_id,
                    }
                )

                count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported {count} recipe_ingredient rows")
        )