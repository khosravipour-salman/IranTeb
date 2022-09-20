from dataclasses import fields
from rest_framework import serializers
from .models import Appointment, Patient, Wallet


class ReservedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('name_doctor', 'status_reservation', 'start_visit_time', 'end_visit_time',
                  'day_week', 'reservetion_code', 'doctor_telephones', 'doctor_address')


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('user_name', 'wallet_balance')


class PatientInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('full_name', 'national_code', 'Insurance', 'phone_number')
