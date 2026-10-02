from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Patient

# Create your views here.

def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        Patient.objects.create(user=user)
        return redirect('login')

    return render(request, 'accounts/register.html', {'form': form})
