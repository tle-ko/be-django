from django.urls import include
from django.urls import path

from . import views


urlpatterns = [
    path("auth", include([
        path("/signin", views.SignInAPIView.as_view()),
        path("/signup", views.SignUpAPIView.as_view()),
        path("/signout", views.SignOutAPIView.as_view()),
        path("/usability", views.UsabilityAPIView.as_view()),
        path("/verification", views.EmailVerificationAPIView.as_view()),
    ])),
    path("user/manage", views.UserManageAPIView.as_view()),
]
