from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PatientForm, RegisterForm
from .models import Patient


# Create your views here.

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        Patient.objects.create(user=user)
        return redirect('login')

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def edit_profile(request):
    patient = request.user.patient
    form = PatientForm(request.POST or None, instance=patient)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Details saved.")
        return redirect('request_appointment')
    return render(request, 'accounts/edit_profile.html', {'form': form})
