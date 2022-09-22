from asyncio.windows_events import NULL
from patients.models import Patient, Wallet
import random
import redis
from datetime import timedelta
import jdatetime

from django.core.cache import cache
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from doctors.models import DoctorUser
from .models import Appointment
from django.db.models import Avg
from doctors.models import CommentForDoctor

from patients.serializers import (ReserveAppointmentSerializer, MyDoctorsSerializer,
                                  DoctorFreeAppointmentSerializer, RserveAppointmentByPatientSerializer,
                                  WalletSerializer, patientCompleteInfoSerilizer, LogOutSerializer)


r = redis.Redis(host='localhost', port=6379, db=0)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['phone_number'] = user.phone_number
        token['full_name'] = user.full_name

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class GetUserID(APIView):
    def post(self, request):
        data = self.request.data
        access_token = data['access_token']
        access_token_obj = AccessToken(access_token)
        user_id = access_token_obj['user_id']
        user_full_name=access_token_obj['full_name']
        user_phone_number=access_token_obj['phone_number']
        return Response({'user_id': user_id})


class PatientLoginSendOTp(APIView):
    def post(self, request):
        phone_number = self.request.data['phone_number']
        if not phone_number:
            return Response({"msg": "phone number is requierd'"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            dr_user = Patient.objects.get(phone_number=phone_number)
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


class PatientRegisterSendOTp (APIView):

    def post(self, request):
        phone_number = self.request.data['phone_number']
        if not phone_number:
            return Response({"msg": "phone number is requierd'"}, status=status.HTTP_400_BAD_REQUEST)

        patient = Patient.objects.create(
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


class PatientVerifyOTP(APIView):

    def post(self, request):
        phone_number = self.request.data['phone_number']
        patient = Patient.objects.get(phone_number=phone_number)
        code = self.request.data['code']
        cached_code = r.get(str(phone_number)).decode()
        # cached_code = cache.get(str(phone_number))
        if code != cached_code:
            return Response({"msg": "code not matched"}, status=status.HTTP_403_FORBIDDEN)
        token = get_tokens_for_user(patient)
        return Response({'token': token, 'msg': 'Successful'}, status=status.HTTP_201_CREATED)


class PatientCompleteInfo(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        data = self.request.data
        phone_number = data['phone_number']

        patient = Patient.objects.get(phone_number=phone_number)
        serializer = patientCompleteInfoSerilizer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            patient.is_active = True
            patient.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NumActiveUser(APIView):
    def get(self, request):
        query = Patient.objects.all().count()
        return Response({"num_active_user": query}, status=status.HTTP_200_OK)


class NumSuccessfulReseced(APIView):
    def get(self, request):
        query = Appointment.objects.filter(
            status_reservation='reserved').count()
        return Response({"num_success_reserved": query}, status=status.HTTP_200_OK)


class UserSatisfy(APIView):
    def get(self, request):
        query = CommentForDoctor.objects.all().aggregate(Avg('rating'))
        a = f" {query['rating__avg']*20} % "
        return Response({"percent_satisfy": a}, status=status.HTTP_200_OK)


class PatientReserveAppointment(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        pra_query = Appointment.objects.filter(
            user__id=pk, status_reservation__in='reserve')
        serializer = ReserveAppointmentSerializer(pra_query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientReservedAppointment(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        pra_query = Appointment.objects.filter(
            user__id=pk, status_reservation__in='reserved')
        serializer = ReserveAppointmentSerializer(pra_query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyDoctor(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        l = ['reserve', 'reserved', 'cancel']
        ra_query = Appointment.objects.filter(
            user__id=pk, status_reservation__in=l)
        serializer = MyDoctorsSerializer(
            ra_query, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK,)


class DoctorFreeAppointment(APIView):
    def get(self, request, pk):
        object = Appointment.objects.filter(doctor__id=pk).exists()
        if object == False:
            Appointment.objects.create(doctor__id=pk)
        a = Appointment.objects.filter(doctor__id=pk).first()
        a.doctor_appointments()
        # Appointment.objects.filter(doctor__id=pk,start_visit_time=None,end_visit_time=None).delete()

        query = Appointment.objects.filter(
            doctor__id=pk, status_reservation='free')
        serializer = DoctorFreeAppointmentSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK,)


class MyWallet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        query = Wallet.objects.get(user__id=pk)
        serializer = WalletSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RserveAppointmentByPatient(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, u_id, dr_id):
        user = Patient.objects.get(id=u_id)
        doctor = DoctorUser.objects.get(id=dr_id)
        data = self.request.data
        # doctor = data['doctor']
        start_visit_time = data['start_visit_time']
        end_visit_time = data['end_visit_time']
        date_of_visit = data['date_of_visit']
        q = Appointment.objects.filter(
            doctor=doctor, start_visit_time=start_visit_time, end_visit_time=end_visit_time,
            date_of_visit=date_of_visit, status_reservation='free').first()
        print(q)
        print("$$$$$$$$$$$$$$")
        q.user = user
        q.status_reservation = 'reserve'
        q.reservetion_code = random.randint(10000, 99999)
        q.save()
        # q.update(user=user, status_reservation='reserve',
        #  reservetion_code=random.randint(10000, 99999))
        print(q)
        print("$$^^^^^^^^^^^^^^^^^")
        serializer = RserveAppointmentByPatientSerializer(q)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CancelAppointmentByPatient(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, u_id, dr_id):
        data = self.request.data
        start_visit_time = data['start_visit_time']
        end_visit_time = data['end_visit_time']
        date_of_visit = data['date_of_visit']
        reserve_appointment = Appointment.objects.filter(
            user__id=u_id, doctor__id=dr_id, date_of_visit=date_of_visit, start_visit_time=start_visit_time,
            end_visit_time=end_visit_time, status_reservation='reserve').first()

        date_of_appointment = reserve_appointment.date_of_visit
        to_day = jdatetime.datetime.today().date()
        delta = (date_of_appointment-to_day).days
        if delta >= 2:
            reserve_appointment.user = None
            reserve_appointment.reservetion_code = None
            reserve_appointment.status_reservation = 'free'
            reserve_appointment.save()

            return Response({'msg': 'appointment canceled by patient'}, status=status.HTTP_200_OK)

        return Response({'msg': 'you can cancel maximon 48hour befor resserve time '}, status=status.HTTP_400_BAD_REQUEST)


class CnacelAppointmentByDoctor(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, u_id, dr_id):
        data = self.request.data
        start_visit_time = data['start_visit_time']
        end_visit_time = data['end_visit_time']
        date_of_visit = data['date_of_visit']
        reserve_appointment = Appointment.objects.filter(
            user__id=u_id, doctor__id=dr_id, date_of_visit=date_of_visit, start_visit_time=start_visit_time,
            end_visit_time=end_visit_time, status_reservation='reserve').first()

        date_of_appointment = reserve_appointment.date_of_visit
        to_day = jdatetime.datetime.today().date()
        delta = (date_of_appointment-to_day).days
        if delta >= 2:
            reserve_appointment.status_reservation = 'cancel'
            reserve_appointment.save()
            return Response({'msg': 'appointment canceled by doctor'}, status=status.HTTP_200_OK)

        return Response({'msg': 'you can cancel maximon 48hour befor resserve time '}, status=status.HTTP_400_BAD_REQUEST)


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
