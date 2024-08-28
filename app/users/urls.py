from django.urls import path

import users.views


urlpatterns = [
    path("auth/signin", users.views.SignInAPIView.as_view()),
    path("auth/signup", users.views.SignUpAPIView.as_view()),
    path("auth/signout", users.views.SignOutAPIView.as_view()),
    path("auth/username/check", users.views.UsernameCheckAPIView.as_view()),
    path("auth/email/check", users.views.EmailCheckAPIView.as_view()),
    path("auth/email/verify", users.views.EmailVerifyAPIView.as_view()),
    path("user/manage", users.views.CurrentUserRetrieveUpdateAPIView.as_view()),
]
