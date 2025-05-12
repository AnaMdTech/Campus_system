from django.urls import path
from . import views

app_name = 'meal'

urlpatterns = [
    path('scan/', views.meal_scan_simulator, name='scan_simulator'), # Renders the scanner page
    path('process/', views.process_scan, name='process_scan'),       # Processes the scanned data
]