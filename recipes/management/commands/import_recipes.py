from django.core.management.base import BaseCommand
import csv
from recipes.models import Recipe
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def to_float(val):
    """Convert string to float, return None if empty or invalid."""
    try:
        return float(val) if val not in (None, '', ' ') else None
    except (ValueError, TypeError):
        return None


class Command(BaseCommand):
    help = "Import recipes from CSV and index to Elasticsearch"

    def add_arguments(self, parser):
        parser.add_argument('csvpath')

    def handle(self, *args, **opts):
        path = opts['csvpath']
        es_host = 'http://elasticsearch:9200'
        count = 0

        # Connect to Elasticsearch
        try:
            es = Elasticsearch([es_host], request_timeout=5)
            if not es.ping():
                self.stdout.write(self.style.WARNING('Elasticsearch not reachable, skipping indexing'))
                es = None
            else:
                # Create index with mapping if it doesn't exist
                if not es.indices.exists(index='recipes'):
                    es.indices.create(index='recipes', body={
                        'mappings': {
                            'properties': {
                                'id': {'type': 'integer'},
                                'title': {'type': 'text', 'fields': {'keyword': {'type': 'keyword'}}},
                                'meal_type': {'type': 'keyword'},
                                'measurement': {'type': 'text'},
                                'ingredients': {'type': 'text'},
                                'substitutions': {'type': 'text'},
                                'how_to_cook': {'type': 'text'},
                                'calories_kcal': {'type': 'float'},
                                'saturated_fat_g': {'type': 'float'},
                                'carbs_g': {'type': 'float'},
                                'protein_g': {'type': 'float'},
                                'fiber_g': {'type': 'float'},
                                'sugar_g': {'type': 'float'},
                                'cholesterol_mg': {'type': 'float'},
                                'sodium_mg': {'type': 'float'},
                                'potassium_mg': {'type': 'float'},
                                'iron_mg': {'type': 'float'},
                                'calcium_mg': {'type': 'float'},
                                'phosphorus_mg': {'type': 'float'},
                                'magnesium_mg': {'type': 'float'},
                                'vitamin_a_ug': {'type': 'float'},
                                'vitamin_b_mg': {'type': 'float'},
                                'vitamin_c_mg': {'type': 'float'},
                                'vitamin_d_ug': {'type': 'float'},
                                'vitamin_e_mg': {'type': 'float'},
                                'vitamin_k_ug': {'type': 'float'},
                                'zinc_mg': {'type': 'float'},
                                'iodine_ug': {'type': 'float'},
                                'selenium_ug': {'type': 'float'},
                                'copper_mg': {'type': 'float'},
                                'magnesium_2_mg': {'type': 'float'},
                                'fluoride_mg': {'type': 'float'},
                                'chromium_mg': {'type': 'float'},
                                'dietary_restrictions': {'type': 'keyword'},
                            }
                        }
                    })
                    self.stdout.write(self.style.SUCCESS('Created recipes index'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Elasticsearch error: {e}. Continuing with DB import only.'))
            es = None

        es_docs = []

        with open(path, newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                recipe_id = int(row.get('ID', 0))
                if not recipe_id:
                    continue
                
                # The CSV has an empty column after Title that contains meal_type
                meal_type = (
                    row.get('Meal_Time')
                    or row.get('Meal Type')
                    or row.get('')
                    or ''
                )
                
                defaults = {
                    'title': row.get('Title', ''),
                    'meal_type': meal_type,
                    'measurement': row.get('Measurement', ''),
                    'ingredients': row.get('Ingredients', ''),
                    'substitutions': row.get('Substitutions', ''),
                    'how_to_cook': row.get('How_To_Cook', ''),
                    'calories_kcal': to_float(row.get('Calories_kcal')),
                    'saturated_fat_g': to_float(row.get('Saturated_Fat_g')),
                    'carbs_g': to_float(row.get('Carbs_g')),
                    'protein_g': to_float(row.get('Protein_g')),
                    'fiber_g': to_float(row.get('Fiber_g')),
                    'sugar_g': to_float(row.get('Sugar_g')),
                    'cholesterol_mg': to_float(row.get('Cholesterol_mg')),
                    'sodium_mg': to_float(row.get('Sodium_mg')),
                    'potassium_mg': to_float(row.get('Potassium_mg')),
                    'iron_mg': to_float(row.get('Iron_mg')),
                    'calcium_mg': to_float(row.get('Calcium_mg')),
                    'phosphorus_mg': to_float(row.get('Phosphorus_mg')),
                    'magnesium_mg': to_float(row.get('Magnesium_mg')),
                    'vitamin_a_ug': to_float(row.get('Vitamin_A_ug')),
                    'vitamin_b_mg': to_float(row.get('Vitamin_B_mg')),
                    'vitamin_c_mg': to_float(row.get('Vitamin_C_mg')),
                    'vitamin_d_ug': to_float(row.get('Vitamin_D_ug')),
                    'vitamin_e_mg': to_float(row.get('Vitamin_E_mg')),
                    'vitamin_k_ug': to_float(row.get('Vitamin_K_ug')),
                    'zinc_mg': to_float(row.get('Zinc_mg')),
                    'iodine_ug': to_float(row.get('Iodine_ug')),
                    'selenium_ug': to_float(row.get('Selenium_ug')),
                    'copper_mg': to_float(row.get('Copper_mg')),
                    'magnesium_2_mg': to_float(row.get('Magnesium_mg')),
                    'fluoride_mg': to_float(row.get('Fluoride_mg')),
                    'chromium_mg': to_float(row.get('Chromium_mg')),
                    'dietary_restrictions': row.get('Dietary_Restrictions', ''),
                }
                
                # Save to database
                Recipe.objects.update_or_create(id=recipe_id, defaults=defaults)

                # Prepare Elasticsearch document
                if es:
                    es_doc = {'id': recipe_id, **defaults}
                    es_docs.append({
                        '_index': 'recipes',
                        '_id': recipe_id,
                        '_source': es_doc
                    })
                
                count += 1

        # Bulk index to Elasticsearch
        if es and es_docs:
            try:
                success, failed = bulk(es, es_docs, stats_only=True)
                self.stdout.write(self.style.SUCCESS(f'Indexed {success} recipes to Elasticsearch'))
                if failed:
                    self.stdout.write(self.style.WARNING(f'{failed} documents failed to index'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Elasticsearch bulk indexing error: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} recipes to database'))