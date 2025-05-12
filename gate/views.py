from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from students.models import Student, Belonging

def gate_scan_simulator(request):
    if request.method == 'POST':
        qr_identifier = request.POST.get('qr_identifier')
        direction = request.POST.get('direction')

        if not qr_identifier:
            messages.error(request, "QR identifier is missing.")
            return redirect(reverse('gate:scan_simulator'))

        if not direction:
            messages.error(request, "Please select a direction.")
            return redirect(reverse('gate:scan_simulator'))

        try:
            student = Student.objects.get(student_id=qr_identifier)
            request.session['current_student_id'] = student.id  # Store student ID in session
        except Student.DoesNotExist:
            messages.error(request, f"No student found with QR identifier: {qr_identifier}")
            return redirect(reverse('gate:scan_simulator'))

        if direction == 'IN':
            messages.success(request, f"{student.get_full_name()} - Entry successful.")
            return redirect(reverse('gate:scan_simulator'))
        elif direction == 'OUT':
            # Redirect to a new view to display belongings and verification button
            return redirect(reverse('gate:verify_exit', kwargs={'student_id': student.id}))
        else:
            messages.error(request, "Invalid direction selected.")
            return redirect(reverse('gate:scan_simulator'))

    return render(request, 'gate/scan_simulator.html')

def verify_exit(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    belongings = Belonging.objects.filter(student=student)
    context = {
        'student': student,
        'belongings': belongings,
    }
    return render(request, 'gate/verify_exit.html', context)

def process_exit(request, student_id):
    if request.method == 'POST':
        # Here you would typically log the exit event.
        messages.success(request, f"{get_object_or_404(Student, pk=student_id).get_full_name()} - Exit verified.")
        return redirect(reverse('gate:scan_simulator'))
    else:
        return redirect(reverse('gate:verify_exit', kwargs={'student_id': student_id}))