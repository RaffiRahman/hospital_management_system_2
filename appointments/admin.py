from django.contrib import admin
from .models import Doctor, Slot, Appointment

# Register your models here.

admin.site.register(Doctor)

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'start_time', 'is_booked')
    list_filter = ('doctor', 'date', 'is_booked')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'slot', 'status')
    list_filter = ('status', 'doctor')
