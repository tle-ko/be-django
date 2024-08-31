from django.urls import include
from django.urls import path

import users.views


urlpatterns = [
    path("auth", include([
        path("/signin", users.views.SignInAPIView.as_view()),
        path("/signup", users.views.SignUpAPIView.as_view()),
        path("/signout", users.views.SignOutAPIView.as_view()),
        path("/username/check", users.views.UsernameCheckAPIView.as_view()),
        path("/email/check", users.views.EmailCheckAPIView.as_view()),
        path("/email/verify", users.views.EmailVerifyAPIView.as_view()),
        path("/usability", users.views.UsabilityAPIView.as_view()),
    ])),
    path("user", include([
        path("/manage", users.views.CurrentUserRetrieveUpdateAPIView.as_view()),
    ])),
]
