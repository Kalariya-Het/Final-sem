# Generated by Django 3.0.8 on 2021-02-26 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_system', '0003_auto_20210226_1243'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='country',
            new_name='inst',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='city',
            new_name='dept',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='country',
            new_name='inst',
        ),
    ]
