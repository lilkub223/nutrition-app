from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login as auth_login, logout
from recipes.models import Disease, AppUser


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

        # can be null
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
                # Check for existing user so it doesn't crash later
                if User.objects.filter(username=email).exists():
                    error_info["errors"]["email"] = "Email already exists"
            except ValidationError:
                error_info["errors"]["email"] = "Not a valid email address"

        if not password:
            error_info["errors"]["password"] = "Password is required"
        if password != confirm_pass:
            error_info["errors"]["confirm_pass"] = "Passwords do not match"

        # find the disease id in the database
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

                AppUser.objects.create(
                    user=user,
                    bmr=float(bmr) if bmr else None,
                    disease=user_disease or None,
                    dietary_restriction=dietary_restriction or None,
                    weight=float(weight) if weight else None,
                    goal_weight=float(goal_weight) if goal_weight else None,
                    allergy=allergy or None,
                    meals_per=int(meals_per) if meals_per else None,
                    snacks_per=int(snacks_per) if snacks_per else None
                )
                return redirect("login_page")
            except Exception as e:
                # This helps pinpoint errors in the Docker console
                print(f"Registration Error: {e}")
                error_info["errors"]["registration"] = f"Database error: {e}"

    all = {**error_info, "diseases": diseases}

    return render(request, 'main/register.html', all)


