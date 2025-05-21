from django.urls import path
from . import views

app_name = 'meal'

urlpatterns = [
    path('scan/', views.meal_scan_simulator, name='scan_simulator'), # Renders the scanner page
    path('staff_login/', views.meal_staff_login, name='staff_login'),
    path('staff_logout/', views.meal_staff_logout, name='staff_logout'),
    path('start/', views.start_scanner, name='start_scanner'),
    path('process/', views.process_scan, name='process_scan'),       # Processes the scanned data
]