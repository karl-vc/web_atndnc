import copy
import random
from datetime import date, datetime
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render

from home.forms import *
from home.models import *
import calendar
# Create your views here.
# global variables




def user_login(request):

    try:

        today1 = date.today()
        if_today_date1 = today1.strftime("%m/%d/%Y")
        str_date = str(if_today_date1)
        auto_terminate = terminations.objects.filter(
            Q(termination_date=str_date) & Q(request_status=2))
        for i in auto_terminate:
            if i.termination_date == if_today_date1:
                terminate_employee = employee_profile(employee_employee_id=i.employee_employee_id.employee_employee_id,
                                                      is_terminated=True, is_active=False)
                terminate_employee.save(
                    update_fields=['is_terminated', 'is_active'])


    except:

        pass

    form = UserLoginForm()

    if request.method == 'POST':

        form = UserLoginForm(request.POST)

        try:

            role = int(request.POST.get('role_id'))

            if int(role) == 1:

                if form.is_valid():
                    email = request.POST['email']
                    password = request.POST['password']

                    try:
                        company_data = company_profile.objects.get(
                            company_user_email=email)

                        if email == company_data.company_user_email:  # check if email exists
                            try:
                                # CHECK IF PASSWORD IS UPDATED(ENCRYPTED)

                                if not company_data.password_updated:

                                    if company_data.company_user_password == password:

                                        request.session['user_email'] = email
                                        request.session['user_role_id'] = company_data.role_id_id
                                        request.session['user_is_authenticated'] = True
                                        return redirect("/change-password")
                                    elif company_data.company_user_password != password:

                                        return render(request, 'login.html',
                                                      {'invalid_credentials': True, 'form': form})
                                if company_data.password_updated:

                                    if check_password(password, company_data.company_user_password):

                                        request.session['user_email'] = email
                                        request.session['user_role_id'] = company_data.role_id_id
                                        request.session['user_is_authenticated'] = True
                                        if not company_data.profile_updated:
                                            return redirect('/settings')
                                        if company_data.profile_updated:
                                            return redirect('/home')
                                    else:

                                        return render(request, 'login.html',
                                                      {'invalid_credentials': True, 'form': form})
                            except:

                                return render(request, 'login.html',
                                              {'invalid_credentials': True, 'form': form})
                    except:

                        return render(request, 'login.html', {'invalid_credentials': True, 'form': form})
            elif int(role) == 2:
                if form.is_valid():
                    email = request.POST['email']
                    password = request.POST['password']
                    hr_data = user_profile.objects.get(user_email=email)
                    if check_password(password, hr_data.user_password):
                        request.session['user_email'] = email
                        request.session['user_role_id'] = hr_data.role_id_id
                        request.session['user_is_authenticated'] = True
                        return redirect("/home")
                    else:
                        form = UserLoginForm(request.POST)
                        return render(request, 'login.html', {'invalid_credentials': True, 'form': form})
                elif not form.is_valid():
                    form = UserLoginForm(request.POST)
                    return render(request, 'login.html', {'invalid_credentials': True, 'form': form})
            elif int(role) == 3:
                if form.is_valid():
                    email = request.POST['email']
                    password = request.POST['password']
                    employee_data = employee_profile.objects.get(
                        employee_official_email=email)
                    if check_password(password, employee_data.employee_password):
                        if not employee_data.is_terminated:
                            request.session['user_email'] = email
                            request.session['user_role_id'] = employee_data.role_id_id
                            request.session['user_is_authenticated'] = True

                            return redirect("/home")
                        if employee_data.is_terminated:
                            form = UserLoginForm(request.POST)
                            return render(request, 'login.html', {'invalid_credentials': True, 'form': form})
                    else:
                        form = UserLoginForm(request.POST)
                        return render(request, 'login.html', {'invalid_credentials': True, 'form': form})
                elif not form.is_valid():
                    form = UserLoginForm(request.POST)
                    return render(request, 'login.html', {'invalid_credentials': True, 'form': form})
            else:
                form = UserLoginForm(request.POST)
                return render(request, 'login.html', {'role_not_selected': True, 'form': form})
        except:
            form = UserLoginForm(request.POST)
            return render(request, 'login.html', {'role_not_selected': True, 'form': form})
    return render(request, 'login.html', {'form': form})


def dashboard(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False

    if permission:

        today = date.today()
        today_date = today.strftime("%d %B, %Y")
        today_day = date.today().strftime("%A")

        # log in as admin
        if request.session['user_role_id'] == 1:
            company_data = company_profile.objects.get(
                company_user_email=request.session['user_email'])
            notifications_data = employee_profile.objects.filter(
                Q(employee_company_email=request.session['user_email']))
            termination_requests = terminations.objects.filter(
                Q(company_email=request.session['user_email']))

            attendance_check = daily_attendance_employee.objects.all()
            print(attendance_check, "dff")

            if not attendance_check:
                total_employees = employee_profile.objects.all()
                for i in total_employees:
                    form2 = attendancForm(request.POST)
                    f2 = form2.save(commit=False)
                    f2.db_date = today.strftime("%d")
                    f2.db_month = today.strftime("%m")
                    f2.db_year = today.strftime("%Y")
                    f2.company_mail = request.session['user_email']
                    f2.employee_employee_id_id = i.employee_employee_id
                    f2.present = False
                    f2.save()
            elif attendance_check:
                for i in attendance_check:

                    if i.db_date == today.strftime("%d") and i.db_month == today.strftime(
                            "%m") and i.db_year == today.strftime("%Y"):
                        print(1)
                        pass
                    elif i.db_date != today.strftime("%d") and i.db_month != today.strftime(
                            "%m") and i.db_year != today.strftime("%Y"):
                        print(2)
                        total_employees = employee_profile.objects.all()

                        for i in total_employees:
                            form2 = attendancForm(request.POST)
                            f2 = form2.save(commit=False)
                            f2.db_date = today.strftime("%d")
                            f2.db_month = today.strftime("%m")
                            f2.db_year = today.strftime("%Y")
                            f2.company_mail = request.session['user_email']
                            f2.employee_employee_id_id = i.employee_employee_id
                            f2.present = False
                            f2.save()

            if 'approved_termination' in request.POST:

                id = request.POST['actionable_id']
                appv_term_id = terminations.objects.get(
                    employee_employee_id_id=id)
                update_apprv_info = terminations(
                    id=appv_term_id.id, request_status=2)
                update_apprv_info.save(update_fields=['request_status'])

            if 'decline_termination' in request.POST:

                id = request.POST['actionable_id']
                appv_term_id = terminations.objects.get(
                    employee_employee_id_id=id)
                update_apprv_info = terminations(
                    id=appv_term_id.id, request_status=3)
                update_apprv_info.save(
                    update_fields=['request_status'])

            if 'approved' in request.POST:
                id = request.POST['actionable_id']
                update_basic_info = employee_profile(employee_employee_id=id,
                                                     request_status=2, permission_to_edit=True)
                update_basic_info.save(
                    update_fields=['request_status', 'permission_to_edit'])

            if 'decline' in request.POST:

                id = request.POST['actionable_id']
                update_basic_info = employee_profile(employee_employee_id=id,
                                                     request_status=3, permission_to_edit=False, edit_request_by_hr=False)
                update_basic_info.save(
                    update_fields=['request_status', 'permission_to_edit', 'edit_request_by_hr'])
            return render(request, "dashboard/dashboard.html", {'today_date': today_date,
                                                                'today_day': today_day,
                                                                'company_data': company_data,
                                                                'notify_requests': notifications_data,
                                                                'termination_requests': termination_requests})

            # log in as HR
        elif request.session['user_role_id'] == 2:

            requests_data = employee_profile.objects.filter(Q(edit_request_by_emp=True) and
                                                            Q(employee_hr_email=request.session['user_email']))

            termination_requests = terminations.objects.filter(
                Q(hr_email=request.session['user_email']))
            hr_data = user_profile.objects.get(
                user_email=request.session['user_email'])

            leaves_data = tb_employee_leaves.objects.filter(
                Q(emp_cmpy_email=hr_data.user_company_email))

            notifications_data = employee_profile.objects.filter(
                Q(employee_company_email=hr_data.user_company_email))

            attendance_check = daily_attendance_employee.objects.all()

            if not attendance_check:
                total_employees = employee_profile.objects.all()
                for i in total_employees:
                    form2 = attendancForm(request.POST)
                    f2 = form2.save(commit=False)
                    f2.db_date = today.strftime("%d")
                    f2.db_month = today.strftime("%m")
                    f2.db_year = today.strftime("%Y")
                    f2.company_mail = hr_data.user_company_email
                    f2.employee_employee_id_id = i.employee_employee_id
                    f2.present = False
                    f2.save()
            elif attendance_check:
                for i in attendance_check:

                    if i.db_date == today.strftime("%d") and i.db_month == today.strftime(
                            "%m") and i.db_year == today.strftime("%Y"):
                        print(1)
                        pass
                    elif i.db_date != today.strftime("%d") and i.db_month != today.strftime(
                            "%m") and i.db_year != today.strftime("%Y"):
                        print(2)
                        total_employees = employee_profile.objects.all()

                        for i in total_employees:
                            form2 = attendancForm(request.POST)
                            f2 = form2.save(commit=False)
                            f2.db_date = today.strftime("%d")
                            f2.db_month = today.strftime("%m")
                            f2.db_year = today.strftime("%Y")
                            f2.company_mail = hr_data.user_company_email
                            f2.employee_employee_id_id = i.employee_employee_id
                            f2.present = False
                            f2.save()

            if 'approved_short_leave' in request.POST:
                id = request.POST['actionable_id']
                total_id = []
                for i in leaves_data:
                    if i.short_leave and i.employee_employee_id_id == id:
                        total_id.append(i.id)
                updatable_id = total_id[-1]
                update_leave_data = tb_employee_leaves(id=updatable_id,
                                                       leave_status=2, emp_hr_email=request.session['user_email'])

                update_leave_data.save(
                    update_fields=['leave_status', 'emp_hr_email'])
            if 'decline_short_leave' in request.POST:
                id = request.POST['actionable_id']
                total_id = []
                for i in leaves_data:
                    if i.short_leave and i.employee_employee_id_id == id:
                        total_id.append(i.id)
                updatable_id = total_id[-1]

                update_leave_data = tb_employee_leaves(id=updatable_id,
                                                       leave_status=3, emp_hr_email=request.session['user_email'])

                update_leave_data.save(
                    update_fields=['leave_status', 'emp_hr_email'])

            if 'approved_oneday_leave' in request.POST:
                id = request.POST['actionable_id']
                total_id = []
                for i in leaves_data:
                    if i.one_day_leave and i.employee_employee_id_id == id:
                        total_id.append(i.id)
                updatable_id = total_id[-1]
                casual_medical = tb_employee_leaves.objects.get(
                    Q(id=updatable_id))
                if casual_medical.leave_type == "Casual":
                    leaves_count_monthly = []
                    for j in leaves_data:
                        if j.employee_employee_id_id == id:
                            leaves_count_monthly.append(j.leaves_left_monthly)

                    leaves_counted_monthly1 = leaves_count_monthly[-1]

                    leaves_counted_monthly2 = float(leaves_counted_monthly1)-1

                    update_leave_data = tb_employee_leaves(id=updatable_id,
                                                           leave_status=2, emp_hr_email=request.session['user_email'], leaves_left_monthly=leaves_counted_monthly2)

                    update_leave_data.save(
                        update_fields=['leave_status', 'emp_hr_email', 'leaves_left_monthly'])
                elif casual_medical.leave_type == "Medical":
                    update_leave_data = tb_employee_leaves(id=updatable_id,
                                                           leave_status=2, emp_hr_email=request.session['user_email'])

                    update_leave_data.save(
                        update_fields=['leave_status', 'emp_hr_email'])

            if 'decline_oneday_leave' in request.POST:
                id = request.POST['actionable_id']
                total_id = []
                for i in leaves_data:
                    if i.one_day_leave and i.employee_employee_id_id == id:
                        total_id.append(i.id)
                updatable_id = total_id[-1]
                leaves_count_monthly = []
                for j in leaves_data:
                    if j.employee_employee_id_id == id:
                        leaves_count_monthly.append(j.leaves_left_monthly)

                leaves_counted_monthly1 = leaves_count_monthly[-1]

                update_leave_data = tb_employee_leaves(id=updatable_id,
                                                       leave_status=3, emp_hr_email=request.session['user_email'], leaves_left_monthly=leaves_counted_monthly1)

                update_leave_data.save(
                    update_fields=['leave_status', 'emp_hr_email', 'leaves_left_monthly'])

            if 'approved_sandwich_leave' in request.POST:
                id = request.POST['actionable_id']
                total_id = []
                for i in leaves_data:
                    if i.leave_policy_type == 'Sandwich' and i.employee_employee_id_id == id:
                        total_id.append(i.id)
                updatable_id = total_id[-1]
                casual_medical = tb_employee_leaves.objects.get(
                    Q(id=updatable_id))

                from_date = casual_medical.leave_from
                to_date = casual_medical.leave_to

                date_str1 = from_date
                format_str = '%m/%d/%Y'
                datetime_obj1 = datetime.strptime(date_str1, format_str)
                dayofweek1 = datetime.date(datetime_obj1).strftime("%A")

                date_str2 = to_date
                format_str = '%m/%d/%Y'
                datetime_obj2 = datetime.strptime(date_str2, format_str)
                dayofweek2 = datetime.date(datetime_obj2).strftime("%A")

                if casual_medical.leave_type == "Casual":
                    leaves_count_monthly = []
                    for j in leaves_data:
                        if j.employee_employee_id_id == id:
                            leaves_count_monthly.append(j.leaves_left_monthly)

                    leaves_counted_monthly1 = leaves_count_monthly[-1]
                    if dayofweek1 == "Saturday" or dayofweek2 == "Monday":
                        month1 = from_date[:2]
                        try:
                            crnt_mnt = month1.lstrip("0")
                        except:
                            crnt_mnt = int(month1)
                        cal = calendar.monthcalendar(2019, int(crnt_mnt))
                        first_week = cal[0]
                        second_week = cal[1]
                        third_week = cal[2]
                        fourth_week = cal[3]
                        fifth_week = cal[4]

                        if first_week[calendar.SATURDAY] and fourth_week[calendar.SATURDAY]:
                            holi_day_1 = second_week[calendar.SATURDAY]
                            holi_day_2 = fourth_week[calendar.SATURDAY]
                        else:
                            holi_day_1 = third_week[calendar.SATURDAY]
                            holi_day_2 = fifth_week[calendar.SATURDAY]

                        if int(from_date[3:5]) != holi_day_1 or int(from_date[3:5]) != holi_day_2:

                            leaves_counted_monthly2 = float(
                                leaves_counted_monthly1) - 3

                            if float(leaves_counted_monthly1) <= 0:
                                above_limit_leaves = 3
                            else:
                                above_limit_leaves = 0
                                update_leave_data = tb_employee_leaves(id=updatable_id,
                                                                       leave_status=2, emp_hr_email=request.session['user_email'], leaves_left_monthly=leaves_counted_monthly2,
                                                                       above_limit_leaves=above_limit_leaves)

                                update_leave_data.save(
                                    update_fields=['leave_status', 'emp_hr_email', 'leaves_left_monthly', 'above_limit_leaves'])

                    elif dayofweek1 == "Friday":
                        if dayofweek2 == "Monday":

                            leaves_count_monthly = []
                            for i in leaves_data:
                                leaves_count_monthly.append(
                                    i.leaves_left_monthly)
                            leaves_counted_monthly1 = leaves_count_monthly[-1]

                            leaves_counted_monthly2 = float(
                                leaves_counted_monthly1) - 4

                            if float(leaves_counted_monthly1) <= 0:
                                above_limit_leaves = 4
                            else:
                                above_limit_leaves = 0
                            update_leave_data = tb_employee_leaves(id=updatable_id,
                                                                   leave_status=2, emp_hr_email=request.session['user_email'], leaves_left_monthly=leaves_counted_monthly2,
                                                                   above_limit_leaves=above_limit_leaves)

                            update_leave_data.save(
                                update_fields=['leave_status', 'emp_hr_email', 'leaves_left_monthly', 'above_limit_leaves'])
                elif casual_medical.leave_type == "Medical":
                    update_leave_data = tb_employee_leaves(id=updatable_id,
                                                           leave_status=2, emp_hr_email=request.session['user_email'])

                    update_leave_data.save(
                        update_fields=['leave_status', 'emp_hr_email'])

            if 'decline_sandwich_leave' in request.POST:
                id = request.POST['actionable_id']
                total_id = []
                for i in leaves_data:
                    if i.leave_policy_type == 'Sandwich' and i.employee_employee_id_id == id:
                        total_id.append(i.id)
                updatable_id = total_id[-1]
                leaves_count_monthly = []
                for j in leaves_data:
                    if j.employee_employee_id_id == id:
                        leaves_count_monthly.append(j.leaves_left_monthly)

                leaves_counted_monthly1 = leaves_count_monthly[-1]

                update_leave_data = tb_employee_leaves(id=updatable_id,
                                                       leave_status=3, emp_hr_email=request.session['user_email'], leaves_left_monthly=leaves_counted_monthly1)

                update_leave_data.save(
                    update_fields=['leave_status', 'emp_hr_email', 'leaves_left_monthly'])

            if 'approved_line_leave' in request.POST:
                id = request.POST['actionable_id']
                total_id = []
                for i in leaves_data:
                    if i.leave_policy_type == 'LineToLine' and i.employee_employee_id_id == id:
                        total_id.append(i.id)
                updatable_id = total_id[-1]
                casual_medical = tb_employee_leaves.objects.get(
                    Q(id=updatable_id))
                if casual_medical.leave_type == "Casual":
                    leaves_count_monthly = []
                    for j in leaves_data:
                        if j.employee_employee_id_id == id:
                            leaves_count_monthly.append(j.leaves_left_monthly)

                    leaves_counted_monthly1 = leaves_count_monthly[-1]

                    leaves_counted_monthly2 = float(leaves_counted_monthly1)-7

                    update_leave_data = tb_employee_leaves(id=updatable_id,
                                                           leave_status=2, emp_hr_email=request.session['user_email'], leaves_left_monthly=leaves_counted_monthly2, above_limit_leaves=2.5)

                    update_leave_data.save(
                        update_fields=['leave_status', 'emp_hr_email', 'leaves_left_monthly', 'above_limit_leaves'])
                elif casual_medical.leave_type == "Medical":
                    update_leave_data = tb_employee_leaves(id=updatable_id,
                                                           leave_status=2, emp_hr_email=request.session['user_email'], above_limit_leaves=2.5)

                    update_leave_data.save(
                        update_fields=['leave_status', 'emp_hr_email', 'above_limit_leaves'])

            if 'decline_line_leave' in request.POST:
                id = request.POST['actionable_id']
                total_id = []
                for i in leaves_data:
                    if i.leave_policy_type == 'LineToLine' and i.employee_employee_id_id == id:
                        total_id.append(i.id)
                updatable_id = total_id[-1]
                leaves_count_monthly = []
                for j in leaves_data:
                    if j.employee_employee_id_id == id:
                        leaves_count_monthly.append(j.leaves_left_monthly)

                leaves_counted_monthly1 = leaves_count_monthly[-1]

                update_leave_data = tb_employee_leaves(id=updatable_id,
                                                       leave_status=3, emp_hr_email=request.session['user_email'], leaves_left_monthly=leaves_counted_monthly1)

                update_leave_data.save(
                    update_fields=['leave_status', 'emp_hr_email', 'leaves_left_monthly'])

            if 'approved_half_leave' in request.POST:

                id = request.POST['actionable_id']

                total_id = []
                leaves_count_monthly = []
                for i in leaves_data:
                    if i.half_day_leave and i.employee_employee_id_id == id and i.leave_type == "Casual":
                        total_id.append(i.id)

                updatable_id = total_id[-1]
                casual_medical = tb_employee_leaves.objects.get(
                    Q(id=updatable_id))
                if casual_medical.leave_type == "Casual":
                    for j in leaves_data:
                        if j.employee_employee_id_id == id:
                            leaves_count_monthly.append(j.leaves_left_monthly)
                        leaves_counted_monthly1 = leaves_count_monthly[-1]
                        leaves_counted_monthly2 = float(
                            leaves_counted_monthly1)-0.5

                        update_leave_data = tb_employee_leaves(id=updatable_id,
                                                               leave_status=2, emp_hr_email=request.session['user_email'], leaves_left_monthly=leaves_counted_monthly2)

                        update_leave_data.save(
                            update_fields=['leave_status', 'emp_hr_email', 'leaves_left_monthly'])

                elif casual_medical.leave_type == "Medical":
                    update_leave_data = tb_employee_leaves(id=updatable_id,
                                                           leave_status=2, emp_hr_email=request.session['user_email'])

                    update_leave_data.save(
                        update_fields=['leave_status', 'emp_hr_email'])

            if 'decline_half_leave' in request.POST:
                id = request.POST['actionable_id']
                total_id = []
                leaves_count_monthly = []
                for i in leaves_data:
                    if i.half_day_leave and i.employee_employee_id_id == id:
                        total_id.append(i.id)
                updatable_id = total_id[-1]
                for j in leaves_data:
                    if j.employee_employee_id_id == id:
                        leaves_count_monthly.append(j.leaves_left_monthly)
                leaves_counted_monthly1 = leaves_count_monthly[-1]
                update_leave_data = tb_employee_leaves(id=updatable_id,
                                                       leave_status=3, emp_hr_email=request.session['user_email'], leaves_left_monthly=leaves_counted_monthly1)

                update_leave_data.save(
                    update_fields=['leave_status', 'emp_hr_email', 'leaves_left_monthly'])

            if 'approved' in request.POST:
                id = request.POST['actionable_id']
                update_request_data = employee_profile(
                    employee_employee_id=id,
                    request_status=1, edit_request_hr_email=request.session['user_email'], edit_request_by_hr=True, edit_request_by_emp=False)

                update_request_data.save(update_fields=[
                    'request_status', 'edit_request_hr_email', 'edit_request_by_hr', 'edit_request_by_emp'])
                # update_basic_info = employee_profile(employee_employee_id=id,
                #                                      request_status=2, permission_to_edit=True)
                # update_basic_info.save(
                #     update_fields=['request_status', 'permission_to_edit'])

            if 'decline' in request.POST:
                id = request.POST['actionable_id']
                update_request_data = employee_profile(
                    employee_employee_id=id,
                    request_status=3, edit_request_hr_email=request.session['user_email'], edit_request_by_hr=True)

                update_request_data.save(update_fields=[
                    'request_status', 'edit_request_hr_email', 'edit_request_by_hr'])

            return render(request, "dashboard/dashboard.html", {'today_date': today_date,
                                                                'today_day': today_day,
                                                                'hr_data': hr_data,
                                                                'requests_data': requests_data,
                                                                'notifications_data': notifications_data,
                                                                'termination_requests': termination_requests,
                                                                'leaves_data': leaves_data})
            # log in as Employee
        elif request.session['user_role_id'] == 3:

            employee_data = employee_profile.objects.get(
                Q(employee_official_email=request.session['user_email']))
            try:
                terminations_data = terminations.objects.get(
                    employee_employee_id=employee_data.employee_employee_id)
                date_str = terminations_data.termination_notice_date
                format_str = '%m/%d/%Y'
                datetime_obj = datetime.strptime(date_str, format_str).date()
                notice_date = datetime_obj.strftime("%d, %m, %Y")
                if_today_date = today.strftime("%d, %m, %Y")
                if notice_date == if_today_date:
                    return render(request, "dashboard/dashboard.html", {'employee_data': employee_data,
                                                                        'today_date': today_date,
                                                                        'today_day': today_day,
                                                                        'terminations_data': terminations_data,
                                                                        'terminate_notice': True})
                else:
                    return render(request, "dashboard/dashboard.html", {'employee_data': employee_data,
                                                                        'today_date': today_date,
                                                                        'today_day': today_day})
            except:
                return render(request, "dashboard/dashboard.html", {'employee_data': employee_data,
                                                                    'today_date': today_date,
                                                                    'today_day': today_day})

    elif not permission:
        return redirect("/")


def all_employee(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        if request.session['user_role_id'] == 1 or request.session['user_role_id'] == 2:
            return render(request, "dashboard/all-employee.html")
        elif request.session['user_role_id'] == 3:
            return redirect("/home")
    elif not permission:
        return redirect("/")


def attendance_admin(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        if request.session['user_role_id'] == 1:
            today = date.today()
            # today.strftime("%d")
            employee_present_today = daily_attendance_employee.objects.filter(
                Q(company_mail=request.session['user_email']))
            total_employees = employee_profile.objects.filter(
                Q(employee_company_email=request.session['user_email']))
            return render(request, "dashboard/attendance-admin.html", {
                'employee_present_today': employee_present_today,
                'total_employees': total_employees,
                'today_date': today.strftime("%d"),
                'today_month': today.strftime("%m"),
                'today_year': today.strftime("%Y")})
        if request.session['user_role_id'] == 1 or request.session['user_role_id'] == 2:
            today = date.today()
            hr_data = user_profile.objects.get(
                Q(user_email=request.session['user_email']))

            employee_present_today = daily_attendance_employee.objects.filter(
                Q(company_mail=hr_data.user_company_email))
            total_employees = employee_profile.objects.filter(
                Q(employee_company_email=hr_data.user_company_email))
            return render(request, "dashboard/attendance-admin.html", {
                'employee_present_today': employee_present_today,
                'total_employees': total_employees,
                'today_date': today.strftime("%d"),
                'today_month': today.strftime("%m"),
                'today_year': today.strftime("%Y")})
        elif request.session['user_role_id'] == 3:
            return redirect("/home")
    elif not permission:
        return redirect("/")


def attendance_employee(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        if request.session['user_role_id'] == 3:
            now = datetime.now()
            today = date.today()
            empdata = employee_profile.objects.get(
                Q(employee_official_email=request.session['user_email']))
            all_punching_data = tb_timesheet.objects.filter(
                Q(employee_employee_id_id=empdata.employee_employee_id))

            try:

                punched_in = False
                punch_in_data = tb_timesheet.objects.filter(Q(employee_employee_id_id=empdata.employee_employee_id)
                                                            & Q(db_date=now.strftime("%d/%m/%Y"))).order_by('-db_date')
                last_id = []

                for i in punch_in_data:
                    last_id.append(i.id)
                latest_punched_in_Id = last_id[-1]
            except:
                try:
                    punch_in_data = tb_timesheet.objects.get(
                        Q(employee_employee_id_id=empdata.employee_employee_id) & Q(db_date=now.strftime("%d/%m/%Y")))
                    latest_punched_in_Id = punch_in_data.Id
                except:
                    pass

            login_first = True
            try:
                latest_punched_in_emp_data = tb_timesheet.objects.get(
                    id=latest_punched_in_Id)
                if latest_punched_in_emp_data.punch_in == "" and latest_punched_in_emp_data.db_date == now.strftime("%d/%m/%Y"):
                    punched_in = False
                    login_first = False
                if latest_punched_in_emp_data.punch_out == "" and latest_punched_in_emp_data.db_date == now.strftime(
                        "%d/%m/%Y"):
                    login_first = False
                    punched_in = True
            except:
                latest_punched_in_emp_data = False
            if "punch_in" in request.POST:
                login_first = False
                form = attendanceForm()
                f = form.save(commit=False)
                f.employee_employee_id_id = empdata.employee_employee_id
                f.punch_in = now.strftime("%I:%M %p")
                f.punch_out = ""
                f.total_hours = ""

                f.db_date = today.strftime("%d/%m/%Y")
                f.save()
                # change to be create here
                try:
                    attendance_check = daily_attendance_employee.objects.get(Q(db_date=today.strftime("%d"))
                                                                             and Q(db_month=today.strftime("%m"))
                                                                             and Q(db_year=today.strftime("%Y"))
                                                                             and Q(employee_employee_id_id=empdata.employee_employee_id))

                    daily_attendance = daily_attendance_employee(
                        id=attendance_check.id, present=True)
                    daily_attendance.save(update_fields=['present'])
                except:
                    form2 = attendancForm(request.POST)
                    f2 = form2.save(commit=False)
                    f2.db_date = today.strftime("%d")
                    f2.db_month = today.strftime("%m")
                    f2.db_year = today.strftime("%Y")
                    f2.company_mail = empdata.employee_company_email
                    f2.employee_employee_id_id = empdata.employee_employee_id
                    f2.present = True
                    f2.save()

                return render(request, "dashboard/attendance-employee.html", {'punched_in': True,
                                                                              'today': now.strftime("%d %B,%Y"),
                                                                              'punched_in_data_time': now.strftime("%I:%M %p"),
                                                                              'punch_in_data': punch_in_data,
                                                                              'login_first': login_first,
                                                                              'all_punching_data': all_punching_data})

            elif "punch_out" in request.POST:
                login_first = False

                date_to_be_compared = today.strftime("%d/%m/%Y")

                if latest_punched_in_emp_data.db_date == date_to_be_compared:
                    punchout_time = now.strftime("%I:%M %p")
                    timeFormat = '%I:%M %p'

                    difference = datetime.strptime(punchout_time, timeFormat)\
                        - datetime.strptime(latest_punched_in_emp_data.punch_in, timeFormat)

                    update_punch_out_data = tb_timesheet(
                        id=latest_punched_in_emp_data.id, punch_out=punchout_time, total_hours=difference)
                    update_punch_out_data.save(
                        update_fields=['punch_out', 'total_hours'])

                    return render(request, "dashboard/attendance-employee.html", {'punched_in': False,
                                                                                  'today': now.strftime("%d %B,%Y"),
                                                                                  'punched_data_time': now.strftime("%I:%M %p"),
                                                                                  'punch_in_data': punch_in_data,
                                                                                  'login_first': login_first,
                                                                                  'all_punching_data': all_punching_data})

                elif latest_punched_in_emp_data.db_date != date_to_be_compared:

                    return render(request, "dashboard/attendance-employee.html", {'punched_in': False,
                                                                                  'today': now.strftime("%d %B,%Y"),
                                                                                  'punched_data': latest_punched_in_emp_data,
                                                                                  'punch_in_data': punch_in_data,
                                                                                  'login_first': login_first,
                                                                                  'all_punching_data': all_punching_data})
            return render(request, "dashboard/attendance-employee.html", {'punched_in': punched_in,
                                                                          'today': now.strftime("%d %B,%Y"),
                                                                          'punched_data': latest_punched_in_emp_data,
                                                                          'punch_in_data': punch_in_data,
                                                                          'login_first': login_first,
                                                                          'all_punching_data': all_punching_data})

        elif request.session['user_role_id'] != 3:
            return redirect("/home")
    elif not permission:
        return redirect("/")


def change_password(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        form = updatePasswordForm()
        # log in as admin
        if request.session['user_role_id'] == 1:
            company_data = company_profile.objects.get(
                company_user_email=request.session['user_email'])
            if company_data.password_updated:
                # if admin profile is updated
                if request.method == "POST":
                    old_password = request.POST['old']
                    # check encrypted password
                    if check_password(old_password, company_data.company_user_password):
                        first_password = request.POST['new1']
                        final_password = request.POST['company_user_password']
                        if first_password == final_password:
                            encrypted_password = make_password(final_password)
                            update_company_password = company_profile(company_user_email=request.session['user_email'],
                                                                      company_user_password=encrypted_password,
                                                                      password_updated=True)
                            update_company_password.save(
                                update_fields=['company_user_password', 'password_updated'])
                            return render(request, "dashboard/update-password.html",
                                          {'form': form, 'updated_password': True,
                                           'company_updated': company_data.profile_updated})
                        elif first_password != final_password:

                            return render(request, "dashboard/update-password.html",
                                          {'form': form, 'password_not_matches': True})
                    else:
                        return render(request, "dashboard/update-password.html",
                                      {'form': form, 'invalid_old': True})
                return render(request, "dashboard/update-password.html",
                              {'form': form})
                # if admin profile is not updated
            elif not company_data.password_updated:
                if request.method == "POST":
                    old_password = request.POST['old']
                    if old_password == company_data.company_user_password:
                        first_password = request.POST['new1']
                        final_password = request.POST['company_user_password']
                        if first_password == final_password:
                            encrypted_password = make_password(final_password)
                            update_company_password = company_profile(company_user_email=request.session['user_email'],
                                                                      company_user_password=encrypted_password,
                                                                      password_updated=True)
                            update_company_password.save(
                                update_fields=['company_user_password', 'password_updated'])
                            return render(request, "dashboard/change-password.html",
                                          {'form': form, 'updated_password': True,
                                           'company_updated': company_data.profile_updated})
                        elif first_password != final_password:
                            return render(request, "dashboard/change-password.html",
                                          {'form': form, 'password_not_matches': True})
                    elif old_password != company_data.company_user_password:
                        return render(request, "dashboard/change-password.html",
                                      {'form': form, 'invalid_old': True})
                return render(request, "dashboard/change-password.html",
                              {'form': form, })

        # log in as HR
        elif request.session['user_role_id'] == 2:
            if request.method == "POST":
                old_password = request.POST['old']
                # check encrypted password
                user_profile_data = user_profile.objects.get(
                    Q(user_email=request.session['user_email']))
                if check_password(old_password, user_profile_data.user_password):
                    first_password = request.POST['new1']
                    final_password = request.POST['company_user_password']
                    if first_password == final_password:
                        encrypted_password = make_password(final_password)
                        user_profile_password = user_profile(user_employee_id=user_profile_data.user_employee_id,
                                                             user_password=encrypted_password)
                        user_profile_password.save(
                            update_fields=['user_password'])
                        return render(request, "dashboard/update-password.html",
                                      {'form': form, 'updated_password': True, })
                    elif first_password != final_password:

                        return render(request, "dashboard/update-password.html",
                                      {'form': form, 'password_not_matches': True})
                else:
                    return render(request, "dashboard/update-password.html",
                                  {'form': form, 'invalid_old': True})
            return render(request, "dashboard/update-password.html",
                          {'form': form})

        # log in as Employee
        elif request.session['user_role_id'] == 3:
            if request.method == "POST":
                old_password = request.POST['old']
                # check encrypted password
                emp_data = employee_profile.objects.get(
                    Q(employee_official_email=request.session['user_email']))
                if check_password(old_password, emp_data.employee_password):
                    first_password = request.POST['new1']
                    final_password = request.POST['company_user_password']
                    if first_password == final_password:
                        encrypted_password = make_password(final_password)
                        employee_profile_password = employee_profile(employee_employee_id=emp_data.employee_employee_id,
                                                                     employee_password=encrypted_password)
                        employee_profile_password.save(
                            update_fields=['employee_password'])
                        return render(request, "dashboard/update-password.html",
                                      {'form': form, 'updated_password': True, })
                    elif first_password != final_password:

                        return render(request, "dashboard/update-password.html",
                                      {'form': form, 'password_not_matches': True})
                else:
                    return render(request, "dashboard/update-password.html",
                                  {'form': form, 'invalid_old': True})
            return render(request, "dashboard/update-password.html",
                          {'form': form})
    elif not permission:
        return redirect("/")


def departments_func(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin or log in as HR
        if request.session['user_role_id'] == 1 or request.session['user_role_id'] == 2:
            form = departmentForm()
            dept_data = department.objects.all().order_by('-department_name')
            if request.method == "POST":
                form = departmentForm(request.POST)
                if form.is_valid():
                    f = form.save(commit=False)
                    f.department_name = request.POST['department_name']
                    f.added_by = request.session['user_email']
                    f.save()
                    form = departmentForm()
                    return render(request, "dashboard/departments.html", {'form': form, 'department_added': True, 'dept_data': dept_data})
                elif not form.is_valid():
                    form = departmentForm(request.POST)
                    return render(request, "dashboard/departments.html", {'form': form, 'dept_data': dept_data})
            return render(request, "dashboard/departments.html", {'form': form, 'dept_data': dept_data})
        elif request.session['user_role_id'] == 3:
            return redirect("/home")
    elif not permission:
        return redirect("/")


def designations_func(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin or log in as HR
        if request.session['user_role_id'] == 1 or request.session['user_role_id'] == 2:
            departments = department.objects.all()
            designations_data = designation.objects.all()
            if 'edit_designation' in request.POST:
                dep_id = request.POST['dept_name']
                des_name = request.POST['dest_name']
                des_id = request.POST['dest_id']
                update = designation(designation_id=des_id, designation_name=des_name)
                update.save(update_fields=["designation_name"])
                # return render(request, "dashboard/designation.html", {'departments': departments, 'form': form,
                #                                                       'designations_data': designations_data}, locals())
                return render(request, "dashboard/designation.html", locals())

            form = designationForm()
            if request.method == "POST":
                form = designationForm(request.POST)
                if form.is_valid():
                    dept = request.POST['department_selected']
                    if dept is not None:
                        f = form.save(commit=False)
                        f.department_id_id = request.POST['department_selected']
                        f.designation_name = request.POST['designation_name']
                        f.added_by = request.session['user_email']
                        f.save()
                        form = designationForm()

                        # return render(request, "dashboard/designation.html",
                        #               {'departments': departments, 'form': form, 'added_designation': True,
                        #                'designations_data': designations_data}, locals())
                    elif dept is None:
                        return render(request, "dashboard/designation.html",
                                      {'departments': departments, 'form': form, 'invalid_role': True,
                                       'designations_data': designations_data}, locals())
                elif not form.is_valid():
                    form = designationForm(request.POST)
                    return render(request, "dashboard/designation.html", locals())
                    # return render(request, "dashboard/designation.html", {'departments': departments, 'form': form})
            return render(request, "dashboard/designation.html", locals())
            # return render(request, "dashboard/designation.html", {'departments': departments, 'form': form,
            #                                                       'designations_data': designations_data}, locals())
        # log in as Employee
        elif request.session['user_role_id'] == 3:
            return redirect("/home")
    elif not permission:
        return redirect("/")
#######################################################################################################################

# def edit_designations(request, designation_id):
#     if request.method == "POST":
#         dep_id = request.POST['dept_name']
#         des_name = request.POST['dest_name']
#         des_id = request.POST['dest_id']
#         update = designation(designation_id=des_id, designation_name=des_name)
#         update.save(update_fields=["designation_name"])
#
#     else:
#         return render(request, "dashboard/designation.html", {'departments': departments, 'form': form,
#                                                               'designations_data': designations_data})
#

def delete(request,designation_id):
        aa = designation(designation_id=designation_id)
        aa.delete()
        return render(request, "dashboard/designation.html",{'aa': aa}, locals())

###################################################################################################

def employee_salary(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin
        if request.session['user_role_id'] == 1:
            return render(request, "dashboard/employee-salary.html")
        # log in as HR
        elif request.session['user_role_id'] == 2:
            return render(request, "dashboard/employee-salary.html")
        # log in as Employee
        elif request.session['user_role_id'] == 3:
            return redirect("/home")
    elif not permission:
        return redirect("/")


def error_404(request):
    return render(request, "dashboard/error-404.html")


def error_500(request):
    return render(request, "dashboard/error-500.html")


def faq(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        return render(request, "dashboard/faq.html")
    elif not permission:
        return redirect("/")


def forgot_password(request):

    return render(request, "dashboard/forgot-password.html")


def holidays_func(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        holidays_data = holidays.objects.all()
        if 'update_holiday' in request.POST:
            holiday_id=request.POST['holid']
            holiday_new_date = request.POST['holiday_new_date']
            holiday_name = request.POST['holiday_name']
            print(holiday_id,holiday_new_date)
            update = holidays(holiday_id=holiday_id, holiday_name=holiday_name, holiday_date=holiday_new_date)
            update.save(update_fields=["holiday_name","holiday_date"])
        form = holidaysForm()
        if 'add_new' in request.POST:
            f = form.save(commit=False)
            f.holiday_name = request.POST['holiday_name']
            f.holiday_date = request.POST['holiday_date']
            f.added_by = request.session['user_email']
            date_str = request.POST['holiday_date']  # The date
            format_str = '%m/%d/%Y'  # The format
            datetime_obj = datetime.strptime(date_str, format_str).weekday()

            if datetime_obj == 0:
                f.day = "Monday"
            if datetime_obj == 1:
                f.day = "Tuesday"
            if datetime_obj == 2:
                f.day = "Wednesday"
            if datetime_obj == 3:
                f.day = "Thursday"
            if datetime_obj == 4:
                f.day = "Friday"
            if datetime_obj == 5:
                f.day = "Saturday"
            if datetime_obj == 6:
                f.day = "Sunday"
            f.save()
            return render(request, "dashboard/holidays.html", {'holidays_data': holidays_data})
        return render(request, "dashboard/holidays.html", {'holidays_data': holidays_data})
    elif not permission:
        return redirect("/")

######################################## holidays_edit and delete ############################################

# def edit_holidays(request, holiday_id):
#     if request.method == "POST":
#         holiday_name = request.POST['holiday_name']
#         holiday_date = request.POST['holiday_date']
#         hol_id = request.POST['hol_id']
#         update = designation(holiday_id=hol_id, holiday_name=holiday_name)
#         update.save(update_fields=["holiday_name"])
#
#     else:
#         return render(request, "dashboard/holidays.html", {'holidays_data': holidays_data})


def del_holidays(request,holiday_id):
        aa = holidays(holiday_id=holiday_id)
        aa.delete()
        return render(request, "dashboard/holidays.html",{'aa': aa}, locals())

######################################################################################################333
def leave_admin(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin
        if request.session['user_role_id'] == 1:

            return render(request, "dashboard/leave-admin.html")
        # log in as HR
        elif request.session['user_role_id'] == 2:
            hr_data = user_profile.objects.get(
                user_email=request.session['user_email'])
            leaves_data = tb_employee_leaves.objects.filter(
                Q(emp_cmpy_email=hr_data.user_company_email))
            return render(request, "dashboard/leave-admin.html", {'leaves_data': leaves_data})
        # log in as Employee
        elif request.session['user_role_id'] == 3:
            return redirect("/home")
    elif not permission:
        return redirect("/")


def leave_employee(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin
        if request.session['user_role_id'] == 1:
            return redirect("/home")
        # log in as HR
        elif request.session['user_role_id'] == 2:
            return redirect("/home")
        # log in as Employee
        elif request.session['user_role_id'] == 3:
            emp_data = employee_profile.objects.get(
                Q(employee_official_email=request.session['user_email']))
            leaves_allwd = 4.5
            try:
                leaves_data = tb_employee_leaves.objects.filter(
                    Q(employee_employee_id_id=emp_data.employee_employee_id))
                leaves_allowed = []
                for i in leaves_data:
                    leaves_allowed.append(i.leaves_left_monthly)
                leaves_allwd = float(leaves_allowed[-1])
            except:
                leaves_allwd = 4.5
            if leaves_allwd == 0 or leaves_allwd < 0:

                return render(request, "dashboard/leave-employee.html", {'deny_permission': True})

            if 'short_leave' in request.POST:

                form = leaves_form(request.POST)
                f = form.save(commit=False)
                f.short_leave = True
                f.short_leave_date = date.today()
                f.reason = request.POST['short_leave_reason']
                f.employee_employee_id_id = emp_data.employee_employee_id
                f.emp_cmpy_email = emp_data.employee_company_email
                f.leave_status = 1
                f.save()

            if 'one_day_leave' in request.POST:
                if leaves_allwd == 0 or leaves_allwd < 0:
                    return render(request, "dashboard/leave-employee.html", {'deny_permission': True})
                elif leaves_allwd != 0 or leaves_allwd > 0:
                    leave_type = request.POST.get('one_day_leave_type')
                    if leave_type == "Medical":
                        form = leaves_form(request.POST)
                        f = form.save(commit=False)
                        f.one_day_leave = True
                        f.leave_status = 1
                        f.one_day_leave_date = request.POST['one_day_leave_date']
                        f.reason = request.POST['reason']
                        f.employee_employee_id_id = emp_data.employee_employee_id
                        f.emp_cmpy_email = emp_data.employee_company_email
                        leaves_count_monthly = []
                        for i in leaves_data:
                            leaves_count_monthly.append(i.leaves_left_monthly)
                        leaves_counted_monthly1 = leaves_count_monthly[-1]

                        leaves_counted_monthly2 = float(
                            leaves_counted_monthly1)-1
                        f.leaves_left_monthly = leaves_counted_monthly2
                        f.leave_type = request.POST.get('one_day_leave_type')
                        f.save()
                    elif leave_type == "Casual":
                        form = leaves_form(request.POST)
                        f = form.save(commit=False)
                        f.one_day_leave = True
                        f.leave_status = 1
                        f.one_day_leave_date = request.POST['one_day_leave_date']
                        f.reason = request.POST['reason']
                        f.employee_employee_id_id = emp_data.employee_employee_id
                        f.emp_cmpy_email = emp_data.employee_company_email
                        leaves_count_monthly = []
                        for i in leaves_data:
                            leaves_count_monthly.append(i.leaves_left_monthly)

                        f.leaves_left_monthly = leaves_count_monthly[-1]
                        f.leave_type = request.POST.get('one_day_leave_type')
                        f.save()

            if 'multiple_days' in request.POST:

                from_date = request.POST['from_date']
                to_date = request.POST['to_date']

                date_str1 = from_date
                format_str = '%m/%d/%Y'
                datetime_obj1 = datetime.strptime(date_str1, format_str)
                dayofweek1 = datetime.date(datetime_obj1).strftime("%A")

                date_str2 = to_date
                format_str = '%m/%d/%Y'
                datetime_obj2 = datetime.strptime(date_str2, format_str)
                dayofweek2 = datetime.date(datetime_obj2).strftime("%A")

                if dayofweek1 == "Friday" or dayofweek1 == "Saturday":
                    if dayofweek2 == "Monday":
                        print("SANDWICH")
                if leaves_allwd == 0 or leaves_allwd < 0:
                    pass
                    # if dayofweek1 == dayofweek2:
                    #     form = leaves_form(request.POST)
                    #     f = form.save(commit=False)
                    #     f.leave_type = request.POST.get('leave_type')
                    #     f.leave_from = request.POST['from_date']
                    #     f.leave_to = request.POST['to_date']
                    #     f.leave_policy_type = "LineToLine"
                    #     f.leaves_left_monthly = 0
                    #     f.above_limit_leaves = 2.5
                    #     f.reason = request.POST['reason']
                    #     f.employee_employee_id_id = emp_data.employee_employee_id
                    #     f.save()
                    # if dayofweek1 == "Saturday" or dayofweek2 == "Monday":
                    #     month1 = from_date[:2]
                    #     try:
                    #         crnt_mnt = month1.lstrip("0")
                    #
                    #     except:
                    #         crnt_mnt = int(month1)
                    #
                    #     cal = calendar.monthcalendar(2019, int(crnt_mnt))
                    #     first_week = cal[0]
                    #     second_week = cal[1]
                    #     third_week = cal[2]
                    #     fourth_week = cal[3]
                    #     fifth_week = cal[4]
                    #
                    #     if first_week[calendar.SATURDAY] and fourth_week[calendar.SATURDAY]:
                    #         holi_day_1 = second_week[calendar.SATURDAY]
                    #         holi_day_2 = fourth_week[calendar.SATURDAY]
                    #     else:
                    #         holi_day_1 = third_week[calendar.SATURDAY]
                    #         holi_day_2 = fifth_week[calendar.SATURDAY]
                    #
                    #     # print(from_date[3:5])
                    #     if int(from_date[3:5]) != holi_day_1 or int(from_date[3:5]) != holi_day_2:
                    #         form = leaves_form(request.POST)
                    #         f = form.save(commit=False)
                    #         f.leave_type = request.POST.get('leave_type')
                    #         f.leave_from = request.POST['from_date']
                    #         f.leave_to = request.POST['to_date']
                    #         f.leave_policy_type = "Sandwich"
                    #         f.leaves_left_monthly = 1.5
                    #         f.reason = request.POST['reason']
                    #         f.employee_employee_id_id = emp_data.employee_employee_id
                    #         f.save()
                elif leaves_allwd != 0 or leaves_allwd > 0:
                    d1 = date(2019, 9, 11)
                    date_from = request.POST['from_date']
                    new_lis = date_from.split("/")
                    month, day, year = new_lis

                    month = int(month)
                    day = int(day)
                    year = int(year)

                    date_new_from = d1.replace(year, month, day)
                    date_to = request.POST['to_date']
                    new_lis2 = date_to.split("/")
                    month, day, year = new_lis2
                    month = int(month)
                    day = int(day)
                    year = int(year)
                    date_to = d1.replace(year, month, day)
                    td = date_to - date_new_from
                    print("difference:", td.days, 'days')
                    leave_type = request.POST.get('leave_type')
                    if leave_type == "Casual":
                        if dayofweek1 == dayofweek2:
                            form = leaves_form(request.POST)
                            f = form.save(commit=False)
                            f.leave_type = request.POST.get('leave_type')
                            f.leave_from = request.POST['from_date']
                            f.leave_status = 1
                            f.leave_to = request.POST['to_date']
                            f.leave_policy_type = "LineToLine"
                            f.leaves_left_monthly = 0

                            f.reason = request.POST['reason']
                            f.employee_employee_id_id = emp_data.employee_employee_id
                            f.emp_cmpy_email = emp_data.employee_company_email
                            f.save()
                        elif dayofweek1 == "Saturday" or dayofweek2 == "Monday":
                            month1 = from_date[:2]
                            try:
                                crnt_mnt = month1.lstrip("0")
                            except:
                                crnt_mnt = int(month1)
                            cal = calendar.monthcalendar(2019, int(crnt_mnt))
                            first_week = cal[0]
                            second_week = cal[1]
                            third_week = cal[2]
                            fourth_week = cal[3]
                            fifth_week = cal[4]

                            if first_week[calendar.SATURDAY] and fourth_week[calendar.SATURDAY]:
                                holi_day_1 = second_week[calendar.SATURDAY]
                                holi_day_2 = fourth_week[calendar.SATURDAY]
                            else:
                                holi_day_1 = third_week[calendar.SATURDAY]
                                holi_day_2 = fifth_week[calendar.SATURDAY]

                            # print(from_date[3:5])
                            if int(from_date[3:5]) != holi_day_1 or int(from_date[3:5]) != holi_day_2:
                                form = leaves_form(request.POST)
                                f = form.save(commit=False)
                                f.leave_type = request.POST.get('leave_type')
                                f.leave_from = request.POST['from_date']
                                f.leave_to = request.POST['to_date']
                                f.emp_cmpy_email = emp_data.employee_company_email
                                f.leave_status = 1
                                f.leave_policy_type = "Sandwich"
                                leaves_count_monthly = []
                                for i in leaves_data:
                                    leaves_count_monthly.append(
                                        i.leaves_left_monthly)

                                f.leaves_left_monthly = leaves_count_monthly[-1]
                                f.reason = request.POST['reason']
                                f.employee_employee_id_id = emp_data.employee_employee_id
                                f.save()
                        elif dayofweek1 == "Friday":
                            if dayofweek2 == "Monday":
                                form = leaves_form(request.POST)
                                f = form.save(commit=False)
                                f.leave_type = request.POST.get('leave_type')
                                f.leave_from = request.POST['from_date']
                                f.leave_status = 1
                                f.leave_to = request.POST['to_date']
                                f.emp_cmpy_email = emp_data.employee_company_email
                                f.leave_policy_type = "Sandwich"
                                leaves_count_monthly = []
                                for i in leaves_data:
                                    leaves_count_monthly.append(
                                        i.leaves_left_monthly)

                                f.leaves_left_monthly = leaves_count_monthly[-1]

                                f.reason = request.POST['reason']
                                f.employee_employee_id_id = emp_data.employee_employee_id
                                f.save()
                        else:
                            form = leaves_form(request.POST)
                            f = form.save(commit=False)
                            f.leave_type = request.POST.get('leave_type')
                            f.leave_from = request.POST['from_date']
                            f.leave_to = request.POST['to_date']
                            f.emp_cmpy_email = emp_data.employee_company_email
                            f.leave_status = 1

                            leaves_count_monthly = []
                            for i in leaves_data:
                                leaves_count_monthly.append(
                                    i.leaves_left_monthly)

                            f.leaves_left_monthly = leaves_count_monthly[-1]
                            f.reason = request.POST['reason']
                            f.employee_employee_id_id = emp_data.employee_employee_id
                            f.save()

                    elif leave_type == "Medical":
                        if dayofweek1 == dayofweek2:
                            form = leaves_form(request.POST)
                            f = form.save(commit=False)
                            f.leave_type = request.POST.get('leave_type')
                            f.leave_from = request.POST['from_date']
                            f.leave_status = 1
                            f.leave_to = request.POST['to_date']
                            f.leave_policy_type = "LineToLine"
                            f.leaves_left_monthly = 0
                            f.above_limit_leaves = 2.5
                            f.emp_cmpy_email = emp_data.employee_company_email
                            f.reason = request.POST['reason']
                            f.employee_employee_id_id = emp_data.employee_employee_id
                            f.save()
                        elif dayofweek1 == "Saturday" or dayofweek2 == "Monday":
                            month1 = from_date[:2]
                            try:
                                crnt_mnt = month1.lstrip("0")
                            except:
                                crnt_mnt = int(month1)
                            cal = calendar.monthcalendar(2019, int(crnt_mnt))
                            first_week = cal[0]
                            second_week = cal[1]
                            third_week = cal[2]
                            fourth_week = cal[3]
                            fifth_week = cal[4]

                            if first_week[calendar.SATURDAY] and fourth_week[calendar.SATURDAY]:
                                holi_day_1 = second_week[calendar.SATURDAY]
                                holi_day_2 = fourth_week[calendar.SATURDAY]
                            else:
                                holi_day_1 = third_week[calendar.SATURDAY]
                                holi_day_2 = fifth_week[calendar.SATURDAY]

                            # print(from_date[3:5])
                            if int(from_date[3:5]) != holi_day_1 or int(from_date[3:5]) != holi_day_2:
                                form = leaves_form(request.POST)
                                f = form.save(commit=False)
                                f.leave_type = request.POST.get('leave_type')
                                f.leave_from = request.POST['from_date']
                                f.leave_to = request.POST['to_date']
                                f.emp_cmpy_email = emp_data.employee_company_email
                                f.leave_status = 1
                                f.leave_policy_type = "Sandwich"
                                leaves_count_monthly = []
                                for i in leaves_data:
                                    leaves_count_monthly.append(
                                        i.leaves_left_monthly)
                                leaves_counted_monthly1 = leaves_count_monthly[-1]

                                leaves_counted_monthly2 = float(
                                    leaves_counted_monthly1) - 3
                                f.leaves_left_monthly = leaves_counted_monthly2
                                f.reason = request.POST['reason']
                                if float(leaves_counted_monthly1) <= 0:
                                    f.above_limit_leaves = 3
                                f.employee_employee_id_id = emp_data.employee_employee_id
                                f.save()
                        elif dayofweek1 == "Friday":
                            if dayofweek2 == "Monday":
                                form = leaves_form(request.POST)
                                f = form.save(commit=False)
                                f.leave_type = request.POST.get('leave_type')
                                f.leave_from = request.POST['from_date']
                                f.leave_status = 1
                                f.leave_to = request.POST['to_date']
                                f.emp_cmpy_email = emp_data.employee_company_email
                                f.leave_policy_type = "Sandwich"
                                leaves_count_monthly = []
                                for i in leaves_data:
                                    leaves_count_monthly.append(
                                        i.leaves_left_monthly)
                                leaves_counted_monthly1 = leaves_count_monthly[-1]

                                leaves_counted_monthly2 = float(
                                    leaves_counted_monthly1) - 4
                                f.leaves_left_monthly = leaves_counted_monthly2
                                if float(leaves_counted_monthly1) <= 0:
                                    f.above_limit_leaves = 4
                                f.reason = request.POST['reason']
                                f.employee_employee_id_id = emp_data.employee_employee_id
                                f.save()
                        else:
                            form = leaves_form(request.POST)
                            f = form.save(commit=False)
                            f.leave_type = request.POST.get('leave_type')
                            f.leave_from = request.POST['from_date']
                            f.leave_to = request.POST['to_date']
                            f.emp_cmpy_email = emp_data.employee_company_email
                            f.leave_status = 1

                            leaves_count_monthly = []
                            for i in leaves_data:
                                leaves_count_monthly.append(
                                    i.leaves_left_monthly)
                            leaves_counted_monthly1 = leaves_count_monthly[-1]

                            leaves_counted_monthly2 = float(
                                leaves_counted_monthly1) - float(td.days)
                            f.leaves_left_monthly = leaves_counted_monthly2
                            if float(leaves_counted_monthly1) <= 0:
                                f.above_limit_leaves = float(td.days)
                            f.reason = request.POST['reason']
                            f.employee_employee_id_id = emp_data.employee_employee_id
                            f.save()

            if 'half_day_leave' in request.POST:
                if leaves_allwd == 0 or leaves_allwd < 0:
                    return render(request, "dashboard/leave-employee.html", {'deny_permission': True})

                elif leaves_allwd != 0 or leaves_allwd > 0:
                    # print("above zero")
                    leave_type = request.POST.get('half_day_leave_type')
                    if leave_type == "Medical":
                        form = leaves_form(request.POST)
                        f = form.save(commit=False)
                        f.half_day_leave = True
                        f.leave_status = 1
                        f.half_day_leave_date = request.POST['half_day_date']
                        f.reason = request.POST['reason']
                        f.employee_employee_id_id = emp_data.employee_employee_id
                        f.emp_cmpy_email = emp_data.employee_company_email
                        leaves_count_monthly = []
                        for i in leaves_data:
                            leaves_count_monthly.append(i.leaves_left_monthly)
                        leaves_counted_monthly1 = leaves_count_monthly[-1]

                        leaves_counted_monthly2 = float(
                            leaves_counted_monthly1)-0.5
                        f.leaves_left_monthly = leaves_counted_monthly2
                        f.leave_type = request.POST.get('half_day_leave_type')
                        f.save()
                    elif leave_type == "Casual":
                        form = leaves_form(request.POST)
                        f = form.save(commit=False)
                        f.half_day_leave = True
                        f.leave_status = 1
                        f.half_day_leave_date = request.POST['half_day_date']
                        f.reason = request.POST['reason']
                        leaves_count_monthly = []
                        for i in leaves_data:
                            leaves_count_monthly.append(i.leaves_left_monthly)

                        f.leaves_left_monthly = leaves_count_monthly[-1]
                        f.employee_employee_id_id = emp_data.employee_employee_id
                        f.emp_cmpy_email = emp_data.employee_company_email
                        f.leave_type = request.POST.get('half_day_leave_type')
                        f.save()
                # 'leave_type',
                #  'leave_from',
                #   'leave_to',
                #    'one_day_leave',
                #    'one_day_leave_date',
                #     'half_day_leave',
                #      'half_day_leave_date',
                #      'short_leave',
                #       'short_leave_date',
                #       'employee_employee_id',
                #        'emp_cmpy_email',
                #        'emp_hr_email',
                #        'leave_status',
                #        'leaves_left_monthly',
                #        'above_limit_leaves', 'reason', 'leave_policy_type', )
            return render(request, "dashboard/leave-employee.html")
    elif not permission:
        return redirect("/")


def leave_setting(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin
        if request.session['user_role_id'] == 1:
            return render(request, "dashboard/leave-setting.html")
        # log in as HR
        elif request.session['user_role_id'] == 2:
            return render(request, "dashboard/leave-setting.html")
        # log in as Employee
        elif request.session['user_role_id'] == 3:
            return redirect("/home")
    elif not permission:
        return redirect("/")


def leave_type(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin
        if request.session['user_role_id'] == 1:
            return render(request, "dashboard/leave-type.html")
        # log in as HR
        elif request.session['user_role_id'] == 2:
            return render(request, "dashboard/leave-type.html")
        # log in as Employee
        elif request.session['user_role_id'] == 3:
            return redirect("/home")
    elif not permission:
        return redirect("/")


def lock_screen(request):
    return render(request, "dashboard/lock-screen.html")


def otp(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin
        if request.session['user_role_id'] == 1:
            return render(request, "dashboard/otp.html")
        # log in as HR
        elif request.session['user_role_id'] == 2:
            return render(request, "dashboard/otp.html")
        # log in as Employee
        elif request.session['user_role_id'] == 3:
            return render(request, "dashboard/otp.html")
    elif not permission:
        return redirect("/")


def overtime(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin
        if request.session['user_role_id'] == 1:
            return render(request, "dashboard/overtime.html")
        # log in as HR
        elif request.session['user_role_id'] == 2:
            return render(request, "dashboard/overtime.html")
        # log in as Employee
        elif request.session['user_role_id'] == 3:
            return redirect("/home")
    elif not permission:
        return redirect("/")


def payroll_item(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin
        if request.session['user_role_id'] == 1:
            return render(request, "dashboard/payroll-item.html")
        # log in as HR
        elif request.session['user_role_id'] == 2:
            return render(request, "dashboard/payroll-item.html")
        # log in as Employee
        elif request.session['user_role_id'] == 3:
            return render(request, "dashboard/payroll-item.html")
    elif not permission:
        return redirect("/")


def payslip(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin
        if request.session['user_role_id'] == 1:
            return render(request, "dashboard/payslip.html")
        # log in as HR
        elif request.session['user_role_id'] == 2:
            return render(request, "dashboard/payslip.html")
        # log in as Employee
        elif request.session['user_role_id'] == 3:
            return render(request, "dashboard/payslip.html")
    elif not permission:
        return redirect("/")


def permotion(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin
        if request.session['user_role_id'] == 1:
            return render(request, "dashboard/permotion.html")
        # log in as HR
        elif request.session['user_role_id'] == 2:
            return render(request, "dashboard/permotion.html")
        # log in as Employee
        elif request.session['user_role_id'] == 3:
            return redirect("/home")
    elif not permission:
        return redirect("/")


def privacy_policy(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        return render(request, "dashboard/privacy-policy.html")
    elif not permission:
        return redirect("/")


def profile_func(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin
        if request.session['user_role_id'] == 1:
            return redirect("/home")
        # log in as HR
        elif request.session['user_role_id'] == 2:
            return redirect("/home")
        # log in as Employee
        elif request.session['user_role_id'] == 3:
            employee_data = employee_profile.objects.get(
                Q(employee_official_email=request.session['user_email']))
            bank_details_emp = ""
            try:
                bank_details_emp = employee_bank_details.objects.get(
                    Q(employee_employee_id_id=employee_data.employee_employee_id))
            except:
                bank_details_emp = ""
            return render(request, "dashboard/profile.html", {'employee_data': employee_data, 'bank_details_emp': bank_details_emp})
    elif not permission:
        return redirect("/")


def register(request):
    return render(request, "dashboard/register.html")


def resignation(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin
        if request.session['user_role_id'] == 1 or request.session['user_role_id'] == 2:
            return redirect("/home")

        # log in as Employee
        elif request.session['user_role_id'] == 3:
            return render(request, "dashboard/resignation.html")
    elif not permission:
        return redirect("/")


def salary_setting(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin
        if request.session['user_role_id'] == 1:
            return render(request, "dashboard/salary-setting.html")
        # log in as HR
        elif request.session['user_role_id'] == 2:
            return render(request, "dashboard/salary-setting.html")
        # log in as Employee
        elif request.session['user_role_id'] == 3:
            return redirect("/home")
    elif not permission:
        return redirect("/")


def setting_func(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin
        if request.session['user_role_id'] == 1:
            company_data = company_profile.objects.get(
                company_user_email=request.session['user_email'])
            form = companyForm()
            if company_data.profile_updated:
                update_company_data = company_profile.objects.get(
                    company_user_email=request.session['user_email'])
                if request.method == "POST":
                    company_name = request.POST['company_name']
                    contact_person = request.POST['contact_person']
                    address = request.POST['address']
                    country = request.POST['country']
                    city = request.POST['city']
                    postal_code = request.POST['postal_code']
                    state_province = request.POST['state_province']
                    mobile_number = request.POST['mobile_number']
                    phone_number = request.POST['phone_number']
                    phone_number = request.POST['phone_number']
                    fax = request.POST['fax']
                    website_url = request.POST['website_url']
                    update_company_info = company_profile(company_user_email=request.session['user_email'],
                                                          company_name=company_name,
                                                          contact_person=contact_person,
                                                          address=address,
                                                          country=country,
                                                          city=city,
                                                          postal_code=postal_code,
                                                          state_province=state_province,
                                                          phone_number=phone_number,
                                                          mobile_number=mobile_number,
                                                          fax=fax,
                                                          website_url=website_url)
                    update_company_info.save(update_fields=['company_name', 'contact_person', 'address', 'country', 'city', 'postal_code',
                                                            'state_province', 'phone_number', 'mobile_number', 'fax', 'website_url'])

                return render(request, "dashboard/update-settings.html", {'profile_updated': company_data.profile_updated, 'update_company_data': update_company_data})
            elif not company_data.profile_updated:
                if request.method == "POST":
                    form = companyForm(request.POST)
                    if form.is_valid():
                        company_name = request.POST['company_name']
                        contact_person = request.POST['contact_person']
                        address = request.POST['address']
                        country = request.POST['country']
                        city = request.POST['city']
                        mobile_number = request.POST['mobile_number']
                        postal_code = request.POST['postal_code']
                        state_province = request.POST['state_province']
                        phone_number = request.POST['phone_number']
                        fax = request.POST['fax']
                        website_url = request.POST['website_url']
                        company_obj = company_profile(company_user_email=request.session['user_email'], company_name=company_name,
                                                      contact_person=contact_person,
                                                      address=address, country=country, city=city,
                                                      postal_code=postal_code,
                                                      state_province=state_province, phone_number=phone_number,
                                                      fax=fax, website_url=website_url, profile_updated=True,
                                                      mobile_number=mobile_number)
                        company_obj.save(
                            update_fields=['company_name', 'contact_person', 'address', 'country', 'city',
                                           'postal_code',
                                           'state_province',
                                           'phone_number', 'fax', 'website_url', 'profile_updated', 'mobile_number'])
                        form = companyForm(request.POST)
                        return render(request, "dashboard/setting.html", {'form': form, 'profile_updated': False,
                                                                          'updated_message': True})
                    elif not form.is_valid():
                        form = companyForm(request.POST)
                        return render(request, "dashboard/setting.html", {'form': form, 'profile_updated': False})
                form = companyForm()
                return render(request, "dashboard/setting.html", {'form': form, 'profile_updated': company_data.profile_updated})

        # log in as HR
        elif request.session['user_role_id'] == 2:
            return redirect("/home")
        # log in as Employee
        elif request.session['user_role_id'] == 3:
            employee_total_data = employee_profile.objects.get(
                Q(employee_official_email=request.session['user_email']))
            bank_details_emp = ""
            try:
                bank_details_emp = employee_bank_details.objects.get(
                    Q(employee_employee_id_id=employee_total_data.employee_employee_id))
            except:
                bank_details_emp = ""

            if 'update_profile' in request.POST:
                update_profile_info = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                       request_status=0, permission_to_edit=False, updated_once=True)
                update_profile_info.save(
                    update_fields=['request_status', 'permission_to_edit', 'updated_once'])

                return redirect("/home")

            if 'update_basic' in request.POST:
                first_name = request.POST['first_name']

                if first_name != "":
                    update_basic_info = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                         employee_firstname=first_name)
                    update_basic_info.save(
                        update_fields=['employee_firstname'])

                last_name = request.POST['last_name']
                if last_name != "":
                    update_basic_info = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                         employee_lastname=last_name,)
                    update_basic_info.save(
                        update_fields=['employee_lastname'])

                birthday = request.POST['birthday']
                if birthday != "":
                    update_basic_info = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                         birthday=birthday)
                    update_basic_info.save(update_fields=['birthday'])

                phone_number = request.POST['phone_number']
                if phone_number != "":
                    update_basic_info = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                         employee_phone=phone_number)
                    update_basic_info.save(
                        update_fields=['employee_phone'])
                gender = request.POST.get('gender')
                if gender != "" and gender is not None:

                    update_basic_info = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                         gender=gender)
                    update_basic_info.save(update_fields=['gender'])

                address = request.POST['address']
                if address != "":
                    update_basic_info = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                         address=address)
                    update_basic_info.save(update_fields=['address'])
                return render(request, "dashboard/update-settings.html",
                              {'employee_total_data': employee_total_data, 'bank_details_emp': bank_details_emp})
            if 'update_bank_details' in request.POST:
                form = empBankDetailsForm(request.POST)
                f = form.save(commit=False)
                f.employee_employee_id_id = employee_total_data.employee_employee_id
                f.bank_name = request.POST['bank_name']
                f.account_no = request.POST['account_number']
                f.ifsc_code = request.POST['ifsc_code']
                f.pan = request.POST['pan_number']
                f.save()
                return render(request, "dashboard/update-settings.html",
                              {'employee_total_data': employee_total_data, 'bank_details_emp': bank_details_emp})
            if 'school_details' in request.POST:
                try:
                    master_college_name = request.POST['master_college_name']
                    master_course_name = request.POST['master_course_name']
                    master_college_details = request.POST['master_college_details']
                    master_start_year = request.POST['master_start_year']
                    master_end_year = request.POST['master_end_year']

                    graduation_college_name = request.POST['graduation_collaege_name']
                    graduation_course_name = request.POST['graduation_course_name']
                    graduation_college_details = request.POST['graduation_college_details']
                    graduation_start_year = request.POST['graduation_start_year']
                    graduation_end_year = request.POST['graduation_end_year']

                    senior_school_name = request.POST['senior_school_name']
                    senior_school_board = request.POST['senior_school_board']
                    senior_school_details = request.POST['senior_school_details']
                    senior_school_end_year = request.POST['senior_school_end_year']

                    matric_school_name = request.POST['matric_school_name']
                    matric_school_board = request.POST['matric_school_board']
                    matric_school_details = request.POST['matric_school_details']
                    matric_school_end_year = request.POST['matric_school_end_year']

                    update_school_info = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                          masters_college_name=master_college_name,
                                                          masters_college_course_name=master_course_name,
                                                          masters_college_details=master_college_details,
                                                          masters_start_year=master_start_year,
                                                          masters_complete_year=master_end_year,
                                                          graduation_college_name=graduation_college_name,
                                                          graduation_college_course_name=graduation_course_name,
                                                          graduation_college_details=graduation_college_details,
                                                          graduation_start_year=graduation_start_year,
                                                          graduation_complete_year=graduation_end_year,
                                                          sec_schl_name=senior_school_name,
                                                          sec_schl_board=senior_school_board,
                                                          sec_schl_details=senior_school_details,
                                                          sec_schl_complete_year=senior_school_end_year,
                                                          matric_schl_name=matric_school_name,
                                                          matric_schl_board=matric_school_board,
                                                          matric_schl_details=matric_school_details,
                                                          matric_schl_complete_year=matric_school_end_year)
                    update_school_info.save(update_fields=['masters_college_name', 'masters_college_course_name', 'masters_college_details',
                                                           'masters_start_year', 'masters_complete_year', 'graduation_college_name',
                                                           'graduation_college_course_name', 'graduation_college_details', 'graduation_start_year',
                                                           'graduation_complete_year', 'sec_schl_name', 'sec_schl_board', 'sec_schl_details',
                                                           'sec_schl_complete_year', 'matric_schl_name', 'matric_schl_board', 'matric_schl_details',
                                                           'matric_schl_complete_year'])
                except:
                    return render(request, "dashboard/update-settings.html", {'employee_total_data': employee_total_data, 'bank_details_emp': bank_details_emp})
            if 'request_to_edit' in request.POST:

                # request_status 1 = waiting
                update_request_data = employee_profile(
                    employee_employee_id=employee_total_data.employee_employee_id,
                    request_status=1, edit_request_emp_email=request.session['user_email'], edit_request_by_emp=True)

                update_request_data.save(update_fields=[
                                         'request_status', 'edit_request_emp_email', 'edit_request_by_emp'])
            return render(request, "dashboard/update-settings.html", {'employee_total_data': employee_total_data, 'bank_details_emp': bank_details_emp})

    elif not permission:
        return redirect("/")


def termination_func(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin
        if request.session['user_role_id'] == 1:
            form = terminationForm()
            if request.method == "POST":
                employee_id = request.POST['Emp_id']
                emp_data = employee_profile.objects.get(
                    employee_employee_id=employee_id)
                if emp_data:
                    f = form.save(commit=False)
                    f.employee_employee_id_id = request.POST['Emp_id']
                    f.reason = request.POST['reason']
                    f.termination_type = request.POST.get(
                        'termination_type')
                    f.termination_date = request.POST['termination_date']
                    f.request_status = 2
                    f.terminate_request_by = "Company Admin"
                    f.company_email = request.session['user_email']
                    f.hr_email = ""
                    f.termination_notice_date = request.POST['notice_date']
                    f.save()
                    print(7)
                elif not emp_data:
                    return render(request, "dashboard/termination.html",
                                  {'invalid_employee_id': True})
            return render(request, "dashboard/termination.html")
        # log in as HR
        elif request.session['user_role_id'] == 2:
            form = terminationForm()
            if request.method == "POST":
                employee_id = request.POST['Emp_id']
                try:
                    if employee_profile.objects.get(Q(employee_employee_id=employee_id)):
                        f = form.save(commit=False)
                        f.employee_employee_id_id = request.POST['Emp_id']
                        f.reason = request.POST['reason']
                        f.termination_type = request.POST.get(
                            'termination_type')
                        f.termination_date = request.POST['termination_date']
                        f.request_status = 1
                        hr_profile = user_profile.objects.get(
                            user_email=request.session['user_email'])
                        f.terminate_request_by = hr_profile.username
                        f.company_email = hr_profile.user_company_email
                        f.hr_email = request.session['user_email']
                        f.termination_notice_date = request.POST['notice_date']
                        f.save()
                except:
                    return render(request, "dashboard/termination.html",
                                  {'invalid_employee_id': True})
            return render(request, "dashboard/termination.html")
        # log in as Employee
        elif request.session['user_role_id'] == 3:
            return redirect("/home")
    elif not permission:
        return redirect("/")


def timesheet(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:

        def terms_condition(request):
            try:
                permission = request.session['user_is_authenticated']
            except:
                permission = False
            if permission:
                return render(request, "dashboard/terms&condition.html")
            elif not permission:
                return redirect("/")

        # log in as admin
        if request.session['user_role_id'] == 1:
            return render(request, "dashboard/timesheet.html")
        # log in as HR
        elif request.session['user_role_id'] == 2:
            return render(request, "dashboard/timesheet.html")
        # log in as Employee
        elif request.session['user_role_id'] == 3:
            return redirect("/home")
    elif not permission:
        return redirect("/")


def designations_details(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin
        if request.session['user_role_id'] == 1 or request.session['user_role_id'] == 2:
            selected_department = request.GET.get('selected_department_id')

            designations_data = designation.objects.filter(
                department_id_id=selected_department)
            dic = {}
            for c in designations_data:
                dic[c.designation_id] = c.designation_name

            return JsonResponse(dic, safe=False)
        # log in as Employee
        elif request.session['user_role_id'] == 3:
            return redirect("/home")
    elif not permission:
        return redirect("/")


def users(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        profile_roles = roles.objects.all()
        # if user logged in is admin
        if request.session['user_role_id'] == 1:
            added_users_data = user_profile.objects.filter(
                Q(user_company_email=request.session['user_email']))
            if request.method == "POST":
                form = user_profileForm(request.POST)
                if form.is_valid():
                    f = form.save(commit=False)
                    first_password = request.POST['first_password']
                    final_password = request.POST['user_password']
                    # True if both entered password matches
                    if first_password == final_password:
                        user_email = request.POST['user_email']
                        # True if entered email already exists in database
                        if user_profile.objects.filter(user_email=user_email) or company_profile.objects.filter(company_user_email=user_email)\
                                or employee_profile.objects.filter(employee_official_email=user_email):

                            form = user_profileForm(request.POST)
                            return render(request, "dashboard/user.html", {'profile_roles': profile_roles,
                                                                           'email_already_exists': True, 'form': form,
                                                                           'added_users_data': added_users_data})
                        # Enter data if password matches,email not already exists and all conditions are true
                        else:
                            role_id_id = request.POST.get('role_selected')
                            if role_id_id is None:
                                form = user_profileForm(request.POST)
                                return render(request, "dashboard/user.html", {'profile_roles': profile_roles,
                                                                               'role_not_selected': True, 'form': form,
                                                                               'added_users_data': added_users_data})
                            elif role_id_id is not None:
                                f.role_id_id = request.POST.get(
                                    'role_selected')
                                f.user_email = request.POST['user_email']
                                f.role_id_id = request.POST.get(
                                    'role_selected')
                                f.user_firstname = request.POST['user_firstname']
                                f.user_lastname = request.POST['user_lastname']
                                f.username = request.POST['username']
                                f.user_email = request.POST['user_email']
                                f.user_password = make_password(
                                    request.POST['user_password'])
                                f.user_phone = request.POST['user_phone']
                                f.user_company_email = request.POST['company_email']
                                company_name_data = company_profile.objects.get(
                                    company_user_email=request.POST['company_email'])
                                f.user_company = company_name_data.company_name
                                user_first_name = request.POST['user_firstname']
                                user_first_name = user_first_name.upper()
                                f.user_employee_id = user_first_name[:3] + str(
                                    random.randint(0, 99999))
                                latest_user_emp = f.user_employee_id
                                f.employee_read = False
                                employee_read = request.POST.get(
                                    'employee_read')
                                if employee_read:
                                    f.employee_read = employee_read
                                elif employee_read is None:
                                    f.employee_read = 0

                                employee_create = request.POST.get(
                                    'employee_create')
                                if employee_create:
                                    f.employee_create = employee_create

                                elif employee_create is None:
                                    f.employee_create = 0

                                employee_edit = request.POST.get(
                                    'employee_write')
                                if employee_edit:
                                    f.employee_edit = employee_edit
                                elif employee_edit is None:
                                    f.employee_edit = 0

                                employee_delete = request.POST.get(
                                    'employee_delete')
                                if employee_delete:
                                    f.employee_delete = employee_delete
                                elif employee_delete is None:
                                    f.employee_delete = 0

                                leaves_read = request.POST.get('leaves_read')
                                if leaves_read:
                                    f.leaves_read = leaves_read
                                elif leaves_read is None:
                                    f.leaves_read = 0

                                leaves_create = request.POST.get(
                                    'leaves_create')
                                if leaves_create:
                                    f.leaves_create = leaves_create
                                elif leaves_create is None:
                                    f.leaves_create = 0

                                leaves_edit = request.POST.get('leaves_write')
                                if leaves_edit:
                                    f.leaves_edit = leaves_edit
                                elif leaves_edit is None:
                                    f.leaves_edit = 0

                                leaves_delete = request.POST.get(
                                    'leaves_delete')
                                if leaves_delete:
                                    f.leaves_delete = leaves_delete
                                elif leaves_delete is None:
                                    f.leaves_delete = 0

                                holidays_read = request.POST.get(
                                    'holidays_read')
                                if holidays_read:
                                    f.holidays_read = holidays_read
                                elif holidays_read is None:
                                    f.holidays_read = 0

                                holidays_create = request.POST.get(
                                    'holidays_create')
                                if holidays_create:
                                    f.holidays_create = holidays_create
                                elif holidays_create is None:
                                    f.holidays_create = 0

                                holidays_edit = request.POST.get(
                                    'holidays_write')
                                if holidays_edit:
                                    f.holidays_edit = holidays_edit
                                elif holidays_edit is None:
                                    f.holidays_edit = 0

                                holidays_delete = request.POST.get(
                                    'holidays_delete')
                                if holidays_delete:
                                    f.holidays_delete = holidays_delete
                                elif holidays_delete is None:
                                    f.holidays_delete = 0

                                event_read = request.POST.get('event_read')
                                if event_read:
                                    f.event_read = event_read
                                elif event_read is None:
                                    f.event_read = 0

                                event_create = request.POST.get('event_create')
                                if event_create:
                                    f.event_create = event_create
                                elif event_create is None:
                                    f.event_create = 0

                                event_edit = request.POST.get('event_write')
                                if event_edit:
                                    f.event_edit = event_edit
                                elif event_create is None:
                                    f.event_edit = 0

                                event_delete = request.POST.get('event_delete')
                                if event_delete:
                                    f.event_delete = event_delete
                                elif event_delete is None:
                                    f.event_delete = False

                                f.is_active = True
                                f.created_date = date.today()
                                f.save()
                                form = user_profileForm()
                                return render(request, "dashboard/user.html", {'profile_roles': profile_roles, 'user_added': True,
                                                                               'form': form,
                                                                               'added_users_data': added_users_data,
                                                                               'latest_added_emp': latest_user_emp})

                    # False if both entered password not matches
                    elif first_password != final_password:
                        form = user_profileForm(request.POST)
                        return render(request, "dashboard/user.html", {'profile_roles': profile_roles,
                                                                       'passwrd_err': True, 'form': form,
                                                                       'added_users_data': added_users_data})

                elif not form.is_valid():
                    form = user_profileForm(request.POST)
                    return render(request, "dashboard/user.html", {'profile_roles': profile_roles, 'form': form,
                                                                   'added_users_data': added_users_data})
            form = user_profileForm()
            return render(request, "dashboard/user.html", {'profile_roles': profile_roles, 'form': form,
                                                           'added_users_data': added_users_data})
        # if user logged in is HR
        elif request.session['user_role_id'] == 2:
            departments = department.objects.all()
            added_emp_data = employee_profile.objects.all()
            if request.method == "POST":

                form = employeeForm(request.POST)
                if form.is_valid():

                    f = form.save(commit=False)
                    first_password = request.POST['first_password']
                    final_password = request.POST['employee_password']

                    # True if both entered password matches
                    if first_password == final_password:

                        user_email = request.POST['employee_official_email']

                        # True if entered email already exists in database
                        if user_profile.objects.filter(user_email=user_email) or company_profile.objects.filter(company_user_email=user_email)\
                                or employee_profile.objects.filter(employee_official_email=user_email):

                            form = employeeForm(request.POST)
                            return render(request, "dashboard/user.html", {'profile_roles': profile_roles,
                                                                           'email_already_exists': True, 'form': form,
                                                                           'departments': departments,
                                                                           'added_emp_data': added_emp_data})
                        # Enter data if password matches,email not already exists and all conditions are true
                        else:

                            department_id_id = request.POST.get(
                                'selected_department')
                            designation_id_id = request.POST.get(
                                'selected_designation')
                            if department_id_id is None:

                                form = employeeForm(request.POST)
                                return render(request, "dashboard/user.html", {'profile_roles': profile_roles,
                                                                               'department_not_selected': True,
                                                                               'form': form,
                                                                               'departments': departments,
                                                                               'added_emp_data': added_emp_data})
                            elif designation_id_id is None:

                                form = employeeForm(request.POST)
                                return render(request, "dashboard/user.html", {'profile_roles': profile_roles,
                                                                               'designation_not_selected': True,
                                                                               'form': form,
                                                                               'departments': departments,
                                                                               'added_emp_data': added_emp_data})
                            elif department_id_id is not None and designation_id_id is not None:

                                f.employee_official_email = request.POST['employee_official_email']
                                f.employee_personal_email = ""
                                f.role_id_id = 3
                                f.department_id_id = request.POST.get(
                                    'selected_department')
                                f.designation_id_id = request.POST.get(
                                    'selected_designation')
                                f.employee_firstname = request.POST['employee_firstname']
                                f.employee_lastname = request.POST['employee_lastname']
                                f.employee_username = request.POST['employee_username']
                                f.terminated_date = ""
                                f.employee_password = make_password(
                                    request.POST['employee_password'])
                                f.employee_phone = request.POST['employee_phone']
                                hr_data = user_profile.objects.get(
                                    user_email=request.session['user_email'])
                                f.employee_company_email = hr_data.user_company
                                f.employee_company = hr_data.user_company
                                f.employee_hr_name = hr_data.username
                                f.employee_company_email = hr_data.user_company_email
                                f.employee_hr_email = request.session['user_email']
                                first_name = request.POST['employee_firstname']
                                first_name = first_name.upper()
                                f.employee_employee_id = first_name[:3] + str(
                                    random.randint(0, 99999))
                                latest_employee_id = f.employee_employee_id
                                f.profile_edit = False
                                f.added_by = request.session['user_email']
                                f.edited_by = ""
                                f.deleted_by = ""
                                f.is_terminated = False
                                f.terminated_by = ""
                                f.promoted_by = ""
                                f.is_active = True
                                f.created_date = date.today()
                                f.terminated_date = ""
                                f.gender = ""
                                f.birthday = ""
                                f.address = ""
                                f.martial_status = ""
                                f.masters_college_name = ""
                                f.masters_college_course_name = ""
                                f.masters_college_details = ""
                                f.masters_start_year = ""
                                f.masters_complete_year = ""
                                f.graduation_college_name = ""
                                f.graduation_college_course_name = ""
                                f.graduation_college_details == ""
                                f.graduation_start_year = ""
                                f.graduation_complete_year = ""
                                f.sec_schl_name = ""
                                f.sec_schl_board = ""
                                f.sec_schl_details = ""
                                f.sec_schl_complete_year = ""
                                f.matric_schl_name = ""
                                f.matric_schl_board = ""
                                f.matric_schl_details = ""
                                f.matric_schl_complete_year = ""
                                f.permission_to_edit = False
                                f.updated_once = False
                                f.request_status = 0
                                f.edit_request_emp_email = ""
                                f.edit_request_hr_email = ""
                                f.edit_request_by_emp = False
                                f.edit_request_by_hr = False
                                f.save()
                                form = employeeForm()
                                return render(request, "dashboard/user.html", {'profile_roles': profile_roles, 'user_added': True,
                                                                               'form': form, 'departments': departments,
                                                                               'added_emp_data': added_emp_data,
                                                                               'latest_employee_id': latest_employee_id})

                    # False if both entered password not matches
                    elif first_password != final_password:

                        form = employeeForm(request.POST)
                        return render(request, "dashboard/user.html", {'profile_roles': profile_roles,
                                                                       'passwrd_err': True, 'form': form,
                                                                       'departments': departments,
                                                                       'added_emp_data': added_emp_data})

                elif not form.is_valid():

                    form = employeeForm(request.POST)
                    return render(request, "dashboard/user.html", {'profile_roles': profile_roles, 'form': form,
                                                                   'departments': departments,
                                                                   'added_emp_data': added_emp_data})
            form = employeeForm()
            return render(request, "dashboard/user.html", {'profile_roles': profile_roles,
                                                           'form': form,
                                                           'departments': departments,
                                                           'added_emp_data': added_emp_data})
        elif request.session['user_role_id'] == 3:
            return redirect("/home")
    elif not permission:
        return redirect("/")


def employeelist(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin
        if request.session['user_role_id'] == 1 or request.session['user_role_id'] == 2:
            return render(request, "dashboard/employeelist.html")

        # log in as Employee
        elif request.session['user_role_id'] == 3:
            return redirect("/home")
    elif not permission:
        return redirect("/")


"""
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('../')
    else:
        form = SignUpForm()
    return render(request,'dashboard/signup.html',locals())

"""


def logout(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False

    if permission:
        del request.session['user_email']
        del request.session['user_role_id']
        del request.session['user_is_authenticated']
        return redirect("/")
    elif not permission:
        return redirect("/")


def update_profile_func(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    # if permission:
    #     # log in as admin
    #     if request.session['user_role_id'] == 1:
    #     # log in as HR
    #     elif request.session['user_role_id'] == 2:
    #     # log in as Employee
    #     elif request.session['user_role_id'] == 3:
    # elif not permission:
    #     return redirect("/")
    pass

# details to be added by HR


def search_added_user(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as admin
        if request.session['user_role_id'] == 1 or request.session['user_role_id'] == 2:
            if 'search-button' in request.POST:
                id_or_email = request.POST['search_content']
                try:

                    employee_total_data = employee_profile.objects.get(Q(employee_official_email=id_or_email) |
                                                                       Q(employee_personal_email=id_or_email) |
                                                                       Q(employee_employee_id=id_or_email))
                    return render(request, "dashboard/added-employee.html", {'found': True,
                                                                             'employee_total_data': employee_total_data})
                except:
                    return render(request, "dashboard/added-employee.html", {'found': False, 'not_found': True})

            return render(request, "dashboard/added-employee.html", {'not_found': False})

        elif request.session['user_role_id'] == 3:
            return redirect("/home")
    elif not permission:
        return redirect("/")


def user_profile_details_func(request):
    try:
        permission = request.session['user_is_authenticated']
    except:
        permission = False
    if permission:
        # log in as HR
        if request.session['user_role_id'] == 2:
            id_or_email = request.GET['user-id']

            employee_total_data = employee_profile.objects.get(Q(employee_official_email=id_or_email) |
                                                               Q(employee_personal_email=id_or_email) |
                                                               Q(employee_employee_id=id_or_email))
            bank_details_emp = ""
            try:
                bank_details_emp = employee_bank_details.objects.get(
                    Q(employee_employee_id_id=employee_total_data.employee_employee_id))
            except:
                bank_details_emp = ""
            edited_request = False
            deleted_request = False
            if not employee_total_data.permission_to_edit and employee_total_data.updated_once:
                if 'request_to_edit' in request.POST:
                    # request_status 1 = waiting

                    hr_profile = user_profile.objects.get(
                        user_email=request.session['user_email'])
                    update_request_data = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                           request_status=1, edit_request_hr_email=request.session['user_email'], edit_request_by_hr=True)

                    update_request_data.save(
                        update_fields=['request_status', 'edit_request_hr_email', 'edit_request_by_hr'])
                    edited_request = True
                if 'request_to_delete' in request.POST:
                    # request_status 1 = waiting

                    hr_profile = user_profile.objects.get(
                        user_email=request.session['user_email'])
                    update_request_data = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                           request_status=4, edit_request_hr_email=request.session['user_email'])

                    update_request_data.save(
                        update_fields=['request_status', 'edit_request_hr_email', 'edit_request_by_hr'])
                    deleted_request = True
                return render(request, "dashboard/update-added-employee.html",
                              {'employee_total_data': employee_total_data, 'permission_not_to_edit': True, 'edited_request': edited_request,
                               'deleted_request': deleted_request, 'bank_details_emp': bank_details_emp})

            if not employee_total_data.updated_once or employee_total_data.permission_to_edit:
                if 'update_profile' in request.POST:
                    update_profile_info = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                           request_status=0, permission_to_edit=False, updated_once=True)
                    update_profile_info.save(
                        update_fields=['request_status', 'permission_to_edit', 'updated_once'])

                    return redirect("/home")

                if 'update_basic' in request.POST:
                    first_name = request.POST['first_name']

                    if first_name != "":
                        update_basic_info = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                             employee_firstname=first_name)
                        update_basic_info.save(
                            update_fields=['employee_firstname'])

                    last_name = request.POST['last_name']
                    if last_name != "":
                        update_basic_info = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                             employee_lastname=last_name,)
                        update_basic_info.save(
                            update_fields=['employee_lastname'])

                    birthday = request.POST['birthday']
                    if birthday != "":
                        update_basic_info = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                             birthday=birthday)
                        update_basic_info.save(update_fields=['birthday'])

                    phone_number = request.POST['phone_number']
                    if phone_number != "":
                        update_basic_info = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                             employee_phone=phone_number)
                        update_basic_info.save(
                            update_fields=['employee_phone'])

                    personal_email = request.POST['personal_email']
                    if personal_email != "":
                        update_basic_info = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                             employee_personal_email=personal_email)
                        update_basic_info.save(
                            update_fields=['employee_personal_email'])

                    martial = request.POST.get('martial')
                    if martial != "":
                        update_basic_info = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                             martial_status=phone_number)
                        update_basic_info.save(
                            update_fields=['martial_status'])

                    gender = request.POST.get('gender')
                    if gender != "" and gender is not None:

                        update_basic_info = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                             gender=gender)
                        update_basic_info.save(update_fields=['gender'])

                    address = request.POST['address']
                    if address != "":
                        update_basic_info = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                             address=address)
                        update_basic_info.save(update_fields=['address'])
                    return render(request, "dashboard/update-added-employee.html",
                                  {'employee_total_data': employee_total_data, 'bank_details_emp': bank_details_emp})
                if 'update_bank_details' in request.POST:
                    form = empBankDetailsForm(request.POST)
                    f = form.save(commit=False)
                    f.employee_employee_id_id = employee_total_data.employee_employee_id
                    f.bank_name = request.POST['bank_name']
                    f.account_no = request.POST['account_number']
                    f.ifsc_code = request.POST['ifsc_code']
                    f.pan = request.POST['pan_number']
                    f.save()
                    return render(request, "dashboard/update-added-employee.html",
                                  {'employee_total_data': employee_total_data, 'bank_details_emp': bank_details_emp})
                if 'school_details' in request.POST:
                    try:
                        master_college_name = request.POST['master_college_name']
                        master_course_name = request.POST['master_course_name']
                        master_college_details = request.POST['master_college_details']
                        master_start_year = request.POST['master_start_year']
                        master_end_year = request.POST['master_end_year']

                        graduation_college_name = request.POST['graduation_collaege_name']
                        graduation_course_name = request.POST['graduation_course_name']
                        graduation_college_details = request.POST['graduation_college_details']
                        graduation_start_year = request.POST['graduation_start_year']
                        graduation_end_year = request.POST['graduation_end_year']

                        senior_school_name = request.POST['senior_school_name']
                        senior_school_board = request.POST['senior_school_board']
                        senior_school_details = request.POST['senior_school_details']
                        senior_school_end_year = request.POST['senior_school_end_year']

                        matric_school_name = request.POST['matric_school_name']
                        matric_school_board = request.POST['matric_school_board']
                        matric_school_details = request.POST['matric_school_details']
                        matric_school_end_year = request.POST['matric_school_end_year']

                        update_school_info = employee_profile(employee_employee_id=employee_total_data.employee_employee_id,
                                                              masters_college_name=master_college_name,
                                                              masters_college_course_name=master_course_name,
                                                              masters_college_details=master_college_details,
                                                              masters_start_year=master_start_year,
                                                              masters_complete_year=master_end_year,
                                                              graduation_college_name=graduation_college_name,
                                                              graduation_college_course_name=graduation_course_name,
                                                              graduation_college_details=graduation_college_details,
                                                              graduation_start_year=graduation_start_year,
                                                              graduation_complete_year=graduation_end_year,
                                                              sec_schl_name=senior_school_name,
                                                              sec_schl_board=senior_school_board,
                                                              sec_schl_details=senior_school_details,
                                                              sec_schl_complete_year=senior_school_end_year,
                                                              matric_schl_name=matric_school_name,
                                                              matric_schl_board=matric_school_board,
                                                              matric_schl_details=matric_school_details,
                                                              matric_schl_complete_year=matric_school_end_year)
                        update_school_info.save(update_fields=['masters_college_name', 'masters_college_course_name', 'masters_college_details',
                                                               'masters_start_year', 'masters_complete_year', 'graduation_college_name',
                                                               'graduation_college_course_name', 'graduation_college_details', 'graduation_start_year',
                                                               'graduation_complete_year', 'sec_schl_name', 'sec_schl_board', 'sec_schl_details',
                                                               'sec_schl_complete_year', 'matric_schl_name', 'matric_schl_board', 'matric_schl_details',
                                                               'matric_schl_complete_year'])

                        return render(request, "dashboard/update-added-employee.html",
                                      {'employee_total_data': employee_total_data,
                                       'bank_details_emp': bank_details_emp})
                    except:
                        return render(request, "dashboard/update-added-employee.html",
                                      {'employee_total_data': employee_total_data, 'bank_details_emp': bank_details_emp})
                return render(request, "dashboard/update-added-employee.html",
                              {'employee_total_data': employee_total_data, 'permission_not_to_edit': False, 'bank_details_emp': bank_details_emp})

        # log in as Employee
        elif request.session['user_role_id'] == 3:
            return redirect("/home")
    elif not permission:
        return redirect("/")


# if port in use already
# sudo kill $(lsof -t -i:8000)
