# Generated by Django 2.2.4 on 2019-09-23 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_tb_employee_leaves_leave_policy_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tb_employee_leaves',
            name='casual_leaves',
        ),
        migrations.RemoveField(
            model_name='tb_employee_leaves',
            name='leaves_left_total',
        ),
        migrations.RemoveField(
            model_name='tb_employee_leaves',
            name='medical_leaves',
        ),
        migrations.RemoveField(
            model_name='tb_employee_leaves',
            name='total_leaves',
        ),
        migrations.AddField(
            model_name='tb_employee_leaves',
            name='above_limit_leaves',
            field=models.CharField(default='', max_length=50),
        ),
    ]
