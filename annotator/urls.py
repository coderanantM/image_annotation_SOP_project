from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('annotate/', views.annotate, name='annotate'),
]
