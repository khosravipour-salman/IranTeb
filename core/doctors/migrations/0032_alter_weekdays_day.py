# Generated by Django 4.0.4 on 2022-08-20 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0031_rename_specilist_doctorspecialist_specialist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weekdays',
            name='day',
            field=models.TextField(choices=[('saturday', 'saturday'), ('sunday', 'sunday'), ('monday', 'monday'), ('tuesday', 'tuesday'), ('wednesday', 'wednesday'), ('thursday', 'thursday'), ('friday', 'friday')]),
        ),
    ]
