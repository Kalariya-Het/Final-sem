# Generated by Django 3.0.8 on 2021-02-26 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_system', '0005_person_reg_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='password',
            field=models.CharField(max_length=10, null=True),
        ),
    ]