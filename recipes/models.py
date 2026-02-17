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
    superfood = models.CharField(max_length=255, blank=True, null=True)
    must_avoid = models.TextField(blank=True, null=True)
    recommended_activity_level = models.CharField(max_length=255, blank=True, null=True)

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
    fluoride_mg = models.FloatField(blank=True, null=True)
    chromium_mg = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.id})"