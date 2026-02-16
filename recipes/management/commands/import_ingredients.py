# import_ingredients.py - simplified for Docker
from django.core.management.base import BaseCommand
import csv
from recipes.models import Ingredient
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def to_float(val):
    """Convert string to float, return None if empty or invalid."""
    try:
        return float(val) if val not in (None, '', ' ') else None
    except (ValueError, TypeError):
        return None


class Command(BaseCommand):
    help = "Import ingredients from CSV and index to Elasticsearch"

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
                if not es.indices.exists(index='ingredients'):
                    es.indices.create(index='ingredients', body={
                        'mappings': {
                            'properties': {
                                'id': {'type': 'integer'},
                                'food': {'type': 'text', 'fields': {'keyword': {'type': 'keyword'}}},
                                'caloric_value': {'type': 'float'},
                                'fat': {'type': 'float'},
                                'saturated_fats': {'type': 'float'},
                                'monounsaturated_fats': {'type': 'float'},
                                'polyunsaturated_fats': {'type': 'float'},
                                'carbohydrates': {'type': 'float'},
                                'sugars': {'type': 'float'},
                                'protein': {'type': 'float'},
                                'dietary_fiber': {'type': 'float'},
                                'cholesterol': {'type': 'float'},
                                'sodium': {'type': 'float'},
                                'water': {'type': 'float'},
                                'vitamin_a': {'type': 'float'},
                                'vitamin_b1': {'type': 'float'},
                                'vitamin_b11': {'type': 'float'},
                                'vitamin_b12': {'type': 'float'},
                                'vitamin_b2': {'type': 'float'},
                                'vitamin_b3': {'type': 'float'},
                                'vitamin_b5': {'type': 'float'},
                                'vitamin_b6': {'type': 'float'},
                                'vitamin_c': {'type': 'float'},
                                'vitamin_d': {'type': 'float'},
                                'vitamin_e': {'type': 'float'},
                                'vitamin_k': {'type': 'float'},
                                'calcium': {'type': 'float'},
                                'copper': {'type': 'float'},
                                'iron': {'type': 'float'},
                                'magnesium': {'type': 'float'},
                                'manganese': {'type': 'float'},
                                'phosphorus': {'type': 'float'},
                                'potassium': {'type': 'float'},
                                'selenium': {'type': 'float'},
                                'zinc': {'type': 'float'},
                                'nutrition_density': {'type': 'float'},
                            }
                        }
                    })
                    self.stdout.write(self.style.SUCCESS('Created ingredients index'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Elasticsearch error: {e}. Continuing with DB import only.'))
            es = None

        es_docs = []
        
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
                
                # Save to database
                Ingredient.objects.update_or_create(id=ingredient_id, defaults=defaults)
                
                # Prepare Elasticsearch document
                if es:
                    es_doc = {'id': ingredient_id, **defaults}
                    es_docs.append({
                        '_index': 'ingredients',
                        '_id': ingredient_id,
                        '_source': es_doc
                    })
                
                count += 1
        
        # Bulk index to Elasticsearch
        if es and es_docs:
            try:
                success, failed = bulk(es, es_docs, stats_only=True)
                self.stdout.write(self.style.SUCCESS(f'Indexed {success} ingredients to Elasticsearch'))
                if failed:
                    self.stdout.write(self.style.WARNING(f'{failed} documents failed to index'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Elasticsearch bulk indexing error: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} ingredients to database'))