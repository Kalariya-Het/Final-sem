# Generated by Django 3.0.8 on 2021-03-24 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_system', '0017_attendance_is_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='total_hour',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
