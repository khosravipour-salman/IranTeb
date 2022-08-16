import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import validators
import datetime as dt
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, send_mail
from random import random
from patients.models import User,UserManager



class DoctorUser(User):
    time_choices=(
        ("15", "15 mine" ),
        ("20", "20 mine" ),
        ("30", "30 mine" ),
        ("45", "45 mine"),
        ("60", "60 mine" ),
        ("90", "90 mine" ),
        ("120" ,"120 mine" ),
    )

    full_name=models.CharField(max_length=80)
    medical_system_code=models.IntegerField(null=True,blank=True)
    adress=models.TextField(null=True,blank=True)
    registeration_date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    bio=models.TextField(null=True,blank=True)
    cost_visit=models.PositiveBigIntegerField(default=10000,null=True,blank=True)
    visit_time=models.CharField(max_length=10,choices=time_choices,null=True,blank=True)
    doctor_specilist=models.OneToOneField("doctors.DoctorSpecialist",on_delete=models.CASCADE,null=True,blank=True)
    
# from doctors.models import DoctorUser
# d = DoctorUser.objects.all()[0] 
# d.get_user_shifts()

    def get_user_shifts(self):
        for shift in self.doctorshift_set.all():
             
            et, st= shift.end_time, shift.start_time
            vt = datetime.timedelta(minutes=int(self.visit_time))
            # vt --> int
            # 16 ta 8 --> total 8 
            # 8 * 60 --> 4800 minute
            # 4800 / vt --> chndta visit_time
            # foreach --> vt + st 8:45, 

            print("#########################")
            print(vt)
            print(st, et, vt) 
            l = []
            while True:
                a=(st,st+vt)
                l.append(a)
                st=st+vt
                if st>=et:
                    break
                return 



class DoctorSpecialist(models.Model):
    parent=models.ForeignKey("self",on_delete=models.CASCADE,null=True,blank=True)
    specialist=models.CharField(max_length=100)


class Telephone(models.Model):
    doctor=models.ForeignKey("doctors.DoctorUser",on_delete=models.CASCADE)
    telephone_number=models.PositiveBigIntegerField(unique=True)


class CommentForDoctor(models.Model):

    rate_choices=(
        ("1", "1" ),
        ("2", "2" ),
        ("3", "3" ),
        ("4", "4" ),
        ("5", "5" ),
    )
    desciption=models.TextField()
    doctor=models.ForeignKey("doctors.DoctorUser",on_delete=models.CASCADE)
    user=models.OneToOneField("patients.patient",on_delete=models.CASCADE)
    create_time=models.DateTimeField(auto_now_add=True)
    rating=models.CharField(choices=rate_choices,max_length=5)


class WeekDays(models.Model):
    choice_days=(
        ("saturday", "saturday" ),
        ("sunday", "sunday" ),
        ("monday", "monday" ),
        ("tuesday", "tuesday" ),
        ("wednesday", "wednesday" ),
        ("thursday", "thursday" ),
        ("friday", "friday" ),
    )
    day=models.CharField(choices=choice_days,max_length=10)
    week_days=models.ManyToManyField("doctors.DoctorUser",null=True,blank=True)

class DoctorShift(models.Model):
    HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]
    start_time=models.TimeField(choices=HOUR_CHOICES)
    end_time=models.TimeField(choices=HOUR_CHOICES)
    doctor=models.ForeignKey("doctors.DoctorUser",on_delete=models.CASCADE)


class DoctorExperoence(models.Model):
    experoence=models.TextField()
    doctor=models.ForeignKey("doctors.DoctorUser",on_delete=models.CASCADE)


