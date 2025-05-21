from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('staff_logout/', views.staff_logout, name='staff_logout'),
]