from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp, name="signup"),
    path('signin/', views.SignIn, name="signin"),
    path('signout/', views.signout, name="signout")
]