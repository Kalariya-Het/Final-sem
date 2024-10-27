# Generated by Django 3.0.8 on 2021-02-27 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_system', '0008_auto_20210227_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='dept',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='attendance_system.City'),
        ),
        migrations.AlterField(
            model_name='person',
            name='inst',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='attendance_system.Country'),
        ),
    ]