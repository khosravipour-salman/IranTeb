import datetime
from django.db import models
from django.db.models import Avg,Sum
import datetime
from django.core import validators
from django.utils import timezone
from random import random
from patients.models import User,UserManager,Appointment



class DoctorUser(User):
    time_choices=(
        ("15", "15 mine" ),
        ("20", "20 mine" ),
        ("25", "25 mine" ),
        ("30", "30 mine" ),
        ("45", "45 mine"),
        ("50", "50 mine"),
        ("60", "60 mine" ),
        ("80", "80 mine" ),
        ("90", "90 mine" ),
        ("100", "100 mine" ),
        ("120" ,"120 mine" ),
    )
    gender_choice=(
        ('male','male'),
        ('female','female'),
    )
    # city_choice=(
        # ('Tehran','Tehran'),
        # ('Esfahan','Esfahan'),
        # ('Shiraz','Shiraz'),
        # ('Tabriz','Tabriz'),
        # ('Gilan','Gilan'),
        # ('Khoozestan','Khoozestan'),
    # )

    full_name=models.CharField(max_length=80)
    medical_system_code=models.IntegerField(null=True,blank=True)
    adress=models.TextField(null=True,blank=True)
    registeration_date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    bio=models.TextField(null=True,blank=True)
    cost_visit=models.PositiveBigIntegerField(default=10000,null=True,blank=True)
    visit_time=models.CharField(max_length=10,choices=time_choices,null=True,blank=True)
    doctor_specilist=models.OneToOneField("doctors.DoctorSpecialist",on_delete=models.CASCADE,null=True,blank=True)
    gender=models.CharField(choices=gender_choice,max_length=10,null=True,blank=True)
    city=models.ForeignKey('doctors.DoctorCity',on_delete=models.CASCADE,null=True,blank=True)
# from doctors.models import DoctorUser
# d = DoctorUser.objects.all()[0] 
# d.get_user_shifts()

# vt --> int
# 16 ta 8 --> total 8 
# 8 * 60 --> 4800 minute
# 4800 / vt --> chndta visit_time
# foreach --> vt + st 8:45, 
    
    @property
    def rate(self):
        t=self.commentfordoctor_set.all().aggregate(Avg('rating'))
        r=t["rating__avg"]
        return r


    @property
    def all_patients_reserved(self):
        c=self.appointment_set.filter(status_reservation='reserved').count()
        return c


    @property
    def experience_years(self):
        a=self.doctorexperoence_set.all().aggregate(Sum('years_experience'))
        e=a['years_experience__sum']
        return e


    @property
    def doctor_telephone(self):
        t=self.telephone_set.all()
        l=[]
        for tel in t:
            tn=tel.telephone_number
            l.append(tn)

        return l

# 
    @property
    def work_day(self):
        d=self.weekdays_set.all()
        l=[]
        for dy in d:
            day=dy.day
            l.append(day)
        j=[]
        hours=self.doctorshift_set.all()
        for i in hours:
            h1=i.start_time
            h2=i.end_time
            k=[h1,h2]
            j.append(k)

        
            
        return l , j
# 
    # @property
    # def doctor_city(self):
        # c1=self.city.parent
        # c2=self.city.city
        # 
# 
        # return c2
    @property
    def user_shifts(self):
        l = []
        for shift in self.doctorshift_set.all():
            j=[]
            et, st= shift.end_time, shift.start_time
            vt = datetime.timedelta(minutes=int(self.visit_time))
            while True:
                e=datetime.datetime.combine(datetime.date.today(),et)
                s=datetime.datetime.combine(datetime.date.today(),st)
                a=((s).time(),(s+vt).time())
                t=(s+vt).strftime('%H:%M:%S')
                st=datetime.datetime.strptime(str(t), '%H:%M:%S').time()
                j.append(a)
                if st==et or st>et:
                    if j[-1][-1]>et:
                        j.pop(-1)
                    l.append(j)
                
                    break
        return l
        






class DoctorSpecialist(models.Model):
    parent=models.ForeignKey("self",on_delete=models.CASCADE,null=True,blank=True)
    specialist=models.CharField(max_length=100)

    def __str__(self):
        return self.specialist



class Telephone(models.Model):
    doctor=models.ForeignKey("doctors.DoctorUser",on_delete=models.CASCADE)
    telephone_number=models.PositiveBigIntegerField(unique=True)

    def __str__(self):
        return f'{self.telephone_number} for {self.doctor}'



class DoctorCity(models.Model):
    parent=models.ForeignKey("self",on_delete=models.CASCADE,null=True,blank=True)
    city=models.CharField(max_length=50)
    def __str__(self):
        return f'{self.city} in {self.parent}'



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
    user=models.ForeignKey("patients.patient",on_delete=models.CASCADE)
    create_time=models.DateTimeField(auto_now_add=True)
    rating=models.CharField(choices=rate_choices,max_length=5)

    def __str__(self):
        return f'{self.user} for  {self.doctor}'



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
    doctor=models.ManyToManyField("doctors.DoctorUser",blank=True)

    def __str__(self):
        return f'{self.day}-{self.doctor}'



class DoctorShift(models.Model):
    HOUR_CHOICES = [(datetime.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]
    start_time=models.TimeField(choices=HOUR_CHOICES)
    end_time=models.TimeField(choices=HOUR_CHOICES)
    doctor=models.ForeignKey("doctors.DoctorUser",on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.start_time}-{self.end_time} for {self.doctor.full_name}'



class DoctorExperoence(models.Model):
    years_experience=models.IntegerField()
    loction=models.TextField()
    doctor=models.ForeignKey("doctors.DoctorUser",on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.doctor} work {self.years_experience} years in {self.loction}'
