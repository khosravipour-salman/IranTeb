# Generated by Django 4.0.4 on 2022-08-17 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0017_rename_city_doctorcity_name_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctoruser',
            name='city',
            field=models.CharField(blank=True, choices=[('Tehran', 'Tehran'), ('Esfahan', 'Esfahan'), ('Shiraz', 'Shiraz'), ('Tabriz', 'Tabriz'), ('Gilan', 'Gilan'), ('Khoozestan', 'Khoozestan')], max_length=30, null=True),
        ),
        migrations.DeleteModel(
            name='DoctorCity',
        ),
    ]