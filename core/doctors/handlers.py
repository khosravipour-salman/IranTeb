# from django.db.models.signals import pre_save
# from django.dispatch import receiver    
# 
# from doctors.models import DoctorUser
# from patients.models import Appointment
# 
# @receiver(pre_save, sender=DoctorUser)
# def my_handler(sender,**kwargs):
    # if sender.pk is None:  # create
        # sender.model = Appointment.objects.create( doctor__username = sender.username )