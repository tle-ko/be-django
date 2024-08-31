from django.urls import include
from django.urls import path

import users.views


urlpatterns = [
    path("auth", include([
        path("/signin", users.views.SignInAPIView.as_view()),
        path("/signup", users.views.SignUpAPIView.as_view()),
        path("/signout", users.views.SignOutAPIView.as_view()),
        path("/usability", users.views.UsabilityAPIView.as_view()),
        path("/verification", users.views.EmailVerificationAPIView.as_view()),
    ])),
    path("user", include([
        path("/manage", users.views.UserManageAPIView.as_view()),
    ])),
]
