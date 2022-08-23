from rest_framework import serializers
from patients.models import Appointment


class ReserveAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Appointment
        fields=('doctor_name','reservetion_code','doctor_address','doctor_telephones','start_visit_time','end_visit_time','status_reservation','visit_day','payment')


    # 'start_visit_time','end_visit_time','day','status_reservation'


class MyDoctorsSerializer(serializers.ModelSerializer):
    doctor=serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='doctor:doctor-detail'
    )
    class Meta:
        model=Appointment
        fields=('doctor_name','doctor',)


class DoctorFreeAppointmentSerializer(serializers.ModelSerializer):
    def get_doctor(self,obj):
        return obj.doctor.full_name
    
    doctor=serializers.SerializerMethodField('get_doctor')
    class Meta:
        model=Appointment
        fields=('doctor','start_visit_time','end_visit_time','date_of_visit')