import random
import requests
from datetime import timedelta
import redis

from django.shortcuts import render
from django.db.models import Q
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


from doctors.models import DoctorUser, CommentForDoctor, DoctorShift
from doctors.serializers import (CommentSerializers, TopDoctorSerializers,
                                 DoctorSpecialistSerializer, AllDoctorSerializers, DoctorDetailSerializer,
                                 DoctorReserveApointmentSerializer, DrRegisterInformationsserrializer,
                                 DrCompleteInfoSerilizer, RetriveDrShiftTimeSerializer, CreateDrShiftTimeSerializer,
                                 DoctorAddressSerilizer, RetriveDoctorTellePhoneSerilizer, CreateDoctorTellePhoneSerilizer,
                                 DoctorVisitTimeSerializer, DoctorWorkDaysSrializer, LogOutSerializer)
from .models import DoctorSpecialist, Telephone, DoctorAddress, WeekDays
from patients.models import Appointment


r = redis.Redis(host='localhost', port=6379, db=0)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class DoctorLoginSendOTp(APIView):
    def post(self, request):
        phone_number = self.request.data['phone_number']
        if not phone_number:
            return Response({"msg": "phone number is requierd'"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            dr_user = DoctorUser.objects.get(phone_number=phone_number)
        except:
            return Response({"msg": "you dont have any user account with this phone number please register "}, status=status.HTTP_400_BAD_REQUEST)

        code = random.randint(10000, 99999)

        r.setex(str(phone_number), timedelta(minutes=2), value=code)
        print('*****************************')
        print(r.get(str(phone_number)).decode())
        print('#############################')
        print(code)
        # cache.set(str(phone_number), code, 2*60)
        # cached_code = cache.get(str(phone_number))
        # print(cached_code)
#######################################
        # api_key = '5141626263533245386B337871415745785856684D5667637573375459306134574C6B47315634437676383D'
        # phone_number2 = '0'+phone_number[2:]
        # print()
        # print(phone_number2)
        # url = 'https://api.kavenegar.com/v1/%s/sms/send.json' % {api_key}
        # data = {"receptor": "09362815318", "text": str(code)}
        # r = requests.post(url, data=data)

        return Response({"msg": "code sent successfully"}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request, *args):
        serializer = LogOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DoctorRegisterSendOTp (APIView):

    def post(self, request):
        phone_number = self.request.data['phone_number']
        if not phone_number:
            return Response({"msg": "phone number is requierd'"}, status=status.HTTP_400_BAD_REQUEST)

        dr_user = DoctorUser.objects.create(
            phone_number=phone_number, is_active=False)

        code = random.randint(10000, 99999)
        r.setex(str(phone_number), timedelta(minutes=1), value=code)
        print('*****************************')
        print(r.get(str(phone_number)).decode())
        print('#############################')
# 
        # cache.set(str(phone_number), code, 2*60)
        # cached_code = cache.get(str(phone_number))
        # print(cached_code)

#################################################
        # api_key = '5141626263533245386B337871415745785856684D5667637573375459306134574C6B47315634437676383D'
        # phone_number2 = '0'+phone_number[2:]
        # print()
        # print(phone_number2)
        # url = 'https://api.kavenegar.com/v1/%s/sms/send.json' % {api_key}
        # data = {"receptor": "09395377024", "text": str(code)}
        # r = requests.post(url, data=data)

        return Response({"msg": "code sent successfully"}, status=status.HTTP_200_OK)


class DrVerifyOTP(APIView):

    def post(self, request):
        phone_number = self.request.data['phone_number']
        dr_user = DoctorUser.objects.get(phone_number=phone_number)
        code = self.request.data['code']
        cached_code = r.get(str(phone_number)).decode()
        # cached_code = cache.get(str(phone_number))
        if code != cached_code:
            return Response({"msg": "code not matched"}, status=status.HTTP_403_FORBIDDEN)
        token = get_tokens_for_user(dr_user)
        return Response({'token': token, 'msg': 'Successful'}, status=status.HTTP_201_CREATED)


class DrCompleteInfo(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        data = self.request.data
        p_num = data['phone_number']
        dr = DoctorUser.objects.get(phone_number=p_num)
        serializer = DrCompleteInfoSerilizer(dr, data=request.data)
        if serializer.is_valid():
            doctor_telephone = Telephone.objects.create(
                doctor=dr, telephone_number=serializer.data['doctor_telephone'])
            doctor_address = DoctorAddress.objects.create(
                doctor=dr, address=serializer.data['doctor_address'])
            serializer.save()
            dr.is_active = True
            dr.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NumActiveDoctor(APIView):

    def get(self, request):
        query = DoctorUser.objects.all().count()
        return Response({"num_active_doctor": query}, status=status.HTTP_200_OK)


class RecentComment(APIView):

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


class DoctorAdvanceSearch(APIView):
    def post(self, request):
        data = self.request.data
        query = DoctorUser.objects.all()
        print(data)
        print('####################################')
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


class DoctorReserveApointment(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        dra = Appointment.objects.filter(
            doctor__id=pk, status_reservation='reserve')
        serializer = DoctorReserveApointmentSerializer(dra, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DrRegisterInformations(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        drinfo = DoctorUser.objects.get(id=pk)
        serializer = DrRegisterInformationsserrializer(drinfo)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetriveDoctorShiftTime(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dr_pk):
        query = DoctorShift.objects.filter(doctor__id=dr_pk)
        serializer = RetriveDrShiftTimeSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateDoctorShiftTime(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, dr_pk):
        serializer = CreateDrShiftTimeSerializer(data=request.data)
        doctor_instance = DoctorUser.objects.get(id=dr_pk)
        if serializer.is_valid():
            serializer.save(doctor=doctor_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateDoctorShiftTime(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        query = DoctorShift.objects.get(id=pk)
        serializer = CreateDrShiftTimeSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteDoctorShiftTime(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        query = DoctorShift.objects.get(id=pk)
        query.delete()
        return Response({'msg': 'shift time delete'}, status=status.HTTP_204_NO_CONTENT)


class DoctorAddressInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dr_pk):
        query = DoctorAddress.objects.get(doctor__id=dr_pk)
        serializer = DoctorAddressSerilizer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, dr_pk):
        serializer = DoctorAddressSerilizer(data=request.data)
        doctor_instance = DoctorUser.objects.get(id=dr_pk)
        if serializer.is_valid():
            serializer.save(doctor=doctor_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, dr_pk):
        query = DoctorAddress.objects.get(doctor__id=dr_pk)
        serializer = DoctorAddressSerilizer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetriveDoctorTellePhone(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dr_pk):
        query = Telephone.objects.filter(doctor__id=dr_pk)
        serilizer = RetriveDoctorTellePhoneSerilizer(query, many=True)
        return Response(serilizer.data, status=status.HTTP_200_OK)


class CreateDoctorTellePhone(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, dr_pk):
        doctor_instance = DoctorUser.objects.get(id=dr_pk)
        serializer = CreateDoctorTellePhoneSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save(doctor=doctor_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateDoctorTellePhone(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        query = Telephone.objects.get(id=pk)
        serializer = CreateDoctorTellePhoneSerilizer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteDoctorTellePhone(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        query = Telephone.objects.get(id=pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DoctorVisitTime(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dr_pk):
        query = DoctorUser.objects.get(id=dr_pk)
        serializer = DoctorVisitTimeSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, dr_pk):
        query = DoctorUser.objects.get(id=dr_pk)
        serializer = DoctorVisitTimeSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorWorkDays(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dr_pk):
        query = WeekDays.objects.filter(doctor__id=dr_pk)
        serializer = DoctorWorkDaysSrializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, dr_pk):

        day = self.request.data['day']
        day_of_week = WeekDays.objects.get(day=day)
        doctor = DoctorUser.objects.get(id=dr_pk)
        day_of_week.doctor.add(doctor)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, dr_pk):
        day = self.request.data['day']
        day_of_week = WeekDays.objects.get(day=day)
        doctor = DoctorUser.objects.get(id=dr_pk)
        day_of_week.doctor.remove(doctor)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DrChangePhoneNumber(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, dr_pk):
        data = self.request.data
        new_phone_number = data['new_phone_number']
        dr_obj = DoctorUser.objects.get(id=dr_pk)
        dr_obj.phone_number = new_phone_number
        dr_obj.save()
        return Response({'msg': 'your new phone number saved'}, status=status.HTTP_202_ACCEPTED)



