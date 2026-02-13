from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.RegisterView.as_view()),
    path('confirm/', views.ConfirmView.as_view()),
    path('login/', views.LoginView.as_view())
]