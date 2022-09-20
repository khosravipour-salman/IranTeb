from __future__ import absolute_import, unicode_literals
import django
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

BROKER_URL = "amqp://guest:guest@localhost/"

app = Celery('core', broker=BROKER_URL)

timezone='Asia/Tehran'

enable_utc=True

app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.beat_schedule = {
    # 'add-every-30-seconds': {
        # 'task': 'test1',
        # 'schedule': 30.0,
    # },
# }
# app.conf.timezone = 'UTC'

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Execute daily at midnight...
    sender.add_periodic_task(
        # crontab(minute=0, hour=0),
        # crontab(),
        1,
        test(),
    )


@app.task()
def test():
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    print('##################################################')
    # a=DoctorUser.objects.get(id=2)
    # a.full_name='mehrshadgh'
    # a.save()


# from doctors.models import DoctorUser
# from patients.models import Appointment
# import jdatetime


# def check_appointment_for_doctor():
    # all_doctor=DoctorUser.objects.all()
    # for doctor in all_doctor:
        # a = Appointment.objects.filter(doctor=doctor).first()
        # create_appointment=a.doctor_appointments()
        # return {'msg':'check appointments and create new appointment for feture'}
# 
# 
# def check_deprecated_appointment():
    # today=jdatetime.datetime.today().date()
    # deprecated_appointment=Appointment.objects.filter(status_reservation='reserve',date_of_visit__lt=today)
    # deprecated_appointment.update(status_reservation='reserved')
# 