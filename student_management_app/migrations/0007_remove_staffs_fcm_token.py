# Generated by Django 4.2.1 on 2023-05-29 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0006_staffs_fcm_token_staffs_updated_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staffs',
            name='fcm_token',
        ),
    ]
