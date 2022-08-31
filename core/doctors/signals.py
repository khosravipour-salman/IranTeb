from django.db.models.signals import post_save
from django.dispatch import receiver
from doctors.models import DoctorUser
from patients.models import Appointment

@receiver(post_save,sender=DoctorUser)
def create_first_obj_appointment(sender,instance,created,**kwargs):
    if created:
        Appointment.objects.create( doctor = instance )
        return True
