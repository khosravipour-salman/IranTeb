from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment
from django.db.models import Avg
from doctors.models import CommentForDoctor

from patients.serializers import ReserveAppointmentSerializer,MyDoctorsSerializer,DoctorFreeAppointmentSerializer

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



class PatientReserveAppointment(APIView):
    def get (self,request,pk):
        pra_query=Appointment.objects.filter(user__id=pk,status_reservation__in='reserve')
        serializer=ReserveAppointmentSerializer(pra_query,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)



class MyDoctor(APIView):
    def get (self,request,pk):
        l=['reserve','reserved','cancel']
        ra_query=Appointment.objects.filter(user__id=pk,status_reservation__in=l)
        serializer=MyDoctorsSerializer(ra_query,many=True,context={'request': request})
        return Response (serializer.data,status=status.HTTP_200_OK,)




class DoctorFreeAppointment(APIView):
    def get(self,request,pk):
        a=Appointment.objects.filter(doctor__id=pk,status_reservation='free')
        serializer=DoctorFreeAppointmentSerializer(a,many=True)
        return Response (serializer.data,status=status.HTTP_200_OK,)

# 
# from django.urls import reverse
# from azbankgateways import bankfactories, models as bank_models, default_settings as settings
# from azbankgateways.exceptions import AZBankGatewaysException
# 
# 
# def go_to_gateway_view(request):
    # خواندن مبلغ از هر جایی که مد نظر است
    # amount = 5000
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    # user_mobile_number = '+989112221234'  # اختیاری
# 
    # factory = bankfactories.BankFactory()
    # 
    # bank = factory.auto_create() # or factory.create(bank_models.BankType.BMI) or set identifier
    # bank.set_request(request)
    # bank.set_amount(amount)
    # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
    # bank.set_client_callback_url('/callback-gateway/')
    # bank.set_mobile_number(user_mobile_number)  # اختیاری
# 
    # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
    # پرداخت برقرار کنید. 
    # bank_record = bank.ready()
    
    # هدایت کاربر به درگاه بانک
    # return bank.redirect_gateway()



# from django.http import HttpResponse, Http404
# from django.urls import reverse
# 
# 
# def callback_gateway_view(request):
    # tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    # if not tracking_code:
        # raise Http404
# 
    # try:
        # bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    # except bank_models.Bank.DoesNotExist:
        # raise Http404
# 
    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    # if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        # return HttpResponse("پرداخت با موفقیت انجام شد.")
# 
    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    # return HttpResponse("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")