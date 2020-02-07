from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(roles)
admin.site.register(user_profile)
admin.site.register(department)
admin.site.register(designation)
admin.site.register(employee_profile)
admin.site.register(holidays)
admin.site.register(terminations)
admin.site.register(employee_bank_details)
admin.site.register(tb_timesheet)
admin.site.register(daily_attendance_employee)
admin.site.register(tb_employee_leaves)




class companyAdmin(admin.ModelAdmin):

    fields = ("role_id", "company_user_email",
              "company_user_password", "created_date", "is_active")


admin.site.register(company_profile, companyAdmin)
