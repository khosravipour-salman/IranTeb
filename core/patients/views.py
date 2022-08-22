from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from doctors.models import DoctorUser

from .serializers import PatientInfoSerializer, ReservedSerializer,WalletSerializer
from .models import Appointment,Wallet
from django.db.models import Avg
from doctors.models import CommentForDoctor

from patients.models import Patient

from kavenegar import *



def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

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


class ReservedAppointment(APIView):
    def get(self,request,pk):
        query=Appointment.objects.filter(id=pk,status_reservation='reserved')
        serializer=ReservedSerializer(query,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class MyWallet(APIView):
    def get(self,request,pk):
        query=Wallet.objects.get(user__id=pk)
        serializer=WalletSerializer(query)
        return Response(serializer.data,status=status.HTTP_200_OK)


class PatientInfo(APIView):
    def put(self,request,pk):
        query=Patient.objects.get(pk=pk)
        serializer=PatientInfoSerializer(query)
        return Response(serializer.data,status=status.HTTP_200_OK)
    # def post(self,request):
    #     serializer=PatientInfoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data,status=status.HTTP_201_CREATED)
    #     return Response(status=status.HTTP_400_BAD_REQUEST)

    # def get(self,request,pk):
    #     query=Patient.objects.get(id=pk)
    #     serializer=PatientInfoSerializer(query)
    #     return Response(serializer.data,status=status.HTTP_200_OK)
        
















import uuid
import random

from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User


class RegisterView(APIView):

    def post(self, request):
        phone_number =self.request.data['phone_number']

        if not phone_number:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            user = User.objects.create_user(phone_number=phone_number)
        code = random.randint(10000, 99999)
        cache.set(str(phone_number), code, 2 * 60)

        try:
            api = KavenegarAPI('462F57306A68694E797377433255374D5A593871516B7647567A5862387079616F676C6B462F59683165413D', timeout=20)
            params = {
                'sender': '',#optional
                'receptor': '09395377024',#multiple mobile number, split by comma
                'message': code,
        } 
            response = api.sms_send(params)
            print(response)
        except APIException as e: 
            print(e)
        except HTTPException as e: 
            print(e)
        return Response({'code': code})


class GetTokenView(APIView):
    def post(self, request):
        phone_number =self.request.data['phone_number']
        patient_user=Patient.objects.get(phone_number=phone_number)
        code =int(self.request.data(['code']))
        cached_code = cache.get(str(phone_number))

        if code != cached_code:
            return Response({"msg":"code not found"},status=status.HTTP_403_FORBIDDEN)
        token = get_tokens_for_user(patient_user)
        return Response({'token': token,'msg':'successful'},status=status.HTTP_201_CREATED)





from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404


def go_to_gateway_view(request):
    # خواندن مبلغ از هر جایی که مد نظر است
    amount = 5000
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = '+989112221234'  # اختیاری
    factory = bankfactories.BankFactory()
    bank = factory.auto_create() # or factory.create(bank_models.BankType.BMI) or set identifier
    bank.set_request(request)
    bank.set_amount(amount)
    # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
    bank.set_client_callback_url('/callback-gateway/')
    bank.set_mobile_number(user_mobile_number)  # اختیاری
    
        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید. 
    bank_record = bank.ready()
        # هدایت کاربر به درگاه بانک
    return bank.redirect_gateway()



def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        return HttpResponse("پرداخت با موفقیت انجام شد.")

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")
  


