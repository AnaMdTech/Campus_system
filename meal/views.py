from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from students.models import Student
from .models import MealRecord

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
        print(f"Found student: {student.get_full_name()} with ID: {student.student_id}") # Debugging
    except Student.DoesNotExist:
        messages.error(request, "Student not found for the scanned QR code.")
        print(f"Student with ID {qr_identifier} not found.") # Debugging
        return redirect('meal:scan_simulator')

    now = timezone.now()
    current_hour = now.hour
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
        # Cafeteria is not currently open
        previous_meal = None
        next_meal = None

        if current_hour < breakfast_start:
            next_meal = "Breakfast"
        elif breakfast_end <= current_hour < lunch_start:
            previous_meal = "Breakfast"
            next_meal = "Lunch"
        elif lunch_end <= current_hour < dinner_start:
            previous_meal = "Lunch"
            next_meal = "Dinner"
        elif dinner_end <= current_hour:
            previous_meal = "Dinner"
        else:
            # This case shouldn't ideally happen if the conditions are exhaustive
            pass

        message = "The cafeteria is currently closed."
        if previous_meal:
            message += f" {previous_meal} service has ended."
        if next_meal:
            message += f" {next_meal} service will begin at {getattr(globals(), f'{next_meal.lower()}_start')}:00."
        else:
            message += " Please check the serving schedule."

        messages.error(request, message)
        return redirect('meal:scan_simulator')

    today = now.date()
    existing_record = MealRecord.objects.filter(student=student, date=today, meal_type=meal_type).first()

    if existing_record:
        messages.error(request, f"{student.get_full_name()} has already recorded {existing_record.get_meal_type_display()} today.")
        print(f"{student.get_full_name()} already ate {existing_record.get_meal_type_display()} today.") # Debugging
    else:
        meal_record = MealRecord.objects.create(student=student, timestamp=now, meal_type=meal_type)
        messages.success(request, f"{student.get_full_name()} successfully recorded for {meal_record.get_meal_type_display()} today.")
        print(f"Meal recorded for {student.get_full_name()} - {meal_record.get_meal_type_display()}") # Debugging

    return redirect('meal:scan_simulator')