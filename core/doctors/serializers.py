from dataclasses import fields
from rest_framework import serializers
from doctors.models import CommentForDoctor,DoctorUser
from .models import DoctorSpecialist

class CommentSerializers(serializers.ModelSerializer):

    class Meta:
        model=CommentForDoctor
        fields='__all__'


class TopDoctorSerializers(serializers.ModelSerializer):
    class Meta:
        model=DoctorUser
        fields=('full_name','doctor_specilist','rate',)


class DoctorSpecialistSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=DoctorSpecialist
        fields='__all__'