import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from recipes.models import Disease, AppUser, UserPickedRecipes
from recipes.models import Recipe


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        u_email = request.user.email  
        return redirect("recipes_list")
    else: 
        return render(request, 'main/home.html',
                      {'app_name': 'Eattiligent',
                       'user_email': 'Login'})


################## Login #################
def login_page(request):
    error_info = {"errors": {}, "email": ""}

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
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
                return redirect("home")

    return render(request, "main/login.html", error_info)
################## Logout #################
def logout_view(request):
    logout(request)  
    return redirect("home")  

################## Register #################
def registration_page(request):
    error_info = {"errors": {}, "email":""}
    diseases = Disease.objects.all()

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_pass = request.POST.get("confirm_pass", "")

        #can be null
        bmr = request.POST.get("bmr", "")
        disease_id = request.POST.get("disease")
        dietary_restriction = request.POST.get("dietary_restriction", "")
        weight = request.POST.get("weight", "")
        goal_weight = request.POST.get("goal_weight", "")
        allergy = request.POST.get("allergy", "")
        meals_per = request.POST.get("meals_per", "")
        snacks_per = request.POST.get("snacks_per", "")

        error_info["email"] = email
        if not email:
            error_info["errors"]["email"]= "Email is required"
        else:
            try:
                validate_email(email)
            except ValidationError:
                error_info["errors"]["email"] = "Not a valid email address"
        if not password:            
            error_info["errors"]["password"] = "Password is required"
        if password != confirm_pass:
            error_info["errors"]["confirm_pass"] = "Passwords do not match"
        
        #find the disease id in the databse
        user_disease = None
        if disease_id:
            try:
                user_disease = Disease.objects.get(id = disease_id)
            except Disease.DoesNotExist:
                error_info["errors"]["disease"] = "Selected disease is not valid"

        if not error_info["errors"]:
            user = User.objects.create_user(
                username = email,
                email = email,
                password = password
            )

            AppUser.objects.create(
                user = user,
                bmr = bmr or None,
                disease=user_disease or None,
                dietary_restriction=dietary_restriction or None,
                weight=weight or None,
                goal_weight=goal_weight or None,
                allergy=allergy or None,
                meals_per=meals_per or None,
                snacks_per=snacks_per or None
            )
            return redirect("login_page")
    all = {**error_info, "diseases": diseases}
    return render(request, 'main/register.html', all) #pass list for bootstrap

def search_page(request):
    return render(request, 'recipes/searchpage.html')


def recipes_list(request):
    recipes = Recipe.objects.all().order_by('title')
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