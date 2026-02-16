from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from recipes.models import Disease, AppUser

def landing_page(request):
    if request.user.is_authenticated:
        u_email = request.user.email  
        return redirect("dashboard")
    else: 
        return render(request, 'recipes/landingpage.html',
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
                login(request, user_info)

                next_url = request.GET.get("next")
                return redirect(next_url or "dashboard")

    return render(request, "recipes/loginpage.html", error_info)

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
    return render(request, 'recipes/registrationpage.html', all) #pass list for bootstrap

################## Logout #################
def logout_view(request):
    logout(request)  
    return redirect("landing_page")  