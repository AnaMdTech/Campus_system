from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from students.models import Student, Belonging
from .models import GateLocation

def is_gate_staff(user):
    return user.groups.filter(name='Gate Staff').exists()

def gate_staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and is_gate_staff(user):
            login(request, user)
            return redirect('gate:start_scanner')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'gate/staff_login.html')

def gate_staff_logout(request):
    logout(request)
    return redirect('gate:staff_login')

@login_required
@user_passes_test(is_gate_staff)
def start_scanner(request):
    if request.method == 'POST':
        gate_id = request.POST.get('gate_location')
        if not gate_id:
            messages.error(request, "Please select a gate location.")
            return redirect('gate:start_scanner')

        # Fetch the gate by ID
        gate = get_object_or_404(GateLocation, id=gate_id)

        # Store gate ID or name in session (optional, for future requests)
        request.session['selected_gate_name'] = gate.name

        # You can now pass it to the template or use it however you want
        return render(request, 'gate/scan_simulator.html', {
            'selected_gate': gate
        })

    # On GET request, show the gate selector
    gate_locations = GateLocation.objects.filter(is_active=True)
    return render(request, 'gate/start_scanner.html', {'gate_locations': gate_locations})

@login_required
@user_passes_test(is_gate_staff)
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
            messages.success(request, f"{student.get_full_name()} - Entry successful. Welcome to {request.session.get('selected_gate_name')}!")
            return redirect(reverse('gate:scan_simulator'))
        elif direction == 'OUT':
            # Redirect to a new view to display belongings and verification button
            return redirect(reverse('gate:verify_exit', kwargs={'student_id': student.id}))
        else:
            messages.error(request, "Invalid direction selected.")
            return redirect(reverse('gate:scan_simulator'))

    return render(request, 'gate/scan_simulator.html')

@login_required
@user_passes_test(is_gate_staff)
def verify_exit(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    belongings = Belonging.objects.filter(student=student)
    context = {
        'student': student,
        'belongings': belongings,
    }
    return render(request, 'gate/verify_exit.html', context)

@login_required
@user_passes_test(is_gate_staff)
def process_exit(request, student_id):
    if request.method == 'POST':
        # Here you would typically log the exit event.
        messages.success(request, f"{get_object_or_404(Student, pk=student_id).get_full_name()} - Exit verified. at {request.session.get('selected_gate_name')}!")
        return redirect(reverse('gate:scan_simulator'))
    else:
        return redirect(reverse('gate:verify_exit', kwargs={'student_id': student_id}))