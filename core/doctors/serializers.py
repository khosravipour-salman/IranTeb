from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from doctors.models import CommentForDoctor,DoctorUser,Telephone
from .models import DoctorSpecialist

class CommentSerializers(serializers.ModelSerializer):

    class Meta:
        model=CommentForDoctor
        fields='__all__'


class TopDoctorSerializers(serializers.ModelSerializer):
    class Meta:
        model=DoctorUser
        fields=('full_name','doctor_specilist','rate','experience_years',)


class DoctorSpecialistSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=DoctorSpecialist
        fields='__all__'



class AllDoctorSerializers(serializers.ModelSerializer):
    doctor_specilist=DoctorSpecialistSerializer()
    class Meta:
        model=DoctorUser
        fields=('full_name','doctor_specilist','rate','all_patients_reserved','experience_years','gender','city')

# class TelephoneSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Telephone
#         fields='__all__'


class DoctorDetailSerializer(serializers.ModelSerializer):
    # doctor_telephone=TelephoneSerializer()
    class Meta:
        model=DoctorUser
        fields=('full_name','doctor_specilist','rate','all_patients_reserved','experience_years','gender','city','registeration_date','adress','doctor_telephone','work_day')