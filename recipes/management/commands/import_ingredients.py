from django.core.management.base import BaseCommand
import csv
from recipes.models import Ingredient


def to_float(val):
    """Convert string to float, return None if empty or invalid."""
    try:
        return float(val) if val not in (None, '', ' ') else None
    except (ValueError, TypeError):
        return None


class Command(BaseCommand):
    help = "Import ingredients from CSV"

    def add_arguments(self, parser):
        parser.add_argument('csvpath')

    def handle(self, *args, **opts):
        path = opts['csvpath']
        count = 0
        with open(path, newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                food_name = row.get('food', '')
                if not food_name:
                    continue
                
                ingredient_id = count + 1
                
                defaults = {
                    'food': food_name,
                    'caloric_value': to_float(row.get('Caloric Value')),
                    'fat': to_float(row.get('Fat')),
                    'saturated_fats': to_float(row.get('Saturated Fats')),
                    'monounsaturated_fats': to_float(row.get('Monounsaturated Fats')),
                    'polyunsaturated_fats': to_float(row.get('Polyunsaturated Fats')),
                    'carbohydrates': to_float(row.get('Carbohydrates')),
                    'sugars': to_float(row.get('Sugars')),
                    'protein': to_float(row.get('Protein')),
                    'dietary_fiber': to_float(row.get('Dietary Fiber')),
                    'cholesterol': to_float(row.get('Cholesterol')),
                    'sodium': to_float(row.get('Sodium')),
                    'water': to_float(row.get('Water')),
                    'vitamin_a': to_float(row.get('Vitamin A')),
                    'vitamin_b1': to_float(row.get('Vitamin B1')),
                    'vitamin_b11': to_float(row.get('Vitamin B11')),
                    'vitamin_b12': to_float(row.get('Vitamin B12')),
                    'vitamin_b2': to_float(row.get('Vitamin B2')),
                    'vitamin_b3': to_float(row.get('Vitamin B3')),
                    'vitamin_b5': to_float(row.get('Vitamin B5')),
                    'vitamin_b6': to_float(row.get('Vitamin B6')),
                    'vitamin_c': to_float(row.get('Vitamin C')),
                    'vitamin_d': to_float(row.get('Vitamin D')),
                    'vitamin_e': to_float(row.get('Vitamin E')),
                    'vitamin_k': to_float(row.get('Vitamin K')),
                    'calcium': to_float(row.get('Calcium')),
                    'copper': to_float(row.get('Copper')),
                    'iron': to_float(row.get('Iron')),
                    'magnesium': to_float(row.get('Magnesium')),
                    'manganese': to_float(row.get('Manganese')),
                    'phosphorus': to_float(row.get('Phosphorus')),
                    'potassium': to_float(row.get('Potassium')),
                    'selenium': to_float(row.get('Selenium')),
                    'zinc': to_float(row.get('Zinc')),
                    'nutrition_density': to_float(row.get('Nutrition Density')),
                }
                
                Ingredient.objects.update_or_create(id=ingredient_id, defaults=defaults)
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} ingredients'))