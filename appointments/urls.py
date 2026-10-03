from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.request_appointment, name='request_appointment'),
    path('mine/', views.my_appointments, name='my_appointments'),
    path('assistant/', views.assistant_dashboard, name='assistant_dashboard'),
    path('assistant/confirm/<int:pk>/', views.confirm_appointment, name='confirm_appointment'),
    path('assistant/cancel/<int:pk>/', views.cancel_appointment, name='cancel_appointment'),
]