# Generated by Django 4.0.4 on 2022-08-17 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0016_doctorcity_alter_doctoruser_city'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctorcity',
            old_name='city',
            new_name='name_city',
        ),
    ]