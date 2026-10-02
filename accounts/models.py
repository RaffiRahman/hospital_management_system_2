from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)

    @property
    def is_profile_complete(self):
        return bool(
            self.phone and
            self.date_of_birth and
            self.address
        )

    def __str__(self):
        return self.user.get_full_name() or self.user.username
