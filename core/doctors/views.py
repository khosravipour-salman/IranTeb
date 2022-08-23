import random
import requests


from django.shortcuts import render
from django.db.models import Q
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


from doctors.models import DoctorUser,CommentForDoctor
from doctors.serializers import CommentSerializers,TopDoctorSerializers,DoctorSpecialistSerializer,AllDoctorSerializers,DoctorDetailSerializer,DoctorReserveApointmentSerializer,DrRegisterInformationsserrializer,DoctorAddressSerializer,DoctorTellphoneSerializer,DrCompleteInfoSerilizer
from .models import DoctorSpecialist,Telephone,DoctorAddress
from patients.models import Appointment


def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class  DoctorValidatePhoneSendOTP (APIView):

    def post(self,request):
        phone_number=self.request.data['phone_number']
        if not phone_number:
            return Response({"msg":"phone number is requierd'"},status=status.HTTP_400_BAD_REQUEST)
        try:
            dr_user=DoctorUser.objects.get(phone_number=phone_number)
        except:
            dr_user=DoctorUser.objects.create(phone_number=phone_number)

        code = random.randint(10000, 99999)
        print('#############################')
        print(phone_number)
        print(type(phone_number))
        print(code)
        # send message (sms or email)
        # cache
        cache.set(str(phone_number), code, 2*60 )
        cached_code=cache.get(str(phone_number))
        print(cached_code)

        api_key='5141626263533245386B337871415745785856684D5667637573375459306134574C6B47315634437676383D'
        phone_number2='0'+phone_number[2:]
        print()
        print(phone_number2)
        url='https://api.kavenegar.com/v1/%s/sms/send.json'%{api_key}
        data={"receptor":"09395377024","text":str(code)}
        r=requests.post(url,data=data)

        return Response({"msg":"code sent successfully"},status=status.HTTP_200_OK)



class DrVerifyOTP(APIView):

    def post(self,request):
        phone_number = self.request.data['phone_number']
        dr_user=DoctorUser.objects.get(phone_number=phone_number)
        code = int(self.request.data['code'])
        cached_code=cache.get(str(phone_number))
        print(code)
        print(type(code))
        print(cached_code)
        print(type(cached_code))
        if code != cached_code:
            return Response({"msg":"code not matched"},status=status.HTTP_403_FORBIDDEN)
        token = get_tokens_for_user(dr_user)
        return Response({'token':token, 'msg':'Successful'}, status=status.HTTP_201_CREATED)



class DrCompleteInfo(APIView):
    # def post(self,request):
        # serializrer=DrCompleteInfoSerilizer(data=request.data)
        # if serializrer.is_valid():
            # return Response(serializrer.data,status=status.HTTP_201_CREATED)
        # return Response (serializrer.errors,status=status.HTTP_400_BAD_REQUEST)


        
    def put(self,request,pk):
        # p_num=self.request.data['phone_number']
        dr=DoctorUser.objects.get(id=pk)        
        serializrer=DrCompleteInfoSerilizer(dr,data=request.data)
        if serializrer.is_valid():
            return Response(serializrer.data,status=status.HTTP_201_CREATED)
        return Response (serializrer.errors,status=status.HTTP_400_BAD_REQUEST)


class NumActiveDoctor(APIView):

    def get(self,request):
        query=DoctorUser.objects.all().count()
        return Response({"num_active_doctor":query},status=status.HTTP_200_OK)


class RecentComment(APIView):

    def get(self,request):
        
        query=CommentForDoctor.objects.all().order_by('-rating','create_time').order_by('?')[:10]
        serializer=CommentSerializers(query,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)




class All_Specialist(APIView):
    def get(self,request):
        query=DoctorSpecialist.objects.all()
        serializer=DoctorSpecialistSerializer(query,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)



class TopDoctors(APIView):

    def get (self,request):
        query=sorted(DoctorUser.objects.all(), key=lambda a: a.rate,reverse=True)[:10]
        serializer=TopDoctorSerializers(query,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)



class DoctorsList(APIView):
    def get (self,request):
        query=sorted(DoctorUser.objects.all(), key=lambda a: a.rate,reverse=True)
        serializer=AllDoctorSerializers(query,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class DoctorDetail(APIView):
    def get(self,request,pk):
        query=DoctorUser.objects.get(id=pk)
        serializer=DoctorDetailSerializer(query)
        return Response(serializer.data,status=status.HTTP_200_OK) 



class CommentForOneDoctor(APIView):

    def get(self,request,pk):
        
        query=CommentForDoctor.objects.filter(id=pk).order_by('-rating','create_time').order_by('?')
        serializer=CommentSerializers(query,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK) 

    def post(self,request):
        serializer=CommentSerializers(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class DoctorAdvanceSearch(APIView):
    def post(self, request):
        data=self.request.data
        query=DoctorUser.objects.all()
        print(data)
        print('####################################')
        try:
            doctor_name=data['doctor_name']
            query=query.filter(full_name=doctor_name)
        except:
            pass

        try:
            specialist=data['specialist']
            query=query.filter(doctor_specilist__specialist=specialist)
        except:
            pass

        try:
            city=data['city']
            query=query.filter(city=city)
        except:
            pass

        try:
            gender=data['gender']
            query=query.filter(gender=gender)
        except:
            pass
        
        serializer=AllDoctorSerializers(query,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

        

class DoctorReserveApointment(APIView):
    def get(self,request,pk):
        dra=Appointment.objects.filter(doctor__id=pk,status_reservation='reserve')
        serializer=DoctorReserveApointmentSerializer(dra,many=True)
        return Response (serializer.data,status=status.HTTP_200_OK)



class DrRegisterInformations(APIView):
    def get(self,request,pk):
        drinfo=DoctorUser.objects.get(id=pk)
        serializer=DrRegisterInformationsserrializer(drinfo)
        return Response(serializer.data,status=status.HTTP_200_OK)



class DoctorAddressInfo(APIView):
    def get(self,request,pk):
        a=DoctorUser.objects.get(id=pk)
        dr_address=a.doctor_address
        # serializer=DoctorAddressSerializer(dr_address)
        return Response({'address':dr_address},status=status.HTTP_200_OK)

    def put(self,request,pk):
        dr_address=DoctorAddress.objects.get(doctor__id=pk)
        serializer=DoctorAddressSerializer(dr_address,data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)    
        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class DoctorTellphone(APIView):
    def get(self,request,dr_pk):
        t=DoctorUser.objects.get(id=dr_pk)
        dr_tell=t.doctor_telephone
        serializer=DoctorTellphoneSerializer(dr_tell)
        return Response(serializer.data,status=status.HTTP_200_OK)

    
    # def post(self,request,pk):
        # serializer=DoctorTellphoneSerializer(data=request.data)
        # t=Telephone.objects.create(doctor__id=pk)


    def Put(self,request,dr_pk,t_pk):
        t=Telephone.objects.filter(doctor__id=dr_pk,id=t_pk)
        serializer=DoctorTellphoneSerializer(t,data=request.data)
        if serializer.is_valid():
                return Response(serializer.data)    
        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)



