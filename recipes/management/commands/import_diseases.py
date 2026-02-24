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
                                'Diease_Super_Food': {'type': 'text'},
                                'Disease_Avoid_Food': {'type': 'text'},
                                #'recommended_activity_level': {'type': 'keyword'},
                                'low_calories_kcal': {'type': 'float'},
                                'low_saturated_fat_g': {'type': 'float'},
                                'low_carbs_g': {'type': 'float'},
                                'low_protein_g': {'type': 'float'},
                                'low_fiber_g': {'type': 'float'},
                                'low_sugar_g': {'type': 'float'},
                                'low_cholesterol_mg': {'type': 'float'},
                                'low_sodium_mg': {'type': 'float'},
                                'low_potassium_mg': {'type': 'float'},
                                'low_iron_mg': {'type': 'float'},
                                'low_calcium_mg': {'type': 'float'},
                                'low_phosphorus_mg': {'type': 'float'},
                                'low_magnesium_mg': {'type': 'float'},
                                'low_vitamin_a_ug': {'type': 'float'},
                                'low_vitamin_b_mg': {'type': 'float'},
                                'low_vitamin_c_mg': {'type': 'float'},
                                'low_vitamin_d_ug': {'type': 'float'},
                                'low_vitamin_e_mg': {'type': 'float'},
                                'low_vitamin_k_ug': {'type': 'float'},
                                'low_zinc_mg': {'type': 'float'},
                                'low_iodine_ug': {'type': 'float'},
                                'low_selenium_ug': {'type': 'float'},
                                'low_copper_mg': {'type': 'float'},
                                'low_fluoride_mg': {'type': 'float'},
                                'low_chromium_mg': {'type': 'float'},

                                'high_calories_kcal': {'type': 'float'},
                                'high_saturated_fat_g': {'type': 'float'},
                                'high_carbs_g': {'type': 'float'},
                                'high_protein_g': {'type': 'float'},
                                'high_fiber_g': {'type': 'float'},
                                'high_sugar_g': {'type': 'float'},
                                'high_cholesterol_mg': {'type': 'float'},
                                'high_sodium_mg': {'type': 'float'},
                                'high_potassium_mg': {'type': 'float'},
                                'high_iron_mg': {'type': 'float'},
                                'high_calcium_mg': {'type': 'float'},
                                'high_phosphorus_mg': {'type': 'float'},
                                'high_magnesium_mg': {'type': 'float'},
                                'high_vitamin_a_ug': {'type': 'float'},
                                'high_vitamin_b_mg': {'type': 'float'},
                                'high_vitamin_c_mg': {'type': 'float'},
                                'high_vitamin_d_ug': {'type': 'float'},
                                'high_vitamin_e_mg': {'type': 'float'},
                                'high_vitamin_k_ug': {'type': 'float'},
                                'high_zinc_mg': {'type': 'float'},
                                'high_iodine_ug': {'type': 'float'},
                                'high_selenium_ug': {'type': 'float'},
                                'high_copper_mg': {'type': 'float'},
                                'high_fluoride_mg': {'type': 'float'},
                                'high_chromium_mg': {'type': 'float'},
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
                    'Disease_Super_Food': row.get('Disease_Super_food', ''),
                    'Disease_Avoid_Food': row.get('Disease_Avoid_Food', ''),
                    #'recommended_activity_level': row.get('Recommended_Activity_Level', ''),

                    # Low stats for nutrients
                    'low_calories_kcal': to_float(row.get('low_calories_kcal')),
                    'low_saturated_fat_g': to_float(row.get('low_saturated_Fat_g')),
                    'low_carbs_g': to_float(row.get('low_carbs_g')),
                    'low_protein_g': to_float(row.get('low_protein_g')),
                    'low_fiber_g': to_float(row.get('low_fiber_g')),
                    'low_sugar_g': to_float(row.get('low_sugar_g')),
                    'low_cholesterol_mg': to_float(row.get('low_cholesterol_mg')),
                    'low_sodium_mg': to_float(row.get('low_sodium_mg')),
                    'low_potassium_mg': to_float(row.get('low_potassium_mg')),
                    'low_iron_mg': to_float(row.get('low_iron_mg')),
                    'low_calcium_mg': to_float(row.get('low_calcium_mg')),
                    'low_phosphorus_mg': to_float(row.get('low_phosphorus_mg')),
                    'low_magnesium_mg': to_float(row.get('low_magnesium_mg')),

                    'low_vitamin_a_ug': to_float(row.get('low_vitamin_A_ug')),
                    'low_vitamin_b_mg': to_float(row.get('low_vitamin_B_mg')),
                    'low_vitamin_c_mg': to_float(row.get('low_vitamin_C_mg')),
                    'low_vitamin_d_ug': to_float(row.get('low_vitamin_D_ug')),
                    'low_vitamin_e_mg': to_float(row.get('low_vitamin_E_mg')),
                    'low_vitamin_k_ug': to_float(row.get('low_vitamin_K_ug')),

                    'low_zinc_mg': to_float(row.get('low_zinc_mg')),
                    'low_iodine_ug': to_float(row.get('low_iodine_ug')),
                    'low_selenium_ug': to_float(row.get('low_selenium_ug')),
                    'low_copper_mg': to_float(row.get('low_copper_mg')),
                    'low_fluoride_mg': to_float(row.get('low_fluoride_mg')),
                    'low_chromium_mg': to_float(row.get('low_chromium_mg')),

                    # High stats for nutrients
                    'high_calories_kcal': to_float(row.get('high_calories_kcal')),
                    'high_saturated_fat_g': to_float(row.get('high_saturated_Fat_g')),
                    'high_carbs_g': to_float(row.get('high_carbs_g')),
                    'high_protein_g': to_float(row.get('high_protein_g')),
                    'high_fiber_g': to_float(row.get('high_fiber_g')),
                    'high_sugar_g': to_float(row.get('high_sugar_g')),
                    'high_cholesterol_mg': to_float(row.get('high_cholesterol_mg')),
                    'high_sodium_mg': to_float(row.get('high_sodium_mg')),
                    'high_potassium_mg': to_float(row.get('high_potassium_mg')),
                    'high_iron_mg': to_float(row.get('high_iron_mg')),
                    'high_calcium_mg': to_float(row.get('high_calcium_mg')),
                    'high_phosphorus_mg': to_float(row.get('high_phosphorus_mg')),
                    'high_magnesium_mg': to_float(row.get('high_magnesium_mg')),

                    'high_vitamin_a_ug': to_float(row.get('high_vitamin_A_ug')),
                    'high_vitamin_b_mg': to_float(row.get('high_vitamin_B_mg')),
                    'high_vitamin_c_mg': to_float(row.get('high_vitamin_C_mg')),
                    'high_vitamin_d_ug': to_float(row.get('high_vitamin_D_ug')),
                    'high_vitamin_e_mg': to_float(row.get('high_vitamin_E_mg')),
                    'high_vitamin_k_ug': to_float(row.get('high_vitamin_K_ug')),

                    'high_zinc_mg': to_float(row.get('high_zinc_mg')),
                    'high_iodine_ug': to_float(row.get('high_iodine_ug')),
                    'high_selenium_ug': to_float(row.get('high_selenium_ug')),
                    'high_copper_mg': to_float(row.get('high_copper_ug')),
                    'high_fluoride_mg': to_float(row.get('high_fluoride_mg')),
                    'high_chromium_mg': to_float(row.get('high_chromium_mg')),
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