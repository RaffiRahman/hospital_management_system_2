from accounts.decorators import patient_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import transaction
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from .models import Slot, Appointment
from accounts.models import Patient


# Create your views here.

@login_required
def my_appointments(request):
    patient = request.user.patient
    appointments = (
        patient.appointments
        .select_related('doctor__user', 'slot')
        .order_by('-slot__date', '-slot__start_time')
    )
    return render(request, 'appointments/my_appointments.html', {
        'appointments': appointments,
    })

@assistant_required
def assistant_dashboard(request):
    appointments = (
        Appointment.objects
        .select_related('patient__user', 'doctor__user', 'slot')
        .order_by('-created_at')
    )

    context = {
        'pending': appointments.filter(status=Appointment.Status.REQUESTED),
        'confirmed': appointments.filter(status=Appointment.Status.CONFIRMED),
        'cancelled': appointments.filter(status=Appointment.Status.CANCELLED),
    }
    return render(request, 'appointments/assistant_dashboard.html', context)

@login_required
def request_appointment(request):
    patient = request.user.patient

    if not patient.is_profile_complete:
        messages.warning(request, "Please complete your profile before requesting an appointment.")
        return redirect('edit_profile')

    slots = Slot.objects.filter(is_booked=False).select_related('doctor__user')

    if request.method == 'POST':
        slot = slots.get(pk=request.POST['slot'])
        Appointment.objects.create(
            patient=patient,
            doctor=slot.doctor,
            slot=slot,
            reason=request.POST.get('reason', ''),
        )
        messages.success(request, "Request submitted successfully. Please wait for confirmation.")
        return redirect('my_appointments')

    return render(request, 'appointments/request.html', {'slots': slots})

@assistant_required
def confirm_appointment(request, pk):
    with transaction.atomic():
        appt = get_object_or_404(
            Appointment.objects.select_for_update().select_related('slot', 'patient__user'),
            pk=pk
        )
        slot= appt.slot
        if slot.is_booked:
            messages.error(request, "This slot is not available.")
            return redirect('assistant_dashboard')

        slot.is_booked = True
        slot.save()
        appt.status = Appointment.Status.CONFIRMED
        appt.save()

    send_mail(
        subject="Appointment Confirmed",
        message= f"Your appointment with {appt.doctor} on {slot.date} at {slot.start_time} has been confirmed.",
        from_email= None,
        recipient_list= [appt.patient.user.email]
    )
    messages.success(request, "Appointment confirmed and patient informed.")
    return redirect('assistant_dashboard')

@assistant_required
def cancel_appointment(request, pk):
    with transaction.atomic():
        appt = get_object_or_404(
            Appointment.objects.select_for_update(), pk=pk
        )
        appt.status = Appointment.Status.CANCELLED
        appt.save()
        appt.slot.is_booked = False
        appt.slot.save()

    send_mail(
        "Appointment Cancelled",
        f"Your appointment on {appt.slot.date} has been cancelled.",
        None,
        [appt.patient.user.email]
    )
    return redirect('assistant_dashboard')





