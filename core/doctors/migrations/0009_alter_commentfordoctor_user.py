# Generated by Django 3.2 on 2022-08-16 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_initial'),
        ('doctors', '0008_auto_20220816_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentfordoctor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.patient'),
        ),
    ]
