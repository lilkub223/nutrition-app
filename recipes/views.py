import json
import random
import re
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import unquote

from urllib3 import request
import recipes
from recipes.models import Disease, AppUser, Disease_Avoid_Food, Ingredient, Recipe_Ingredients, UserPickedRecipes, UserPickedDisease, Disease_Super_Food,DailyLog, WorkoutEntry
from recipes.models import Recipe
from nutrition_project.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from datetime import date, timedelta
from recipes.models import DailyLog, MealEntry, WorkoutEntry

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect("login_page")
    
    #diseases = Disease.objects.all()
    return render(request, "main/home.html")


def landing_page(request):
    if request.user.is_authenticated:
        return redirect("home")

    return render(request, 'main/landingpage.html',
                  {'app_name': 'Eattiligent',
                   'user_email': 'Login'})


# login
def login_page(request):
    error_info = {"errors": {}, "email": ""}

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        error_info["email"] = email

        try:
            validate_email(email)
        except ValidationError:
            error_info["errors"]["email"] = "Not a valid email address"

        if not password:
            error_info["errors"]["password"] = "Not a valid password"

        if not error_info["errors"]:
            user_info = authenticate(request, username=email, password=password)

            if user_info is None:
                error_info["errors"]["login"] = "Invalid email or password"
            else:
                auth_login(request, user_info)

                next_url = request.GET.get("next")
                if next_url:
                    return redirect(next_url)
                return redirect("home")

    return render(request, "main/login.html", error_info)


# logout
def logout_view(request):
    logout(request)
    return redirect("login_page")

# registration
def registration_page(request):
    form_data = {
        "email": "", "weight": "", "goal_weight": "", "bmr" : "", "dietary_restriction": "", 
        "allergy": "", "meals_per": "", "snacks_per": ""
    }
    error_info = {"errors": {}}
    #error_info = {"errors": {}, "email": ""}
    diseases = Disease.objects.all()

    if request.method == "POST":
        for fields in form_data.keys():
            form_data[fields] = request.POST.get(fields, "").strip()

        email = form_data["email"].lower()
        password = request.POST.get("password", "")
        confirm_pass = request.POST.get("confirm_pass", "")
        disease_id = request.POST.get("disease")

        if not email:
            error_info["errors"]["email"] = "Email is required"
        else:
            try:
                validate_email(email)
                if User.objects.filter(username=email).exists():
                    error_info["errors"]["email"] = "Email already exists"
            except ValidationError:
                error_info["errors"]["email"] = "Not a valid email address"

        if not password:
            error_info["errors"]["password"] = "Password is required"
        if password != confirm_pass:
            error_info["errors"]["confirm_pass"] = "Passwords do not match"
            
        if not error_info["errors"]:
            try:
                user = User.objects.create_user(username=email, email=email, password=password)
                app_user = AppUser.objects.create(
                    user=user,
                    bmr=float(form_data["bmr"]) if form_data["bmr"] else None,
                    dietary_restriction=form_data["dietary_restriction"] or None,
                    weight=float(form_data["weight"]) if form_data["weight"] else None,
                    goal_weight=float(form_data["goal_weight"]) if form_data["goal_weight"] else None,
                    allergy=form_data["allergy"] or None,
                    meals_per=int(form_data["meals_per"]) if form_data["meals_per"] else None,
                    snacks_per=int(form_data["snacks_per"]) if form_data["snacks_per"] else None
                
                ) #user_disease = None
                if disease_id and disease_id.isdigit():
                    try:
                        user_disease = Disease.objects.get(id=disease_id)
                        UserPickedDisease.objects.create(user=app_user, disease=f"{user_disease.title}]")
                        app_user.diseases.set([user_disease])
                    except Disease.DoesNotExist:
                        error_info["errors"]["disease"] = "Selected disease is not valid"

                return redirect("login_page")
            except Exception as e:
                print(f"Registration Error: {e}")
                error_info["errors"]["registration"] = f"Database error: {e}"

        
                # disease_name = ""
                # if user_disease:
                #     disease_name = f"{user_disease.title}]"
                
                # UserPickedDisease.objects.get_or_create(
                #     user=app_user,
                #     defaults={'disease': disease_name}
                # )

                # M2M must be set AFTER create, NOT inside create()
                # if user_disease:
                #     app_user.diseases.set([user_disease])

                # return redirect("login_page")
            
    all = {**error_info, "diseases": diseases}
    return render(request, 'main/register.html', all)


def search_page(request):
    return render(request, 'recipes/searchpage.html')


def recipes_list(request):
    recipes = list(Recipe.objects.all().order_by('title'))

    if request.user.is_authenticated:
        try:
            app_user = AppUser.objects.get(user=request.user)

            try:
                user_picks = UserPickedDisease.objects.get(user=app_user)
                picked_disease = [d for d in user_picks.disease.rstrip("]").split("]") if d]
                user_disease_ids = Disease.objects.filter(title__in=picked_disease).values_list('id', flat=True)
            except UserPickedDisease.DoesNotExist:
                user_disease_ids = []

            avoid_ingredient_ids = Disease_Avoid_Food.objects.filter(
                disease_id__in=user_disease_ids
            ).values_list('ingredient_id', flat=True)

            if avoid_ingredient_ids:
                avoided_recipe_ids = Recipe_Ingredients.objects.filter(
                    ingredient_id__in=avoid_ingredient_ids
                ).values_list('recipe_id', flat=True)
                recipes = list(Recipe.objects.all().order_by('title').exclude(id__in=avoided_recipe_ids))

        except AppUser.DoesNotExist:
            pass

    # Build nutrition list — always runs, same size/order as recipes
    nutrition_list = []
    for recipe in recipes:
        recipe_ingredients = Recipe_Ingredients.objects.filter(recipe_id=recipe).select_related('ingredient_id')
        total_calories = sum(ri.ingredient_id.calories_kcal or 0 for ri in recipe_ingredients)
        total_protein = sum(ri.ingredient_id.protein_g or 0 for ri in recipe_ingredients)
        total_carbs = sum(ri.ingredient_id.carbs_g or 0 for ri in recipe_ingredients)
        total_fiber = sum(ri.ingredient_id.fiber_g or 0 for ri in recipe_ingredients)
        total_saturated_fat_g = sum(ri.ingredient_id.saturated_fat_g or 0 for ri in recipe_ingredients)

        nutrition_list.append({
            'calories': round(total_calories, 1) if total_calories else 'N/A',
            'protein': round(total_protein, 1) if total_protein else 'N/A',
            'carbs': round(total_carbs, 1) if total_carbs else 'N/A',
            'fiber': round(total_fiber, 1) if total_carbs else 'N/A',
            'fats': round(total_saturated_fat_g, 1) if total_carbs else 'N/A',

        })
 
    return render(request, 'recipes/recipes_list.html', {
        'recipes': recipes,
        'recipes_with_nutrition': list(zip(recipes, nutrition_list)),
    })


def recipe_detail(request, recipe_id):
    #from django.shortcuts import get_object_or_404
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

#saving recipes to the user's picked list
@csrf_exempt 
def add_to_picked_recipes(request):
    if request.method == 'POST':
        #if user is logged in
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'You must be logged in to pick recipes'})
        
        try:
            # Parse the JSON data 
            data = json.loads(request.body)
            recipe_title = data.get('recipe_title')
            
            # check recipe title
            if not recipe_title:
                return JsonResponse({'success': False, 'error': 'Recipe title is required'})
            
            # Get or create AppUser for the logged-in user
            # This links Django's User to your custom AppUser model
            app_user, created = AppUser.objects.get_or_create(user=request.user)
            
            # Get or create UserPickedRecipes for this user
            # Each user has one UserPickedRecipes record with all their picks
            user_picks, created = UserPickedRecipes.objects.get_or_create(user=app_user)
            
            # Parse the existing recipe list from the TextField
            # Format is: "Recipe1]Recipe2]Recipe3]"
            if user_picks.recipe:
                recipe_list = user_picks.recipe.rstrip("]").split("]")
                recipe_list = [r for r in recipe_list if r]  # Remove empty strings
            else:
                recipe_list = []
            
            #  if recipe is already in the user's picks
            if recipe_title not in recipe_list:
                # Add  new recipe
                recipe_list.append(recipe_title)
                # Save to database with ] delimiter
                user_picks.recipe = "]".join(recipe_list) + "]"
                user_picks.save()
                return JsonResponse({'success': True, 'message': f'Added {recipe_title} to your picks!'})
            else:
                return JsonResponse({'success': False, 'error': f'{recipe_title} is already in your picks'})
                
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# Added recipes page
def selected_recipes(request):
    try:
        app_user = AppUser.objects.get(user=request.user)
        
        user_picks = UserPickedRecipes.objects.get(user=app_user)
    
        if user_picks.recipe:
            recipe_list = user_picks.recipe.rstrip("]").split("]")
            recipe_list = [r for r in recipe_list if r]  # Remove empty strings
        else:
            recipe_list = []

    except AppUser.DoesNotExist:
        recipe_list = []
    except UserPickedRecipes.DoesNotExist:
        recipe_list = []


    nutrition_list = []
    i = 0
    for recipe in recipe_list:
        current_recipe = Recipe.objects.get(title=recipe)
        recipe_list[i] = current_recipe
        recipe_ingredients = Recipe_Ingredients.objects.filter(recipe_id=current_recipe.id).select_related('ingredient_id')
        total_calories = sum(ri.ingredient_id.calories_kcal or 0 for ri in recipe_ingredients)
        total_protein = sum(ri.ingredient_id.protein_g or 0 for ri in recipe_ingredients)
        total_carbs = sum(ri.ingredient_id.carbs_g or 0 for ri in recipe_ingredients)
        total_fiber = sum(ri.ingredient_id.fiber_g or 0 for ri in recipe_ingredients)
        total_saturated_fat_g = sum(ri.ingredient_id.saturated_fat_g or 0 for ri in recipe_ingredients)

        nutrition_list.append({
            'calories': round(total_calories, 1) if total_calories else 'N/A',
            'protein': round(total_protein, 1) if total_protein else 'N/A',
            'carbs': round(total_carbs, 1) if total_carbs else 'N/A',
            'fiber': round(total_fiber, 1) if total_carbs else 'N/A',
            'fats': round(total_saturated_fat_g, 1) if total_carbs else 'N/A',

        })
        
        i += 1
    

    return render(request, 'recipes/selected_recipes.html', {"recipes": recipe_list, "recipes_with_nutrition": list(zip(recipe_list, nutrition_list))})


def remove_recipes(request):
    try:
        app_user = AppUser.objects.get(user=request.user)
        
        user_picks = UserPickedRecipes.objects.get(user=app_user)
    
        if user_picks.recipe:
            recipe_list = user_picks.recipe.rstrip("]").split("]")
            recipe_list = [r for r in recipe_list if r]  # Remove empty strings
        else:
            recipe_list = []

    except AppUser.DoesNotExist:
        recipe_list = []
    except UserPickedRecipes.DoesNotExist:
        recipe_list = []

    data = json.loads(request.body)
    recipe_title = data.get('recipe_title')

    if recipe_title in recipe_list:
        recipe_list.remove(recipe_title)
    
    user_picks.recipe = "]".join(recipe_list) + "]"
    user_picks.save()
    return JsonResponse({'success': True, 'message': f'Removed {recipe_title} from your picks!'})

# Forgot password page
def forgot_password_page(request):
    error_info = {"errors": {}, "email": "", "sent": False}

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        error_info["email"] = email

        if not email:
            error_info["errors"]["email"]= "Email is required"
        else:
            try:
                validate_email(email)
            except ValidationError:
                error_info["errors"]["email"] = "Not a valid email address"
            
            send_mail(
                subject= "Eatilligent Forgotten Password",
                message= "This email is for your forgotten password",
                from_email=EMAIL_HOST_USER,
                recipient_list= [email],
            )          
            error_info["sent"] = True     
    return render(request, "main/forgotpass.html", error_info)



@login_required
def user_profile(request):
    app_user = get_object_or_404(AppUser, user=request.user)
    all_diseases = Disease.objects.all().order_by('title')
    user_picks, created = UserPickedDisease.objects.get_or_create(user=app_user)

    if request.method == 'POST':
        # Capture the new selection from the dropdown for diseases
        new_disease_title = request.POST.get('disease')
        
        # Current disease user input
        current_badge_titles = request.POST.getlist('active_diseases')

        # Combines added disease and old diseasinto a single list
        updated_title_list = list(set(current_badge_titles))
        if new_disease_title and new_disease_title not in updated_title_list:
            updated_title_list.append(new_disease_title)

        disease_objects = Disease.objects.filter(title__in=updated_title_list)
        app_user.diseases.set(disease_objects)

        final_titles = [d.title for d in disease_objects]
        user_picks.disease = "]".join(final_titles) + "]" if final_titles else ""

        # Saves user info
        app_user.weight = request.POST.get('weight') or app_user.weight
        app_user.height = request.POST.get('height') or app_user.height
        app_user.age = request.POST.get('age') or app_user.age
        app_user.gender = request.POST.get('gender')
        app_user.activity_level = request.POST.get('activity_level')

        restrictions_list = request.POST.getlist('dietary_restrictions')
        app_user.dietary_restriction = ", ".join(restrictions_list)
        
        app_user.save()
        user_picks.save()
        
        return redirect('user_profile')

    # Parses through disease list
    picked_diseases = [d for d in user_picks.disease.rstrip("]").split("]") if d]

    return render(request, 'recipes/userprofile.html', {
        'app_user': app_user,
        'all_diseases': all_diseases,
        'picked_diseases': picked_diseases,
    })

def disease_page(request):
    if not request.user.is_authenticated:
        return redirect("login_page")
    
    diseases = Disease.objects.prefetch_related(
        "disease_super_food_set__ingredient_id",
        "disease_avoid_food_set__ingredient_id"
    )
    return render(request, "main/disease_page.html",{
        "diseases": diseases
    })


def disease_detail(request, id):
    if not request.user.is_authenticated:
        return redirect("login_page")
    
    diseases = Disease.objects.prefetch_related(
        "disease_super_food_set__ingredient_id",
        "disease_avoid_food_set__ingredient_id"
    ).get(id=id)

    return render(request, "main/disease_detail.html",{
        "diseases": diseases
    })


def grocery_list(request):
    try:
        app_user = AppUser.objects.get(user=request.user)
        
        user_picks = UserPickedRecipes.objects.get(user=app_user)
    
        if user_picks.recipe:
            recipe_list = user_picks.recipe.rstrip("]").split("]")
            recipe_list = [r for r in recipe_list if r]  # Remove empty strings
        else:
            recipe_list = []

    except AppUser.DoesNotExist:
        recipe_list = []
    except UserPickedRecipes.DoesNotExist:
        recipe_list = []

    ingredients_amount = {}

    for r in recipe_list:
        current_recipe = Recipe.objects.get(title=r)
        recipe_ingredient_list = Recipe_Ingredients.objects.filter(recipe_id=current_recipe.id)
        for i in recipe_ingredient_list:
            current_ingredient = i.ingredient_id
            if current_ingredient not in ingredients_amount:
                ingredients_amount[current_ingredient] = i.amount
            else:
                ingredients_amount[current_ingredient] += i.amount
    
    

    return render(request, 'recipes/grocerylist.html', {"recipes": recipe_list, "ingredients": ingredients_amount})

# took the format for saving recipes to the user's picked list to create it for diseases with the same functionality
@csrf_exempt 
def add_to_picked_disease(request):
    if request.method == 'POST':
        #if user is logged in
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'You must be logged in to pick a disease'})
        
        try:
            # Parse the JSON data 
            data = json.loads(request.body)
            disease_title = data.get('disease_title')
            
            # check recipe title
            if not disease_title:
                return JsonResponse({'success': False, 'error': 'Disease title is required'})
            
            # Get or create AppUser for the logged-in user
            # This links Django's User to your custom AppUser model
            app_user, created = AppUser.objects.get_or_create(user=request.user)
            
            # Get or create UserPickedDisease for this user
            # Each user has one UserPickedDisease record with all their picks
            user_picks, created = UserPickedDisease.objects.get_or_create(user=app_user)
            
            # Parse the existing recipe list from the TextField
            # Format is: "Recipe1]Recipe2]Recipe3]"
            if user_picks.disease:
                disease_list = user_picks.disease.rstrip("]").split("]")
                disease_list = [d for d in disease_list if d]  # Remove empty strings
            else:
                disease_list = []
            
            #  if disease is already in the user's picks
            if disease_title not in disease_list:
                # Add  new disease
                disease_list.append(disease_title)
                # Save to database with ] delimiter
                user_picks.disease = "]".join(disease_list) + "]"
                user_picks.save()
                return JsonResponse({'success': True, 'message': f'Added {disease_title} to your profile!'})
            else:
                return JsonResponse({'success': False, 'error': f'{disease_title} is already in your profile'})
                
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# Added disease page
def selected_disease(request):
    try:
        app_user = AppUser.objects.get(user=request.user)
        
        user_picks = UserPickedDisease.objects.get(user=app_user)
    
        if user_picks.disease:
            disease_list = user_picks.disease.rstrip("]").split("]")
            disease_list = [d for d in disease_list if d]  # Remove empty strings
            disease_list = Disease.objects.filter(title__in=disease_list)
        else:
            disease_list= []

    except AppUser.DoesNotExist:
        disease_list = []
    except UserPickedDisease.DoesNotExist:
        disease_list = []

    return render(request, 'main/selected_disease.html', {"disease": disease_list})

def custom_user_recipe(request):
    error_info = {"errors": {}}

    if request.method == "POST":
        title = request.POST.get('title')
        mealType = request.POST.getlist('type')
        ingredientList = request.POST.getlist('ingredient-selection')
        amountsList = request.POST.getlist('ingredient-amount')
        instructions = request.POST.get('instructions')

        if not title:
            error_info["errors"]["title"] = "Error"
        
        if not mealType:
            error_info["errors"]["type"] = "Error"

        if not ingredientList:
            error_info["errors"]["ingredients"] = "Error"

        if not amountsList:
            error_info["errors"]["amounts"] = "Error"

        if not instructions:
            error_info["errors"]["instructions"] = "Error"

        if not error_info["errors"]:
            newId = 1
            while newId in Recipe.objects.values_list("id", flat=True):
                newId += 1

            mealType = "; ".join(mealType)
            ingredientListString = ";".join(ingredientList)

            Recipe.objects.create(
                id = newId,
                title = title,
                meal_type = mealType,
                ingredients = ingredientListString,
                how_to_cook = instructions
            )

            for i in range(len(ingredientList)):
                current_ingredient_id = Ingredient.objects.get(title=ingredientList[i]).id
                Recipe_Ingredients.objects.create(
                    recipe_id = Recipe.objects.get(id=newId),
                    ingredient_id = Ingredient.objects.get(id=current_ingredient_id),
                    amount = amountsList[i]
                )
            
            return redirect('recipes_list')

    ingredients = Ingredient.objects.all()
    return render(request, 'recipes/customrecipe.html', {'ingredients':ingredients, "errors":error_info["errors"]})

def weekly_digest(request):
    if not request.user.is_authenticated:
        return redirect("login_page")
    
    if request.user.is_authenticated:
        try:
            app_user = AppUser.objects.get(user=request.user)

            try:
                user_picks = UserPickedDisease.objects.get(user=app_user)
                picked_disease = [d for d in user_picks.disease.rstrip("]").split("]") if d]
                user_disease_ids = Disease.objects.filter(title__in=picked_disease).values_list('id', flat=True)
            except UserPickedDisease.DoesNotExist:
                user_disease_ids = []

            avoid_ingredient_ids = Disease_Avoid_Food.objects.filter(
                disease_id__in=user_disease_ids
            ).values_list('ingredient_id', flat=True)

            if avoid_ingredient_ids:
                avoided_recipe_ids = Recipe_Ingredients.objects.filter(
                    ingredient_id__in=avoid_ingredient_ids
                ).values_list('recipe_id', flat=True)
                recipes = list(Recipe.objects.all().order_by('title').exclude(id__in=avoided_recipe_ids))

        except AppUser.DoesNotExist:
            pass
    my_recipies = Recipe.objects.filter(id__in=UserPickedRecipes.objects.filter(user=app_user).values_list('recipe', flat=True))

    # Build nutrition list — always runs, same size/order as recipes
    nutrition_list = []
    highest_cal = 0
    lowest_cal = float('inf')
    highest_cal_recipe = None
    lowest_cal_recipe = None
    for recipe in recipes:
        recipe_ingredients = Recipe_Ingredients.objects.filter(recipe_id=recipe).select_related('ingredient_id')
        total_calories = sum(ri.ingredient_id.calories_kcal or 0 for ri in recipe_ingredients)
        total_protein = sum(ri.ingredient_id.protein_g or 0 for ri in recipe_ingredients)
        total_carbs = sum(ri.ingredient_id.carbs_g or 0 for ri in recipe_ingredients)
        nutrition_list.append({
            'calories': round(total_calories, 1) if total_calories else 'N/A',
            'protein': round(total_protein, 1) if total_protein else 'N/A',
            'carbs': round(total_carbs, 1) if total_carbs else 'N/A',
        })
        if total_calories > highest_cal:
            highest_cal = total_calories
            highest_cal_recipe = recipe
        if total_calories < lowest_cal:
            lowest_cal = total_calories
            lowest_cal_recipe = recipe
        
    not_Chosen= Recipe.objects.all().exclude(title__in=[r for r in recipes])
    random_recipe = random.choice(not_Chosen) if not_Chosen else None


    ingredient_count = {}
    for recipe in recipes:
        recipe_ingredients = Recipe_Ingredients.objects.filter(recipe_id=recipe).select_related('ingredient_id')
        for ri in recipe_ingredients:
            ingredient_title = ri.ingredient_id.title
            if ingredient_title not in ingredient_count:
                ingredient_count[ingredient_title] = 1
            else:
                ingredient_count[ingredient_title] += 1

    # Get most common ingredient
    most_common_ingredient = max(ingredient_count, key=ingredient_count.get) if ingredient_count else None

    sevenDaysAgo = date.today() - timedelta(days=7)
    results = DailyLog.objects.all().filter(user=request.user)
    results = results.filter(date__gte=sevenDaysAgo)
    sevenDaysAgoLst = [date.today() - timedelta(days=i) for i in range(7)]

    results_json = json.dumps([
        {
            'date': str(log.date),
            'total_calories': log.total_calories,
            'total_protein': log.total_protein,
            'total_carbs': log.total_carbs,
            'total_fats': log.total_fats,
            'net_calories': log.net_calories,
        }
        for log in results
    ])
    
    myWorkouts= WorkoutEntry.objects.filter(daily_log__in=results)
    mydict = {str(date): 0 for date in sevenDaysAgoLst}
    for w in myWorkouts:
        mydict[str(w.daily_log.date)] += 1


    workouts_json = json.dumps({str(k): v for k, v in mydict.items()})

        


    return render(request, 'recipes/weekly_digest.html', {
        'recipes': recipes,
        'recipes_with_nutrition': list(zip(recipes, nutrition_list)),
        'most_common_ingredient': most_common_ingredient,
        'highest_cal_recipe': highest_cal_recipe,
        'not_Chosen': random_recipe,
        'lowest_cal_recipe': lowest_cal_recipe,
        'highest_cal': round(highest_cal, 1),
        'lowest_cal': round(lowest_cal, 1),
        'results_json': results_json,
        'workouts_json': workouts_json,
    })

@login_required
def daily_digest(request):
    """
    Display the daily nutrition digest page
    """
    return render(request, 'recipes/daily_digest.html')



@login_required
def daily_digest(request):
    """
    Display the daily nutrition digest page
    """
    return render(request, 'recipes/daily_digest.html')


@login_required
@require_http_methods(["GET"])
def get_daily_data(request):
    """
    API endpoint to get today's daily log data
    """
    today = date.today()
    
    # Get or create today's log
    daily_log, created = DailyLog.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={'calorie_goal': 2000}
    )
    
    # Get all meals for today
    meals = list(daily_log.meals.values(
        'id', 'meal_name', 'calories', 'protein', 'carbs', 'fats', 'logged_at'
    ))
    
    # Get all workouts for today
    workouts = list(daily_log.workouts.values(
        'id', 'workout_type', 'calories_burned', 'logged_at'
    ))
    
    return JsonResponse({
        'success': True,
        'date': str(today),
        'total_calories': daily_log.total_calories,
        'total_protein': daily_log.total_protein,
        'total_carbs': daily_log.total_carbs,
        'total_fats': daily_log.total_fats,
        'total_burned': daily_log.total_burned,
        'calorie_goal': daily_log.calorie_goal,
        'net_calories': daily_log.net_calories,
        'remaining_calories': daily_log.remaining_calories,
        'meals': meals,
        'workouts': workouts,
    })


@login_required
@require_http_methods(["POST"])
def add_meal(request):
    """
    API endpoint to add a meal entry
    """
    try:
        data = json.loads(request.body)
        today = date.today()
        
        # Get or create today's log
        daily_log, created = DailyLog.objects.get_or_create(
            user=request.user,
            date=today,
            defaults={'calorie_goal': 2000}
        )
        
        # Create meal entry
        meal = MealEntry.objects.create(
            daily_log=daily_log,
            meal_name=data.get('meal_name', 'Meal'),
            calories=float(data.get('calories', 0)),
            protein=float(data.get('protein', 0)),
            carbs=float(data.get('carbs', 0)),
            fats=float(data.get('fats', 0)),
        )
        
        # Update daily totals
        daily_log.total_calories += meal.calories
        daily_log.total_protein += meal.protein
        daily_log.total_carbs += meal.carbs
        daily_log.total_fats += meal.fats
        daily_log.save()
        
        return JsonResponse({
            'success': True,
            'meal_id': meal.id,
            'total_calories': daily_log.total_calories,
            'total_protein': daily_log.total_protein,
            'total_carbs': daily_log.total_carbs,
            'total_fats': daily_log.total_fats,
            'net_calories': daily_log.net_calories,
            'remaining_calories': daily_log.remaining_calories,
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_http_methods(["POST"])
def add_workout(request):
    """
    API endpoint to add a workout entry
    """
    try:
        data = json.loads(request.body)
        today = date.today()
        
        # Get or create today's log
        daily_log, created = DailyLog.objects.get_or_create(
            user=request.user,
            date=today,
            defaults={'calorie_goal': 2000}
        )
        
        # Create workout entry
        workout = WorkoutEntry.objects.create(
            daily_log=daily_log,
            workout_type=data.get('workout_type', 'other'),
            calories_burned=float(data.get('calories_burned', 0)),
        )
        
        # Update daily totals
        daily_log.total_burned += workout.calories_burned
        daily_log.save()
        
        return JsonResponse({
            'success': True,
            'workout_id': workout.id,
            'total_burned': daily_log.total_burned,
            'net_calories': daily_log.net_calories,
            'remaining_calories': daily_log.remaining_calories,
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    


def recipe_info(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    recipe_ingredient_list = Recipe_Ingredients.objects.filter(recipe_id=recipe.id)
    ingredient_list = []
    instructions = recipe.how_to_cook
    instruction_list = re.split(r'\d+\.\s', instructions.strip('"'))[1:]

    for i in recipe_ingredient_list:
        ingredient_list.append(i.ingredient_id)
    

    return render(request,'recipes/recipe_info.html', {"recipe": recipe, "ingredients": ingredient_list, "instructions": instruction_list})
