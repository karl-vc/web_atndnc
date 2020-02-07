# Generated by Django 2.2.4 on 2019-09-19 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_delete_daily_attendance_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='daily_attendance_employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('db_date', models.CharField(default='', max_length=2)),
                ('db_month', models.CharField(default='', max_length=2)),
                ('db_year', models.CharField(default='', max_length=4)),
                ('present', models.BooleanField(default=False)),
                ('on_leave', models.BooleanField(default=False)),
                ('company_mail', models.CharField(default='', max_length=255)),
                ('hr_mail', models.CharField(default='', max_length=255)),
                ('employee_employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.employee_profile')),
            ],
        ),
    ]
