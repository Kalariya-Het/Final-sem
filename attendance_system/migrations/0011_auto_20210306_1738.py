# Generated by Django 3.0.8 on 2021-03-06 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_system', '0010_auto_20210227_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_id', models.IntegerField()),
                ('inst', models.CharField(max_length=10)),
                ('dept', models.CharField(max_length=10)),
                ('date', models.DateField()),
                ('in_time', models.TimeField()),
                ('out_time', models.TimeField()),
                ('is_in_or_out', models.BooleanField()),
            ],
        ),
        migrations.AlterField(
            model_name='person',
            name='password',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
