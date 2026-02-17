from django.contrib import admin
from django.urls import path
from recipes import views

urlpatterns = [    
    path('admin/', admin.site.urls),
    path('login/', views.login_page, name='login_page'),
    path('register/', views.registration_page, name='registration_page'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home')
]
