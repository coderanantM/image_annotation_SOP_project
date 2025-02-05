from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('upload/', views.upload_image, name='upload_image'),
    path('annotate/<int:pk>/', views.annotate_image, name='annotate_image'),
    path('save-annotations/<int:pk>/', views.save_annotations, name='save_annotations'),
]