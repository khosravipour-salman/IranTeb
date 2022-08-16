from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from patients.models import Patient

class NumActiveUser(APIView):
    def get(self,request):
        query=Patient.objects.all().count()
        return Response({"num_active_user":query},status=status.HTTP_200_OK)
