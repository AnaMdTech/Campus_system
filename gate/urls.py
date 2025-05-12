from django.urls import path
from . import views

app_name = 'gate'

urlpatterns = [
    path('scan/', views.gate_scan_simulator, name='scan_simulator'),
    path('verify/exit/<int:student_id>/', views.verify_exit, name='verify_exit'),
    path('process/exit/<int:student_id>/', views.process_exit, name='process_exit'),
]