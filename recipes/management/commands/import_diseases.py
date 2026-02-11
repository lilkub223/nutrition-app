from django.core.management.base import BaseCommand
import csv
from recipes.models import Disease


class Command(BaseCommand):
    help = "Import diseases from CSV"

    def add_arguments(self, parser):
        parser.add_argument('csvpath')

    def handle(self, *args, **opts):
        path = opts['csvpath']
        count = 0
        with open(path, newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                disease_id = int(row.get('ID', 0))
                if not disease_id:
                    continue
                
                defaults = {
                    'title': row.get('Title', ''),
                    'superfood': row.get('Superfood', ''),
                    'must_avoid': row.get('Must_Avoid', ''),
                    'recommended_activity_level': row.get('Recommended_Activity_Level', ''),
                    'calories_kcal': row.get('Calories_kcal', ''),
                    'saturated_fat_g': row.get('Saturated_Fat_g', ''),
                    'carbs_g': row.get('Carbs_g', ''),
                    'protein_g': row.get('Protein_g', ''),
                    'fiber_g': row.get('Fiber_g', ''),
                    'sugar_g': row.get('Sugar_g', ''),
                    'cholesterol_mg': row.get('Cholesterol_mg', ''),
                    'sodium_mg': row.get('Sodium_mg', ''),
                    'potassium_mg': row.get('Potassium_mg', ''),
                    'iron_mg': row.get('Iron_mg', ''),
                    'calcium_mg': row.get('Calcium_mg', ''),
                    'phosphorus_mg': row.get('Phosphorus_mg', ''),
                    'magnesium_mg': row.get('Magnesium_mg', ''),
                    'vitamin_a_ug': row.get('Vitamin_A_ug', ''),
                    'vitamin_b_mg': row.get('Vitamin_B_mg', ''),
                    'vitamin_c_mg': row.get('Vitamin_C_mg', ''),
                    'vitamin_d_ug': row.get('Vitamin_D_ug', ''),
                    'vitamin_e_mg': row.get('Vitamin_E_mg', ''),
                    'vitamin_k_ug': row.get('Vitamin_K_ug', ''),
                    'zinc_mg': row.get('Zinc_mg', ''),
                    'iodine_ug': row.get('Iodine_ug', ''),
                    'selenium_ug': row.get('Selenium_ug', ''),
                    'copper_mg': row.get('Copper_mg', ''),
                    'fluoride_mg': row.get('Fluoride_mg', ''),
                    'chromium_mg': row.get('Chromium_mg', ''),
                }
                
                Disease.objects.update_or_create(id=disease_id, defaults=defaults)
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} diseases'))