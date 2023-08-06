from django.urls import path

from . import views

urlpatterns = [
    path("register/",views.RegistrationView.as_view(),name="RegistrationView"),
    path("login/",views.LoginView.as_view(),name="LoginView"),
    path("user/",views.UserView.as_view(),name="UserView"),
    path("logout/",views.LogoutView.as_view(),name="LogoutView"),
]