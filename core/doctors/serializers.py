from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import CommentForDoctor,DoctorUser,Telephone,DoctorCity,DoctorAddress
from .models import DoctorCity, DoctorSpecialist
from patients.models import Appointment



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

    doctor_specialist=serializers.SerializerMethodField('get_doctor_specialist',read_only=True)

    def get_doctor_specialist(self,obj):
        # return str ({"specialist":obj.doctor_specialist.parent,
        # " high specialist'":obj.doctor_specialist.specialist})
        a={"specialist":obj.doctor_specialist.parent,
        " high specialist'":obj.doctor_specialist.specialist}
        
        return str(a)
        

    class Meta:
        model=DoctorUser
        fields=('full_name','doctor_specialist','rate','all_patients_reserved','experience_years','gender','city','registeration_date','doctor_address','doctor_telephone','work_day','user_shifts')


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model=CommentForDoctor
        fields='__all__'



class DoctorReserveApointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Appointment
        fields=('status_reservation','patient_name','patient_phone_number','patient_insurance',)


class DrRegisterInformationsserrializer(serializers.ModelSerializer):
    class Meta:
        model=DoctorUser
        fields=('registeration_date','phone_number')


class DoctorTellphoneSerializer(serializers.ModelSerializer):
    def get_doctor(self,obj):
        return obj.doctor.full_name

    doctor=serializers.SerializerMethodField('get_doctor')
    class Meta:
        model=Telephone
        fields='__all__'


class DoctorAddressSerializer(serializers.ModelSerializer):
    def get_doctor(self,obj):
        return obj.doctor.full_name

    doctor=serializers.SerializerMethodField('get_doctor')

    class Meta:
        model=DoctorAddress
        fields='__all__'


class DrCompleteInfoSerilizer(serializers.ModelSerializer):
    class Meta:
        model=DoctorUser
        fields=('full_name','medical_system_code','dr_specialist','doctor_telephone','doctor_address')