# Generated by Django 2.2.4 on 2019-09-23 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_daily_attendance_employee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee_profile',
            old_name='edit_request_by',
            new_name='edit_request_emp_email',
        ),
        migrations.AddField(
            model_name='employee_profile',
            name='edit_request_hr_email',
            field=models.CharField(default='', max_length=255),
        ),
    ]
