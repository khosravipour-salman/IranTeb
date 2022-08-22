from django.contrib import admin
from patients.models import (
    Patient, 
    Wallet, 
    Appointment, 
) 

admin.site.register(Patient)
admin.site.register(Wallet)
admin.site.register(Appointment)
