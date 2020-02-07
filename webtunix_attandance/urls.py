"""webtunix_attandance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from home import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.user_login, name='login'),
    url(r'^designationdetails$', views.designations_details),
    url(r'^home$', views.dashboard, name='home_dashboard'),
    url(r'^all-employees$', views.all_employee, name='all_employee'),
    url(r'^attendance-admin', views.attendance_admin, name='attendance_admin'),
    url(r'^attendance-employee', views.attendance_employee,
        name='attendance_employee'),
    url(r'^change-password', views.change_password, name='change_password'),
    url(r'^departments', views.departments_func, name='departments'),
    url(r'^designation', views.designations_func, name='designation'),
    
    url(r'^employee-salary', views.employee_salary, name='employee_salary'),
   
    url(r'^error-404', views.error_404, name='error_404'),
    url(r'^error-500', views.error_500, name='error_500'),
    url(r'^faq$', views.faq, name='faq'),
    url(r'^forgot-password', views.forgot_password, name='forgot_password'),
    url(r'^holidays', views.holidays_func, name='holidays'),
    url(r'^leave-admin', views.leave_admin, name='leave_admin'),
    url(r'^leave-employee', views.leave_employee, name='leave_employee'),
    url(r'^leave-setting', views.leave_setting, name='leave_setting'),
    url(r'^leave-type', views.leave_type, name='leave_type'),
    url(r'^lock-screen', views.lock_screen, name='lock_screen'),
    url(r'^otp', views.otp, name='otp'),
    url(r'^overtime', views.overtime, name='overtime'),
    url(r'^payroll-item', views.payroll_item, name='payroll_item'),
    url(r'^payslip$', views.payslip, name='payslip'),
    url(r'^promotion$', views.permotion, name='permotion'),
    url(r'^privacy-policy$', views.privacy_policy, name='privacy_policy'),
    url(r'^profile$', views.profile_func, name='profile'),
    url(r'^register$', views.register, name='register'),
    url(r'^resignation$', views.resignation, name='resignation'),
    url(r'^salary-setting$', views.salary_setting, name='salary_setting'),
    url(r'^settings$', views.setting_func, name='setting'),
    url(r'^termination$', views.termination_func, name='termination'),
    # url(r'^terms&condition$', views.terms_condition, name='terms_condition'),
    url(r'^timesheet$', views.timesheet, name='timesheet'),
    url(r'^users', views.users, name='users'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^update-profile$', views.update_profile_func, name='update-profile'),
    url(r'^search-users$', views.search_added_user, name='all-users'),
    url(r'^user-profile-details$', views.user_profile_details_func, name='user-profile-details'),
    # url(r'^edit/<int:designation_id>', views.edit_designations, name='edit_designations'),
    # url(r'^edit_holidays/<int:holiday_id>', views.edit_holidays, name='edit_holidays'),
    url(r'^del_holidays/<int:holiday_id>', views.del_holidays, name='del_holidays'),
    url(r'^delete/<int:designation_id>', views.delete, name='delete'),

    # url(r'^forgot', views.forgot, name='forgot'),
    # url(r'^signup', views.signup, name='signup'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
