
from django.db import models
from django.contrib.auth.models import User

class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bmr = models.FloatField(blank=True, null=True)
    disease = models.CharField(max_length=255, blank=True, null=True)
    dietary_restriction = models.CharField(max_length=255, blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    goal_weight = models.FloatField(blank=True, null=True)
    allergy = models.CharField(max_length=255, blank=True, null=True)
    meals_per = models.IntegerField(blank=True, null=True)
    snacks_per = models.IntegerField(blank=True, null=True)
from django.contrib.auth.models import User

class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bmr = models.FloatField(blank=True, null=True)
    disease = models.CharField(max_length=255, blank=True, null=True)
    dietary_restriction = models.CharField(max_length=255, blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    goal_weight = models.FloatField(blank=True, null=True)
    allergy = models.CharField(max_length=255, blank=True, null=True)
    meals_per = models.IntegerField(blank=True, null=True)
    snacks_per = models.IntegerField(blank=True, null=True)


class Recipe(models.Model):
	id = models.IntegerField(primary_key=True)
	title = models.CharField(max_length=255)
	meal_type = models.CharField(max_length=255, blank=True, null=True)
	measurement = models.TextField(blank=True)
	ingredients = models.TextField(blank=True)
	substitutions = models.TextField(blank=True, null=True)
	how_to_cook = models.TextField(blank=True, null=True)

	calories_kcal = models.FloatField(blank=True, null=True)
	saturated_fat_g = models.FloatField(blank=True, null=True)
	carbs_g = models.FloatField(blank=True, null=True)
	protein_g = models.FloatField(blank=True, null=True)
	fiber_g = models.FloatField(blank=True, null=True)
	sugar_g = models.FloatField(blank=True, null=True)
	cholesterol_mg = models.FloatField(blank=True, null=True)
	sodium_mg = models.FloatField(blank=True, null=True)
	potassium_mg = models.FloatField(blank=True, null=True)
	iron_mg = models.FloatField(blank=True, null=True)
	calcium_mg = models.FloatField(blank=True, null=True)
	phosphorus_mg = models.FloatField(blank=True, null=True)
	magnesium_mg = models.FloatField(blank=True, null=True)

	vitamin_a_ug = models.FloatField(blank=True, null=True)
	vitamin_b_mg = models.FloatField(blank=True, null=True)
	vitamin_c_mg = models.FloatField(blank=True, null=True)
	vitamin_d_ug = models.FloatField(blank=True, null=True)
	vitamin_e_mg = models.FloatField(blank=True, null=True)
	vitamin_k_ug = models.FloatField(blank=True, null=True)

	zinc_mg = models.FloatField(blank=True, null=True)
	iodine_ug = models.FloatField(blank=True, null=True)
	selenium_ug = models.FloatField(blank=True, null=True)
	copper_mg = models.FloatField(blank=True, null=True)
	magnesium_2_mg = models.FloatField(blank=True, null=True)
	fluoride_mg = models.FloatField(blank=True, null=True)
	chromium_mg = models.FloatField(blank=True, null=True)

	dietary_restrictions = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return f"{self.title} ({self.id})"
class Disease(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    superfood = models.TextField(blank=True, null=True)
    must_avoid = models.TextField(blank=True, null=True)
    recommended_activity_level = models.CharField(max_length=255, blank=True, null=True)
    
    calories_kcal = models.CharField(max_length=50, blank=True, null=True)
    saturated_fat_g = models.CharField(max_length=50, blank=True, null=True)
    carbs_g = models.CharField(max_length=50, blank=True, null=True)
    protein_g = models.CharField(max_length=50, blank=True, null=True)
    fiber_g = models.CharField(max_length=50, blank=True, null=True)
    sugar_g = models.CharField(max_length=50, blank=True, null=True)
    cholesterol_mg = models.CharField(max_length=50, blank=True, null=True)
    sodium_mg = models.CharField(max_length=50, blank=True, null=True)
    potassium_mg = models.CharField(max_length=50, blank=True, null=True)
    iron_mg = models.CharField(max_length=50, blank=True, null=True)
    calcium_mg = models.CharField(max_length=50, blank=True, null=True)
    phosphorus_mg = models.CharField(max_length=50, blank=True, null=True)
    magnesium_mg = models.CharField(max_length=50, blank=True, null=True)
    
    vitamin_a_ug = models.CharField(max_length=50, blank=True, null=True)
    vitamin_b_mg = models.CharField(max_length=50, blank=True, null=True)
    vitamin_c_mg = models.CharField(max_length=50, blank=True, null=True)
    vitamin_d_ug = models.CharField(max_length=50, blank=True, null=True)
    vitamin_e_mg = models.CharField(max_length=50, blank=True, null=True)
    vitamin_k_ug = models.CharField(max_length=50, blank=True, null=True)
    
    zinc_mg = models.CharField(max_length=50, blank=True, null=True)
    iodine_ug = models.CharField(max_length=50, blank=True, null=True)
    selenium_ug = models.CharField(max_length=50, blank=True, null=True)
    copper_mg = models.CharField(max_length=50, blank=True, null=True)
    fluoride_mg = models.CharField(max_length=50, blank=True, null=True)
    chromium_mg = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.id})"
    
class Ingredient(models.Model):
    id = models.IntegerField(primary_key=True)
    food = models.CharField(max_length=255)
    caloric_value = models.FloatField(blank=True, null=True)
    fat = models.FloatField(blank=True, null=True)
    saturated_fats = models.FloatField(blank=True, null=True)
    monounsaturated_fats = models.FloatField(blank=True, null=True)
    polyunsaturated_fats = models.FloatField(blank=True, null=True)
    carbohydrates = models.FloatField(blank=True, null=True)
    sugars = models.FloatField(blank=True, null=True)
    protein = models.FloatField(blank=True, null=True)
    dietary_fiber = models.FloatField(blank=True, null=True)
    cholesterol = models.FloatField(blank=True, null=True)
    sodium = models.FloatField(blank=True, null=True)
    water = models.FloatField(blank=True, null=True)
    
    vitamin_a = models.FloatField(blank=True, null=True)
    vitamin_b1 = models.FloatField(blank=True, null=True)
    vitamin_b11 = models.FloatField(blank=True, null=True)
    vitamin_b12 = models.FloatField(blank=True, null=True)
    vitamin_b2 = models.FloatField(blank=True, null=True)
    vitamin_b3 = models.FloatField(blank=True, null=True)
    vitamin_b5 = models.FloatField(blank=True, null=True)
    vitamin_b6 = models.FloatField(blank=True, null=True)
    vitamin_c = models.FloatField(blank=True, null=True)
    vitamin_d = models.FloatField(blank=True, null=True)
    vitamin_e = models.FloatField(blank=True, null=True)
    vitamin_k = models.FloatField(blank=True, null=True)
    
    calcium = models.FloatField(blank=True, null=True)
    copper = models.FloatField(blank=True, null=True)
    iron = models.FloatField(blank=True, null=True)
    magnesium = models.FloatField(blank=True, null=True)
    manganese = models.FloatField(blank=True, null=True)
    phosphorus = models.FloatField(blank=True, null=True)
    potassium = models.FloatField(blank=True, null=True)
    selenium = models.FloatField(blank=True, null=True)
    zinc = models.FloatField(blank=True, null=True)
    nutrition_density = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.food} ({self.id})"    