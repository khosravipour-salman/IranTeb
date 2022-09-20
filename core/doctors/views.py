import imp
from django.shortcuts import render
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from doctors.models import DoctorUser, CommentForDoctor
from doctors.serializers import CommentSerializers, TopDoctorSerializers, DoctorSpecialistSerializer, AllDoctorSerializers, DoctorDetailSerializer, CancelSerializer
from .models import DoctorSpecialist
from patients.models import Appointment
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class NumActiveDoctor(APIView):
    def get(self, request):
        query = DoctorUser.objects.all().count()
        return Response({"num_active_doctor": query}, status=status.HTTP_200_OK)


class RecentComment(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):

        query = CommentForDoctor.objects.all().order_by(
            '-rating', 'create_time').order_by('?')[:10]
        serializer = CommentSerializers(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class All_Specialist(APIView):
    def get(self, request):
        query = DoctorSpecialist.objects.all()
        serializer = DoctorSpecialistSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TopDoctors(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = sorted(DoctorUser.objects.all(),
                       key=lambda a: a.rate, reverse=True)[:10]
        serializer = TopDoctorSerializers(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorsList(APIView):
    def get(self, request):
        query = sorted(DoctorUser.objects.all(),
                       key=lambda a: a.rate, reverse=True)
        serializer = AllDoctorSerializers(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        query = DoctorUser.objects.get(id=pk)
        serializer = DoctorDetailSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentForOneDoctor(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        query = CommentForDoctor.objects.filter(id=pk).order_by(
            '-rating', 'create_time').order_by('?')
        serializer = CommentSerializers(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CommentSerializers(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = CommentForDoctor.objects.get(id=pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DoctorAdvanceSearch(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = self.request.data
        query = DoctorUser.objects.all()
        try:
            doctor_name = data['doctor_name']
            query = query.filter(full_name=doctor_name)
        except:
            pass

        try:
            specialist = data['specialist']
            query = query.filter(doctor_specilist__specialist=specialist)
        except:
            pass

        try:
            city = data['city']
            query = query.filter(city=city)
        except:
            pass

        try:
            gender = data['gender']
            query = query.filter(gender=gender)
        except:
            pass

        serializer = AllDoctorSerializers(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CancelReservation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        query = Appointment.objects.filter(
            doctor__id=pk, status_reservation='cancel')
        serializer = CancelSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
