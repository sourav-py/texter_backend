from django.urls import path

from . import views

urlpatterns = [
    #path("register/",views.RegistrationView.as_view(),name="RegistrationView"),
    path("dummy-login/",views.DummyLoginView.as_view(),name="DummyLoginView"),
    
    path("user/",views.UserView.as_view(),name="UserView"),
    path("updateprofile/",views.ProfileUpdate.as_view(),name="ProfileUpdate"),
    path("logout/",views.LogoutView.as_view(),name="LogoutView"),

    path("sendotp/",views.OTPSenderView.as_view(),name="OTPSenderView"),
    path("verifyotp/",views.OTPVerificationView.as_view(),name="OTPVerificationView"),

    path("activitystatus/",views.UserActivityStatusView.as_view(),name="UserActivityStatusView"),
    path("fetchuser/",views.FetchUser.as_view(),name="FetchUser"),
]