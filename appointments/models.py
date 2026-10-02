from django.db import models
from django.contrib.auth.models import User
from accounts.models import Patient

# Create your models here.

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} ({self.specialization})"


class Slot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('doctor', 'date', 'start_time')
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.doctor} - {self.date} {self.start_time}"


class Appointment(models.Model):
    class Status(models.TextChoices):
        REQUESTED = 'REQUESTED', 'Requested'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.PROTECT)
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.REQUESTED)
    creates_at = models.DateTimeField(auto_now_add=True)
    updates_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment for {self.patient} with {self.doctor} [{self.status}]"