# Generated by Django 3.2 on 2022-09-24 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0012_auto_20220923_0407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
