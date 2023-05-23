# Generated by Django 4.2 on 2023-05-23 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branch_class', '0001_initial'),
        ('attendance', '0002_alter_attendace_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='holiday',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='branch_class.officebranchmodel'),
        ),
        migrations.AlterField(
            model_name='holiday',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterUniqueTogether(
            name='holiday',
            unique_together={('branch', 'date')},
        ),
    ]
