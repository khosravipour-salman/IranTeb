# Generated by Django 3.2 on 2022-09-30 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0017_alter_patient_national_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='payment_code',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
