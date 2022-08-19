from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import CommentForDoctor,DoctorUser,Telephone,DoctorCity
from .models import DoctorCity, DoctorSpecialist




class TopDoctorSerializers(serializers.ModelSerializer):
    class Meta:
        model=DoctorUser
        fields=('full_name','doctor_specialist','rate','experience_years',)


class DoctorSpecialistSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=DoctorSpecialist
        fields='__all__'


class DoctorCitySerializer(serializers.ModelSerializer):

    class Meta:
        model=DoctorCity
        fields=('parent','city',)


class AllDoctorSerializers(serializers.ModelSerializer):
    doctor_specilist=DoctorSpecialistSerializer()
    city=DoctorCitySerializer()
    class Meta:
        model=DoctorUser
        fields=('full_name','doctor_specialist','rate','all_patients_reserved','experience_years','gender','city')

# class TelephoneSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Telephone
#         fields='__all__'


class DoctorDetailSerializer(serializers.ModelSerializer):
    city=DoctorCitySerializer()

    doctor_specialist=serializers.SerializerMethodField('get_doctor_specialist')

    def get_doctor_specialist(self,obj):
        return {'parent':obj.doctor_specialist.parent,'specialist':obj.doctor_specialist.specialist}

    class Meta:
        model=DoctorUser
        fields=('full_name','doctor_specialist','rate','all_patients_reserved','experience_years','gender','city','registeration_date','doctor_address','doctor_telephone','work_day','user_shifts')


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model=CommentForDoctor
        fields='__all__'