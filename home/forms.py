from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from home.models import *

# from django.forms import ModelForm

# from home.models import user_profile, company_profile


class empBankDetailsForm(forms.ModelForm):
    class Meta:
        model = employee_bank_details
        exclude = ('id', 'employee_employee_id', 'bank_name',
                   'account_no', 'ifsc_code', 'pan', )


class leaves_form(forms.ModelForm):

    class Meta:
        model = tb_employee_leaves
        exclude = ('id', 'leave_type', 'leave_from', 'leave_to', 'one_day_leave', 'one_day_leave_date', 'half_day_leave', 'half_day_leave_date', 'short_leave', 'short_leave_date',
                   'employee_employee_id', 'emp_cmpy_email', 'emp_hr_email', 'leave_status', 'leaves_left_monthly', 'above_limit_leaves', 'reason', 'leave_policy_type', )


class updateEmployeeForm(forms.ModelForm):
    class Meta:
        model = employee_profile
        exclude = ('role_id',
                   'department_id',
                   'designation_id',
                   'employee_firstname',
                   'employee_lastname',
                   'employee_username',
                   'employee_official_email',
                   'employee_personal_email',
                   'employee_password',
                   'employee_company',
                   'employee_hr_name',
                   'employee_company_email',
                   'employee_hr_email',
                   'employee_phone',
                   'employee_employee_id',
                   'profile_edit',
                   'added_by',
                   'edited_by',
                   'deleted_by',
                   'is_active',
                   'is_terminated',
                   'terminated_by',
                   'promoted_by',
                   'created_date',
                   'terminated_date',
                   'gender',
                   'birthday',
                   'address',
                   'martial_status',
                   'masters_college_name',
                   'masters_college_course_name',
                   'masters_college_details',
                   'masters_start_year',
                   'masters_complete_year',
                   'graduation_college_name',
                   'graduation_college_course_name',
                   'graduation_college_details',
                   'graduation_start_year',
                   'graduation_complete_year',
                   'sec_schl_name',
                   'sec_schl_board',
                   'sec_schl_details',
                   'sec_schl_complete_year',
                   'matric_schl_name',
                   'matric_schl_board',
                   'matric_schl_details',
                   'matric_schl_complete_year',
                   'permission_to_edit',
                   'updated_once',
                   'request_status',
                   'edit_request_hr_email'
                   'edit_request_emp_email',
                   'edit_request_by_emp',
                   'edit_request_by_hr')


class attendanceForm(forms.ModelForm):
    class Meta:
        model = tb_timesheet
        exclude = ('id',
                   'db_date',
                   'employee_employee_id',
                   'punch_in',
                   'punch_out',
                   'total_hours')


class attendancForm(forms.ModelForm):
    class Meta:
        model = daily_attendance_employee
        exclude = ('id', 'db_date', 'db_month', 'db_year', 'employee_employee_id',
                   'present', 'on_leave', 'company_mail', 'hr_mail', )


class terminationForm(forms.ModelForm):
    class Meta:
        model = terminations
        exclude = ('id',
                   'employee_employee_id',
                   'reason',
                   'termination_type',
                   'termination_date',
                   'request_status',
                   'terminate_request_by',
                   'termination_notice_date',
                   'company_email',
                   'hr_email')


class holidaysForm(forms.ModelForm):
    class Meta:
        model = holidays
        exclude = ('holiday_id',
                   'holiday_name',
                   'holiday_date',
                   'day',
                   'added_by',
                   'edited_by',
                   'deleted_by')


class updatedCompanyProfileForm(forms.ModelForm):
    class Meta:
        model = company_profile
        exclude = ('company_name', 'contact_person', 'address', 'country', 'city', 'postal_code', 'state_province',
                   'phone_number', 'mobile_number', 'fax', 'website_url')


class employeeForm(forms.ModelForm):
    employee_firstname = forms.CharField(required=True, max_length=100,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       }))
    employee_lastname = forms.CharField(required=True, max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', }))
    employee_username = forms.CharField(required=True, max_length=100,
                                        widget=forms.TextInput(attrs={'class': 'form-control',

                                                                      }))

    employee_official_email = forms.EmailField(required=True, max_length=100,
                                               widget=forms.EmailInput(attrs={'class': 'form-control',

                                                                              }))
    employee_password = forms.CharField(required=True, max_length=255,
                                        widget=forms.PasswordInput(attrs={'class': 'form-control',

                                                                          }))
    employee_phone = forms.CharField(required=True, max_length=15,
                                     widget=forms.TextInput(attrs={'class': 'form-control', }))

    class Meta:
        model = employee_profile
        exclude = ('role_id',
                   'department_id',
                   'designation_id',
                   'employee_firstname',
                   'employee_lastname',
                   'employee_username',
                   'employee_official_email',
                   'employee_personal_email',
                   'employee_password',
                   'employee_company',
                   'employee_hr_name',
                   'employee_company_email',
                   'employee_hr_email',
                   'employee_phone',
                   'employee_employee_id',
                   'profile_edit',
                   'added_by',
                   'edited_by',
                   'deleted_by',
                   'is_active',
                   'is_terminated',
                   'terminated_by',
                   'promoted_by',
                   'created_date',
                   'terminated_date',
                   'gender',
                   'birthday',
                   'address',
                   'martial_status',
                   'masters_college_name',
                   'masters_college_course_name',
                   'masters_college_details',
                   'masters_start_year',
                   'masters_complete_year',
                   'graduation_college_name',
                   'graduation_college_course_name',
                   'graduation_college_details',
                   'graduation_start_year',
                   'graduation_complete_year',
                   'sec_schl_name',
                   'sec_schl_board',
                   'sec_schl_details',
                   'sec_schl_complete_year',
                   'matric_schl_name',
                   'matric_schl_board',
                   'matric_schl_details',
                   'matric_schl_complete_year',
                   'permission_to_edit',
                   'updated_once',
                   'request_status',
                   'edit_request_hr_email',
                   'edit_request_emp_email',
                   'edit_request_by_emp',
                   'edit_request_by_hr')


class departmentForm(forms.ModelForm):
    department_name = forms.CharField(required=True, max_length=100,
                                      widget=forms.TextInput(attrs={'class': 'form-control text-dark', 'placeholder': 'Enter Department Name',
                                                                    }))

    class Meta:
        model = department
        exclude = ('department_id', 'department_name',
                   'added_by', 'edited_by', 'deleted_by')


class designationForm(forms.ModelForm):
    designation_name = forms.CharField(required=True, max_length=100,
                                       widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = designation
        exclude = ('designation_id', 'department_id',
                   'designation_name', 'added_by', 'edited_by', 'deleted_by')


class user_profileForm(forms.ModelForm):
    user_firstname = forms.CharField(
        required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    user_lastname = forms.CharField(
        required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(required=True, max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    user_email = forms.EmailField(required=True, max_length=100,
                                  widget=forms.EmailInput(attrs={'class': 'form-control'}))
    user_password = forms.CharField(required=True, max_length=255,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    user_phone = forms.CharField(required=True, max_length=15,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = user_profile
        exclude = ('role_id',
                   'user_firstname',
                   'user_lastname',
                   'user_email',
                   'user_password',
                   'user_company_email',
                   'user_company',
                   'user_phone',
                   'user_employee_id',
                   'employee_read',
                   'employee_create',
                   'employee_edit',
                   'employee_delete',
                   'leaves_read',
                   'leaves_create',
                   'leaves_edit',
                   'leaves_delete',
                   'holidays_read',
                   'holidays_create',
                   'holidays_edit',
                   'holidays_delete',
                   'event_read',
                   'event_create',
                   'event_edit',
                   'event_delete',
                   'is_active',
                   'created_date')


class companyForm(forms.ModelForm):

    company_name = forms.CharField(
        required=True, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact_person = forms.CharField(required=True, max_length=255,
                                     widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(required=True, max_length=255,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(required=True, max_length=255,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(required=True, max_length=255,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    postal_code = forms.IntegerField(
        required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state_province = forms.CharField(required=True, max_length=255,
                                     widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(required=True, max_length=15,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile_number = forms.CharField(required=True, max_length=15,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    fax = forms.CharField(required=False, max_length=50,
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    website_url = forms.CharField(required=True, max_length=255,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = company_profile
        fields = ('company_name',
                  'contact_person',
                  'address',
                  'country',
                  'city',
                  'postal_code',
                  'state_province',
                  'phone_number',
                  'mobile_number',
                  'fax',
                  'website_url')


class updatePasswordForm(forms.Form):
    company_user_password = forms.CharField(required=True, max_length=1000,
                                            widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = company_profile
        fields = ('company_user_password',)


class EmailValidationOnForgotPassword(PasswordResetForm):
    email = forms.EmailField(max_length=254, label='',
                             widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Email'}
                                                    ))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError(
                "There is no user registered with the specified email address!")
            # messeage =("There is no user registered with the specified email address!")
            # return redirect('../password_reset',locals())

            # return 'no'
        return email


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'New password',
            }
        ),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'New password confirmation',
            }
        ),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class SignUpForm(UserCreationForm):

    username = forms.CharField(label='Username', max_length=254, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username',
        }
    ))
    email = forms.EmailField(label='Email', max_length=254, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        }
    ))
    password1 = forms.CharField(label='Password', max_length=254, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))
    password2 = forms.CharField(label='Confirm Password', max_length=254, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email already exists.')
        return email


class UserLoginForm(forms.Form):
    email = forms.CharField(required=True, label='Email', max_length=254, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        }
    ))
    password = forms.CharField(label='Password', max_length=254, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    })
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True,
                                          'class': 'form-control',
                                          'placeholder': 'Old Password',

                                          }),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password
