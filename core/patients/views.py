from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment
from django.db.models import Avg
from doctors.models import CommentForDoctor


from patients.models import Patient

class NumActiveUser(APIView):
    def get(self,request):
        query=Patient.objects.all().count()
        return Response({"num_active_user":query},status=status.HTTP_200_OK)


class NumSuccessfulReseced(APIView):
    def get(self,request):
        query=Appointment.objects.filter(status_reservation='reserved').count()
        return Response({"num_success_reserved":query},status=status.HTTP_200_OK)


class UserSatisfy(APIView):
    def get(self,request):
        query=CommentForDoctor.objects.all().aggregate(Avg('rating'))
        a=f" {query['rating__avg']*20} % "       
        return Response({"percent_satisfy":a},status=status.HTTP_200_OK)
