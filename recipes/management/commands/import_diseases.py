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
                    "title": row.get("Name", "").strip(),

                    "low_calories_kcal": get_min(row, "Calories_kcal"),
                    "high_calories_kcal": get_max(row, "Calories_kcal"),

                    "low_saturated_fat_g": get_min(row, "Saturated_Fat_g"),
                    "high_saturated_fat_g": get_max(row, "Saturated_Fat_g"),

                    "low_carbs_g": get_min(row, "Carbs_g"),
                    "high_carbs_g": get_max(row, "Carbs_g"),

                    "low_protein_g": get_min(row, "Protein_g"),
                    "high_protein_g": get_max(row, "Protein_g"),

                    "low_fiber_g": get_min(row, "Fiber_g"),
                    "high_fiber_g": get_max(row, "Fiber_g"),

                    "low_sugar_g": get_min(row, "Sugar_g"),
                    "high_sugar_g": get_max(row, "Sugar_g"),

                    "low_cholesterol_mg": get_min(row, "Cholesterol_mg"),
                    "high_cholesterol_mg": get_max(row, "Cholesterol_mg"),

                    "low_sodium_mg": get_min(row, "Sodium_mg"),
                    "high_sodium_mg": get_max(row, "Sodium_mg"),

                    "low_potassium_mg": get_min(row, "Potassium_mg"),
                    "high_potassium_mg": get_max(row, "Potassium_mg"),

                    "low_iron_mg": get_min(row, "Iron_mg"),
                    "high_iron_mg": get_max(row, "Iron_mg"),

                    "low_calcium_mg": get_min(row, "Calcium_mg"),
                    "high_calcium_mg": get_max(row, "Calcium_mg"),

                    "low_phosphorus_mg": get_min(row, "Phosphorus_mg"),
                    "high_phosphorus_mg": get_max(row, "Phosphorus_mg"),
                    "low_magnesium_mg": get_min(row, "Magnesium_mg"),
                    "high_magnesium_mg": get_max(row, "Magnesium_mg"),

                    "low_vitamin_a_ug": get_min(row, "Vitamin_A_ug"),
                    "high_vitamin_a_ug": get_max(row, "Vitamin_A_ug"),

                    "low_vitamin_b_mg": get_min(row, "Vitamin_B_mg"),
                    "high_vitamin_b_mg": get_max(row, "Vitamin_B_mg"),

                    "low_vitamin_c_mg": get_min(row, "Vitamin_C_mg"),
                    "high_vitamin_c_mg": to_float(row.get("Vitamin_C_max")),

                    "low_vitamin_d_ug": get_min(row, "Vitamin_D_ug"),
                    "high_vitamin_d_ug": get_max(row, "Vitamin_D_ug"),

                    "low_vitamin_e_mg": get_min(row, "Vitamin_E_mg"),
                    "high_vitamin_e_mg": get_max(row, "Vitamin_E_mg"),  
                    "low_vitamin_k_ug": get_min(row, "Vitamin_K_ug"),
                    "high_vitamin_k_ug": get_max(row, "Vitamin_K_ug"),

                    "low_zinc_mg": get_min(row, "Zinc_mg"),
                    "high_zinc_mg": get_max(row, "Zinc_mg"),

                    "low_iodine_ug": get_min(row, "Iodine_ug"),
                    "high_iodine_ug": get_max(row, "Iodine_ug"),
                    "low_selenium_ug": get_min(row, "Selenium_ug"),
                    "high_selenium_ug": get_max(row, "Selenium_ug"),

                    "low_copper_mg": get_min(row, "Copper_mg"),
                    "highcopper_mg": get_max(row, "Copper_mg"),

                    "low_fluoride_mg": get_min(row, "Fluoride_mg"),
                    "high_fluoride_mg": get_max(row, "Fluoride_mg"),

                    "low_chromium_mg": get_min(row, "Chromium_mg"),
                    "high_chromium_mg": get_max(row, "Chromium_mg"),
                }


                Disease.objects.update_or_create(id=disease_id, defaults=defaults)
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully imported {count} diseases"))

