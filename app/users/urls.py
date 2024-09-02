from django.urls import include
from django.urls import path

from users.views import SignInAPIView
from users.views import SignUpAPIView
from users.views import SignOutAPIView
from users.views import UsabilityAPIView
from users.views import EmailVerificationAPIView
from users.views import UserManageAPIView


urlpatterns = [
    path("auth", include([
        path("/signin", SignInAPIView.as_view()),
        path("/signup", SignUpAPIView.as_view()),
        path("/signout", SignOutAPIView.as_view()),
        path("/usability", UsabilityAPIView.as_view()),
        path("/verification", EmailVerificationAPIView.as_view()),
    ])),
    path("user", include([
        path("/manage", UserManageAPIView.as_view()),
    ])),
]
