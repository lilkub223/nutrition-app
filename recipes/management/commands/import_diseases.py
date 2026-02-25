from django.core.management.base import BaseCommand
import csv
from recipes.models import Disease


def to_float(val):
    try:
        return float(val) if val not in (None, '', ' ') else None
    except (ValueError, TypeError):
        return None
    
def get_min(row, key):
    return to_float(row.get(f"{key}_min"))

def get_max(row, key):
    return to_float(row.get(f"{key}_max"))


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

                    "low_low_vitamin_a_ug": get_min(row, "Vitamin_A_ug"),
                    "high_vitamin_a_ug": get_max(row, "low_vitamin_A_ug"),

                    "low_low_vitamin_b_mg": get_min(row, "Vitamin_B_mg"),
                    "high_vitamin_b_mg": get_max(row, "Vitamin_B_mg"),

                    "low_vitamin_c_mg": get_min(row, "low_vitamin_C_mg"),
                    "high_low_vitamin_c_mg": to_float(row.get("low_vitamin_C_max")),

                    "low_low_vitamin_d_ug": get_min(row, "Vitamin_D_ug"),
                    "high_vitamin_d_ug": get_max(row, "low_vitamin_D_ug"),

                    "low_low_vitamin_e_mg": get_min(row, "Vitamin_E_mg"),
                    "high_vitamin_e_mg": get_max(row, "low_vitamin_E_mg"),  
                    "low_low_vitamin_k_ug": get_min(row, "Vitamin_K_ug"),
                    "high_vitamin_k_ug": get_max(row, "low_vitamin_K_ug"),

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
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully imported {count} diseases"))

