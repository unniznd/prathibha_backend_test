# Generated by Django 4.2 on 2023-05-22 02:59

import attendance.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendace',
            name='date',
            field=models.DateField(validators=[attendance.models.validate_date_not_future]),
        ),
    ]