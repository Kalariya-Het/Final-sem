# Generated by Django 3.0.8 on 2021-04-10 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_system', '0021_auto_20210410_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
