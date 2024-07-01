from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('about/', views.about, name='about'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_of_service/', views.terms_of_service, name='terms_of_service'),
    path('tools/', views.tools, name='tools'),
    path('text_analysis/', views.text_analysis, name='text_analysis'),
    path('voice_analysis/', views.voice_analysis, name='voice_analysis'),
    path('live_video_analysis/', views.live_video_analysis, name='live_video_analysis'),
    path('', views.index, name='index'),
]

