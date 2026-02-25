import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from recipes.models import Disease, AppUser, Disease_Avoid_Food, Recipe_Ingredients
from recipes.models import Recipe
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect("login_page")
    return render(request, "main/home.html")

def landing_page(request):
    if request.user.is_authenticated:
        return redirect("landing_page")

    return render(request, 'main/landingpage.html',
                  {'app_name': 'Eattiligent',
                   'user_email': 'Login'})


################## Login #################
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


################## Logout #################
def logout_view(request):
    logout(request)
    return redirect("landing_page")

################## Register #################
def registration_page(request):
    error_info = {"errors": {}, "email": ""}
    diseases = Disease.objects.all()

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_pass = request.POST.get("confirm_pass", "")

        bmr = request.POST.get("bmr", "").strip()
        disease_id = request.POST.get("disease")
        dietary_restriction = request.POST.get("dietary_restriction", "").strip()
        weight = request.POST.get("weight", "").strip()
        goal_weight = request.POST.get("goal_weight", "").strip()
        allergy = request.POST.get("allergy", "").strip()
        meals_per = request.POST.get("meals_per", "").strip()
        snacks_per = request.POST.get("snacks_per", "").strip()

        error_info["email"] = email
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

        user_disease = None
        if disease_id and disease_id.isdigit():
            try:
                user_disease = Disease.objects.get(id=disease_id)
            except Disease.DoesNotExist:
                error_info["errors"]["disease"] = "Selected disease is not valid"

        if not error_info["errors"]:
            try:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password
                )

                app_user = AppUser.objects.create(
                    user=user,
                    bmr=float(bmr) if bmr else None,
                    dietary_restriction=dietary_restriction or None,
                    weight=float(weight) if weight else None,
                    goal_weight=float(goal_weight) if goal_weight else None,
                    allergy=allergy or None,
                    meals_per=int(meals_per) if meals_per else None,
                    snacks_per=int(snacks_per) if snacks_per else None
                )

                # M2M must be set AFTER create, NOT inside create()
                if user_disease:
                    app_user.diseases.set([user_disease])

                return redirect("login_page")
            except Exception as e:
                print(f"Registration Error: {e}")
                error_info["errors"]["registration"] = f"Database error: {e}"

    all = {**error_info, "diseases": diseases}
    return render(request, 'main/register.html', all)


def search_page(request):
    return render(request, 'recipes/searchpage.html')


def recipes_list(request):
    recipes = Recipe.objects.all().order_by('title')

    if request.user.is_authenticated:
        try:
            app_user = AppUser.objects.get(user=request.user)

            # Get user's disease IDs
            user_disease_ids = app_user.diseases.values_list('id', flat=True)

            # Get ingredient IDs to avoid based on user's diseases
            avoid_ingredient_ids = Disease_Avoid_Food.objects.filter(
                disease_id__in=user_disease_ids
            ).values_list('ingredient_id', flat=True)

            # Exclude recipes that contain any avoided ingredients
            if avoid_ingredient_ids:
                avoided_recipe_ids = Recipe_Ingredients.objects.filter(
                    ingredient_id__in=avoid_ingredient_ids
                ).values_list('recipe_id', flat=True)

                recipes = recipes.exclude(id__in=avoided_recipe_ids)

        except AppUser.DoesNotExist:
            pass

    return render(request, 'recipes/recipes_list.html', {'recipes': recipes})
def recipe_detail(request, recipe_id):
    from django.shortcuts import get_object_or_404
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

    return render(request, 'recipes/selected_recipes.html', {"recipes": recipe_list})



@login_required
def user_profile(request):
    """
    Display and update user profile
    """
    if request.method == 'POST':
        # Get the current user
        user = request.user
        
        # Update profile fields
        # Note: You'll need to create a UserProfile model if it doesn't exist
        # For now, this is a placeholder
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')
    
    # GET request - just display the profile
    return render(request, 'recipes/userprofile.html')