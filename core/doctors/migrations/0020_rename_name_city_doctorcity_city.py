# Generated by Django 4.0.4 on 2022-08-17 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0019_doctorcity_alter_doctoruser_city'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctorcity',
            old_name='name_city',
            new_name='city',
        ),
    ]