from django.db import models
from django.contrib.auth.models import User

class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bmr = models.FloatField(blank=True, null=True)
    diseases = models.ManyToManyField("Disease", blank=True)
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
	# measurement = models.TextField(blank=True)
	ingredients = models.TextField(blank=True)
	# substitutions = models.TextField(blank=True, null=True)
	how_to_cook = models.TextField(blank=True, null=True)

	"""
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
    """

	def __str__(self):
		return f"{self.title} ({self.id})"

class Disease(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    # superfood = models.CharField(max_length=255, blank=True, null=True)
    # must_avoid = models.TextField(blank=True, null=True)
    # recommended_activity_level = models.CharField(max_length=255, blank=True, null=True)


    # needs top and bottom range values:
    
    low_calories_kcal = models.FloatField(blank=True, null=True)
    high_calories_kcal = models.FloatField(blank=True, null=True)

    low_saturated_fat_g = models.FloatField(blank=True, null=True)
    high_saturated_fat_g = models.FloatField(blank=True, null=True)

    low_carbs_g = models.FloatField(blank=True, null=True)
    high_carbs_g = models.FloatField(blank=True, null=True)

    low_protein_g = models.FloatField(blank=True, null=True)
    high_protein_g = models.FloatField(blank=True, null=True)

    low_fiber_g = models.FloatField(blank=True, null=True)
    high_fiber_g = models.FloatField(blank=True, null=True)

    low_sugar_g = models.FloatField(blank=True, null=True)
    high_sugar_g = models.FloatField(blank=True, null=True)

    low_cholesterol_mg = models.FloatField(blank=True, null=True)
    high_cholesterol_mg = models.FloatField(blank=True, null=True)

    low_sodium_mg = models.FloatField(blank=True, null=True)
    high_sodium_mg = models.FloatField(blank=True, null=True)

    low_potassium_mg = models.FloatField(blank=True, null=True)
    high_potassium_mg = models.FloatField(blank=True, null=True)

    low_iron_mg = models.FloatField(blank=True, null=True)
    high_iron_mg = models.FloatField(blank=True, null=True)

    low_calcium_mg = models.FloatField(blank=True, null=True)
    high_calcium_mg = models.FloatField(blank=True, null=True)

    low_phosphorus_mg = models.FloatField(blank=True, null=True)
    high_phosphorus_mg = models.FloatField(blank=True, null=True)

    low_magnesium_mg = models.FloatField(blank=True, null=True)
    high_magnesium_mg = models.FloatField(blank=True, null=True)

    low_vitamin_a_ug = models.FloatField(blank=True, null=True)
    high_vitamin_a_ug = models.FloatField(blank=True, null=True)

    low_vitamin_b_mg = models.FloatField(blank=True, null=True)
    high_vitamin_b_mg = models.FloatField(blank=True, null=True)

    low_vitamin_c_mg = models.FloatField(blank=True, null=True)
    high_vitamin_c_mg = models.FloatField(blank=True, null=True)

    low_vitamin_d_ug = models.FloatField(blank=True, null=True)
    high_vitamin_d_ug = models.FloatField(blank=True, null=True)

    low_vitamin_e_mg = models.FloatField(blank=True, null=True)
    high_vitamin_e_mg = models.FloatField(blank=True, null=True)

    low_vitamin_k_ug = models.FloatField(blank=True, null=True)
    high_vitamin_k_ug = models.FloatField(blank=True, null=True)

    low_zinc_mg = models.FloatField(blank=True, null=True)
    high_zinc_mg = models.FloatField(blank=True, null=True)

    low_iodine_ug = models.FloatField(blank=True, null=True)
    high_iodine_ug = models.FloatField(blank=True, null=True)

    low_selenium_ug = models.FloatField(blank=True, null=True)
    high_selenium_ug = models.FloatField(blank=True, null=True)

    low_copper_mg = models.FloatField(blank=True, null=True)
    high_copper_mg = models.FloatField(blank=True, null=True)

    low_fluoride_mg = models.FloatField(blank=True, null=True)
    high_fluoride_mg = models.FloatField(blank=True, null=True)

    low_chromium_mg = models.FloatField(blank=True, null=True)
    high_chromium_mg = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.id})"
    

class Ingredient(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    measurements = models.TextField(blank=True, null=True)

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

    def __str__(self):
        return f"{self.title} ({self.id})"


class Recipe_Ingredients(models.Model):
    recipe_id = models.ForeignKey(Recipe, null=True, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, null=True, on_delete=models.CASCADE)
    recipe_ingredient_id = models.IntegerField(primary_key=True)


class Disease_Super_Food(models.Model):
    disease_id = models.ForeignKey(Disease, null=True, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, null=True, on_delete=models.CASCADE)
    disease_ingredient_id = models.IntegerField(primary_key=True)

class Disease_Avoid_Food(models.Model):
    disease_id = models.ForeignKey(Disease, null=True, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, null=True, on_delete=models.CASCADE)
    disease_ingredient_id = models.IntegerField(primary_key=True)

class UserPickedRecipes(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    recipe = models.TextField(blank=True, null=True)  
    def __str__(self):
        recipe_preview = self.recipe[:50] if self.recipe else "No recipes"
        return f"{self.user.user.email} - {recipe_preview}"