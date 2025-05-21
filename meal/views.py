from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.utils.timezone import localtime
from django.views.decorators.http import require_POST
from students.models import Student
from .models import MealRecord, Cafeteria

def is_meal_staff(user):
    return user.groups.filter(name='Meal Staff').exists()

def meal_staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and is_meal_staff(user):
            login(request, user)
            return redirect('meal:start_scanner')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'meal/staff_login.html')

def meal_staff_logout(request):
    logout(request)
    return redirect('meal:staff_login')

@login_required
@user_passes_test(is_meal_staff)
def start_scanner(request):
    if request.method == 'POST':
        cafe_id = request.POST.get('cafe_location')
        if not cafe_id:
            messages.error(request, "Please select a cafeteria location.")
            return redirect('meal:start_scanner')

        # Fetch the cafeteria by ID
        cafeteria = get_object_or_404(Cafeteria, id=cafe_id)

        # Store cafeteria ID or name in session (optional, for future requests)
        request.session['selected_cafe_name'] = cafeteria.name

        # You can now pass it to the template or use it however you want
        return render(request, 'meal/scan_simulator.html', {
            'selected_cafe': cafeteria
        })
    
    # On GET request, show the cafeteria selector
    cafe_locations = Cafeteria.objects.filter(is_active=True)
    return render(request, 'meal/start_scanner.html', {'cafe_locations': cafe_locations})

@login_required
@user_passes_test(is_meal_staff)
def meal_scan_simulator(request):
    return render(request, 'meal/scan_simulator.html')

@require_POST
def process_scan(request):
    qr_identifier = request.POST.get('qr_identifier')

    if not qr_identifier:
        messages.error(request, "Invalid QR code scanned.")
        return redirect('meal:scan_simulator')

    try:
        student = Student.objects.get(student_id=qr_identifier)
    except Student.DoesNotExist:
        messages.error(request, "Student not found for the scanned QR code.")
        return redirect('meal:scan_simulator')

    # Get selected cafeteria from session
    selected_cafe_name = request.session.get('selected_cafe_name')
    if not selected_cafe_name:
        messages.error(request, "Cafeteria context is missing. Please restart the scanning process.")
        return redirect('meal:start_scanner')

    if not student.assigned_cafeteria:
        messages.error(request, f"{student.get_full_name()} is not assigned to any cafeteria.")
        return redirect('meal:scan_simulator')

    if student.assigned_cafeteria.name != selected_cafe_name:
        messages.error(request, f"{student.get_full_name()} is assigned to {student.assigned_cafeteria.name}, not {selected_cafe_name}.")
        return redirect('meal:scan_simulator')

    # Determine current meal type based on time
    now_local = localtime(timezone.now())
    current_hour = now_local.hour
    meal_type = None

    breakfast_start, breakfast_end = 6, 8
    lunch_start, lunch_end = 11, 13
    dinner_start, dinner_end = 17, 19

    if breakfast_start <= current_hour < breakfast_end:
        meal_type = 'B'
    elif lunch_start <= current_hour < lunch_end:
        meal_type = 'L'
    elif dinner_start <= current_hour < dinner_end:
        meal_type = 'D'
    else:
        message = "The cafeteria is currently closed."
        if current_hour < breakfast_start:
            message += " Breakfast service starts at 6:00."
        elif breakfast_end <= current_hour < lunch_start:
            message += " Lunch service starts at 11:00."
        elif lunch_end <= current_hour < dinner_start:
            message += " Dinner service starts at 17:00."
        else:
            message += " Please check the schedule."
        messages.error(request, message)
        return redirect('meal:scan_simulator')

    today = now_local.date()
    existing_record = MealRecord.objects.filter(student=student, date=today, meal_type=meal_type).first()

    if existing_record:
        messages.error(request, f"{student.get_full_name()} has already recorded {existing_record.get_meal_type_display()} today.")
    else:
        MealRecord.objects.create(student=student, meal_type=meal_type)
        messages.success(request, f"{student.get_full_name()} successfully recorded for {meal_type} today.")

    return redirect('meal:scan_simulator')
