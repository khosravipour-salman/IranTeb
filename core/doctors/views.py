import imp
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from doctors.models import DoctorUser,CommentForDoctor
from doctors.serializers import CommentSerializers,TopDoctorSerializers


class NumActiveDoctor(APIView):

    def get(self,request):
        query=DoctorUser.objects.all().count()
        return Response({"num_active_doctor":query},status=status.HTTP_200_OK)


class RecentComment(APIView):

    def get(self,request):
        
        query=CommentForDoctor.objects.all().order_by('-rating','create_time').order_by('?')[:10]
        serializer=CommentSerializers(query,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)




class TopDoctors(APIView):

    def get (self,request):
        query=sorted(DoctorUser.objects.all(), key=lambda a: a.rate['rating__avg'],reverse=True)[:10]
        
        serializer=TopDoctorSerializers(query,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

