from django.urls import path

from login import views

app_name = 'login'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('weatherInfo/', views.weatherInfo, name='weatherInfo')
]
