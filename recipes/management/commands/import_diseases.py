from django.core.management.base import BaseCommand
import csv
from recipes.models import Disease
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def to_float(val):
    try:
        return float(val) if val not in (None, '', ' ') else None
    except (ValueError, TypeError):
        return None


class Command(BaseCommand):
    help = "Import diseases from CSV and index to Elasticsearch"

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
                if not es.indices.exists(index='diseases'):
                    es.indices.create(index='diseases', body={
                        'mappings': {
                            'properties': {
                                'id': {'type': 'integer'},
                                'title': {'type': 'text', 'fields': {'keyword': {'type': 'keyword'}}},
                                'superfood': {'type': 'text'},
                                'must_avoid': {'type': 'text'},
                                'recommended_activity_level': {'type': 'keyword'},
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
                                'fluoride_mg': {'type': 'float'},
                                'chromium_mg': {'type': 'float'},
                            }
                        }
                    })
                    self.stdout.write(self.style.SUCCESS('Created diseases index'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Elasticsearch error: {e}. Continuing with DB import only.'))
            es = None

        es_docs = []

        with open(path, newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                disease_id = int(row.get('ID', 0) or 0)
                if not disease_id:
                    continue

                defaults = {
                    'title': row.get('Title', ''),
                    'superfood': row.get('Superfood', ''),
                    'must_avoid': row.get('Must_Avoid', ''),
                    'recommended_activity_level': row.get('Recommended_Activity_Level', ''),

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
                    'fluoride_mg': to_float(row.get('Fluoride_mg')),
                    'chromium_mg': to_float(row.get('Chromium_mg')),
                }

                # Save to database
                Disease.objects.update_or_create(id=disease_id, defaults=defaults)

                # Prepare Elasticsearch document
                if es:
                    es_doc = {'id': disease_id, **defaults}
                    es_docs.append({
                        '_index': 'diseases',
                        '_id': disease_id,
                        '_source': es_doc
                    })

                count += 1

        # Bulk index to Elasticsearch
        if es and es_docs:
            try:
                success, failed = bulk(es, es_docs, stats_only=True)
                self.stdout.write(self.style.SUCCESS(f'Indexed {success} diseases to Elasticsearch'))
                if failed:
                    self.stdout.write(self.style.WARNING(f'{failed} documents failed to index'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Elasticsearch bulk indexing error: {e}'))

        self.stdout.write(self.style.SUCCESS(f"Successfully imported {count} diseases to database"))