#
# #from datetime import datetime
# '''
# import random
#
# a = "demoemployee"  # type: str
# a = a.upper()
#
# e = a[:3]+str(random.randint(0, 99999))
# print(e)
# '''
#
# """
# date_str = '03/09/2019' # The date - 29 Dec 2017
# format_str = '%d/%m/%Y' # The format
# datetime_obj = datetime.datetime.strptime(date_str, format_str).weekday()
# if datetime_obj==0:
#     print("MONDAY")
# if datetime_obj==1:
#     print("TuesDAY")
# if datetime_obj==2:
#     print("Wednesday")
#
# if datetime_obj==3:
#     print("Thursday")
#
#
# if datetime_obj==4:
#     print("friday")
#
# if datetime_obj==5:
#     print("satrday")
#
#
# if datetime_obj==6:
#     print("sunday")
# print(datetime_obj)
# #weekday Monday is 0 and Sunday is 6
#
# import timestring
#
#
# datea='09/01/2019'
# date_is=datetime.date(datea)
#
# dayofweek = datetime.date(date_is).strftime("%A")
# print(dayofweek)
#
#
# timestring.Date('monday, aug 15th 2015 at 8:40 pm')
# # weekday Monday is 0 and Sunday is 6
# print("weekday():", datetime.date(date_is).weekday())
#
# # isoweekday() Monday is 1 and Sunday is 7
# print("isoweekday()", datetime.date(date_is).isoweekday())
#
# dayofweek = datetime.datetime.today().strftime("%A")
# print(dayofweek)
# print("weekday():", datetime.datetime.today().weekday())
# print("isoweekday()", datetime.datetime.today().isoweekday())
#
# date_str = "termination_date"
# format_str = '%m/%d/%Y'
# datetime_obj = datetime.strftime(date_str, format_str).date()
#
# datetime_obj2 = datetime_obj.strftime("%d, %m, %Y")"""
# """
# today = "date.today()"
#
# today_date = today.strftime("%d, %m, %Y")
# if datetime_obj2 == today_date:
#     print("mattched")
# elif datetime_obj2 != today_date:
#     print("Not today")
#
# now = datetime.datetime.now()
#
# print("now =", now)
# # dd/mm/YY H:M:S
# dt_string = now.strftime("%I:%M:%S %p")
# print("time =", dt_string)
#
#
# class first:
#     def tower(self):
#         a = [1, 2, 3, 4, 5]
#         print(a)
#
#
# class second(first):
#     pass
#
#
# class third(second):
#     def tower2(self):
#         first.tower(self)
#         print("third")
#
#
# d = third()
# third.tower2()
#
# # Create datetime objects for each time (a and b)
# dateTimeA = datetime.datetime.combine(datetime.date.today(), a)
# dateTimeB = datetime.datetime.combine(datetime.date.today(), b)
# # Get the difference between datetimes (as timedelta)
# dateTimeDifference = dateTimeA - dateTimeB
# # Divide difference in seconds by number of seconds in hour (3600)
# dateTimeDifferenceInHours = dateTimeDifference.total_seconds() / 3600
#
# timestr = '02:26:46 PM' #
# format_str = '%I:%M:%S %p' # The format
# datetime_obj = dt.datetime.strptime(timestr, '%I:%M:%S %p')
# dt_ob=datetime_obj.time()
# print(type(dt_ob))
# now = dt.datetime.now().time()
# print(now)
# punchout_time = now.strftime("%H:%M:%S")
# newobj=dt.datetime.strptime(punchout_time,"%H:%M:%S")
# #newobj=punchout_time.time()
# print(type(newobj),newobj)
# dt_ob2=punchout_time.time()#print(type(dt_ob2))
# diff = punchout_time-datetime_obj.time()
# print("differnce",diff)
# db_string="02:26:46 PM"
#
# #datetime_obj = datetime.strptime(db_string,"%I:%M:%S %p")
#
# #time_is=datetime_obj.time()
# #print(time_is,type(time_is))
# #now = dt.datetime.now().time()
# #print(now,type(now))
# now=datetime.now().strftime('%I:%M %p')
#
# #now_time= datetime.strptime(now,"%H:%M:%S")
# #print(now,type(now))
# #now_time_is=now_time.time()
# #print(now_time_is,type(now_time_is))
# #diff = now_time_is - time_is
# #print(diff.total_seconds()/3600)
# #print(datetime.now().strftime('%H:%M:%S'),type(datetime.now().strftime('%H:%M:%S')))
#
# import datetime
# from datetime import timedelta
#
# datetimeFormat = '%I:%M %p'
# date1 = now
# date2 = '04:37 PM'
# diff = datetime.datetime.strptime(date1, datetimeFormat)\
#     - datetime.datetime.strptime(date2, datetimeFormat)
#
#
#
# print("Difference :", diff)
# print("Days:", diff.days)
# print("Microseconds:", diff.microseconds)
# print("Seconds:", diff.seconds)"""
# # new code
# """
# import datetime
#
# import pytz
#
# db_punch_in_time = "10:16 AM"
# db_punch_out_time = datetime.datetime.now().strftime('%I:%M %p')
#
# print("Punch in :", db_punch_in_time, "\nPunch out:", db_punch_out_time)
# timeFormat = '%I:%M %p'
# difference = datetime.datetime.strptime(db_punch_out_time, timeFormat)\
#     - datetime.datetime.strptime(db_punch_in_time, timeFormat)
# print("Differnce :", difference)
#
#
#
# $ pip install pytz
# You can use the pytz library as follows:
#
# from datetime import datetime
# from pytz import timezone
# format = "%Y-%m-%d %H:%M:%S %Z%z"
# # Current time in UTC
# now_utc = datetime.now(timezone('UTC'))
# print(now_utc.strftime(format))
# # Convert to Asia/Kolkata time zone
# now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
# print(now_asia.strftime(format))
# This will give the output:
#
# 2018-01-03 07:05:50 UTC+0000
# 2018-01-03 12:35:50 IST+0530
#
# """
# """
# format = "%Y-%m-%d %H:%M:%S %Z%z"
# # Current time in UTC
# now_utc = datetime.datetime.now(timezone('UTC'))
# print(now_utc.strftime(format))
# # Convert to Asia/Kolkata time zone
# now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
# print(now_asia.strftime(format))
#
# #now_asia = now_utc.astimezone(timezone(''))
# # print(now_asia.strftime(format))
# s = "india"
# country_selected = "jnjnjn"
# for tz in pytz.all_timezones:
#     if tz.find(country_selected) == -1:
#         print("tz", tz)
#
# """
# from datetime import date,datetime
# """eg='09,10,2019'
# #print(eg,type(eg))
# f_date = date(2019,9,10)
# #print(type(f_date))
# l_date = date(2019,9,21)
# delta = l_date - f_date
# #print(delta.days)   """
#
# #converted=datetime.strptime(eg,'%m,%d,%y').date()
# #print(converted,type(converted),converted)
# #datetime.date(2012, 1, 30)
# #ab=datetime.strptime('09,10,2019', '%m,%d,%Y').date()
# #
# #cb=ab.strftime("%Y,%m,%d")
# #new=datetime.strptime(cb, "%Y-%m-%d").date()
# #print(new,type(new))
# #print(cb,type(cb))
# #print(ab,type(ab))
# """
# date_str = '09/10/2019'
# print(date_str)
# new_str=date_str.replace("/",",")
# print("new",new_str)
# formatter_string = "%m,%d,%Y"
# datetime_object = datetime.strptime(new_str,'%m,%d,%Y')
# print(datetime_object,type(datetime_object))
# date_object = datetime_object.date()
# print(date_object,type(date_object))
#
# year= 2019
# month=9
# day=23
# ab= date(year, month, day).__format__("%Y,%m,%d")
# print(ab,type(ab))
#
# """
# # d1 = date(2019, 9, 11)
# #
# #
# # date_from="09/11/2019"
# # new_lis=date_from.split("/")
# # month,day,year=new_lis
# #
# # month=int(month)
# # day=int(day)
# # year=int(year)
# #
# #
# # date_new_from = d1.replace(year, month, day)
# # print('date from:', date_new_from )
# #
# # date_to = "09/15/2019"
# # new_lis2 = date_to.split("/")
# # month, day, year = new_lis2
# #
# # month = int(month)
# # day = int(day)
# # year = int(year)
# #
# # date_to = d1.replace(year,month,day)
# # print('date to:', date_to)
# #
# #
# # td=date_to-date_new_from
# #
# # print("difference:",td.days,'days')
# #
# # #print ('Difference:'+str(td)  )
# #
# #
# #
# # #calculated time difference
# # import datetime
# #
# # import pytz
# #
# # db_punch_in_time = "10:16 AM"
# # db_punch_out_time = "10:20 AM"
# #
# #
# # timeFormat = '%I:%M %p'
# # difference = datetime.datetime.strptime(db_punch_out_time, timeFormat)\
# #     - datetime.datetime.strptime(db_punch_in_time, timeFormat)
# # print("Differnce :", difference)
# from  datetime import  datetime,date
# date_is=date.today()
# date_today=date.strftime(date_is,"%d")
# month_today=date.strftime(date_is,"%m")
# print(type(date_today),type(month_today))
# if date_today=='01':
#     print("p")
# if date_today=='02':
#     print("p")
# if date_today=='03':
#     print("p")
# if date_today=='01':
#     print("p")
# if date_today=='04':
#     print("p")
# if date_today=='05':
#     print("p")
# if date_today=='06':
#     print("p")
# if date_today=='07':
#     print("p")
# if date_today=='08':
#     print("p")
# if date_today=='09':
#     print("p")
# if date_today=='10':
#     print("p")
# if date_today=='11':
#     print("p")
# if date_today=='12':
#     print("p")
# if date_today=='13':
#     print("p")
# if date_today=='14':
#     print("p")
# if date_today=='15':
#     print("p")
# if date_today=='16':
#     print("16")
# if date_today=='17':
#     print(17)
# if date_today=='18':
#     print("18")
# if date_today=='19':
#     print("19")
# if date_today=='20':
#     print("20")
# if date_today=='21':
#     print("21")
# if date_today=='22':
#     print("22")
# if date_today=='23':
#     print("23")
# if date_today=='24':
#     print("24")
# if date_today=='25':
#     print("25")
# if date_today=='26':
#     print("26")
# if date_today=='27':
#     print("27")
# if date_today=='28':
#     print("28")
# if date_today=='29':
#     print("29")
# if date_today=='30':
#     print("30")
# if date_today=='31':
#     print("31")
#
#
#

import calendar
from datetime import datetime


def second_fourth_saturday(year, month):
    cal = calendar.monthcalendar(year, month)


    if cal[0][calendar.SATURDAY]:
        holidays[month] = (
            cal[1][calendar.SATURDAY],
            cal[3][calendar.SATURDAY]
        )
    else:
        holidays[month] = (
            cal[2][calendar.SATURDAY],
            cal[4][calendar.SATURDAY]
        )

# print(second_fourth_saturday(2019,9))

import calendar

# Show every monthimport calendar
# # Show every month
# for month in range(1, 13):
#     cal = calendar.monthcalendar(2020, month)
#     first_week  = cal[0]
#     second_week = cal[1]
#     third_week  = cal[2]
#
#     # If a Saturday presents in the first week, the second Saturday
#     # is in the second week.  Otherwise, the second Saturday must
#     # be in the third week.
#
#     if first_week[calendar.SATURDAY]:
#         holi_day = second_week[calendar.SATURDAY]
#     else:
#         holi_day = third_week[calendar.SATURDAY]
#
#     print('%3s: %2s' % (calendar.month_abbr[month], holi_day))
# for month in range(1, 13):
#     cal = calendar.monthcalendar(2019, month)
#     first_week = cal[0]
#     second_week = cal[1]
#     third_week = cal[2]
#     # If a Saturday presents in the first week, the second Saturday
#     # is in the second week.  Otherwise, the second Saturday must
#     # be in the third week.
#
#     if first_week[calendar.SATURDAY]:
#         holi_day = second_week[calendar.SATURDAY]
#     else:
#         holi_day = third_week[calendar.SATURDAY]
#
#     print('%3s: %2s' % (calendar.month_abbr[month], holi_day))
#
from  datetime import date
print(date.today())


from calendar import monthcalendar, SATURDAY
from datetime import datetime
#
# def second_fourth_saturday(date):
#     month_calender = monthcalendar(date.year, date.month)
#     second_fourth_saturday = (1, 3) if month_calender[0][SATURDAY] else (2, 4)
#     return any(date.day == month_calender[i][SATURDAY] for i in second_fourth_saturday)
#
# is_second_fourth_saturday = second_fourth_saturday(datetime.today())
# print("Enjoy" if is_second_fourth_saturday else "Start working")

import calendar

# Show every month
# for month in range(1, 13):
#     cal = calendar.monthcalendar(2019, month)
#     first_week = cal[0]
#     second_week = cal[1]
#     third_week = cal[2]
#     fourth_week=cal[3]
#     fifth_week = cal[4]
#
#     # If a Saturday presents in the first week, the second Saturday
#     # is in the second week.  Otherwise, the second Saturday must
#     # be in the third week.
#
#     if first_week[calendar.SATURDAY] and fourth_week[calendar.SATURDAY]:
#         holi_day_1 = second_week[calendar.SATURDAY]
#         holi_day_2 = fourth_week[calendar.SATURDAY]
#     else:
#         holi_day_1 = third_week[calendar.SATURDAY]
#         holi_day_2 = fifth_week[calendar.SATURDAY]
#
#
#     print('%3s: %2s %1s' % (calendar.month_abbr[month], holi_day_1,holi_day_2))
# print("%n")
# for month in range(1, 13):
#     cal = calendar.monthcalendar(2019, month)
#     first_week = cal[0]
#     second_week = cal[1]
#     third_week = cal[2]
#     fourth_week=cal[3]
#     fifth_week = cal[4]
#
#     # If a Saturday presents in the first week, the second Saturday
#     # is in the second week.  Otherwise, the second Saturday must
#     # be in the third week.
#     first_sunday=first_week[calendar.SUNDAY]
#     second_sunday=second_week[calendar.SUNDAY]
#     third_sunday=third_week[calendar.SUNDAY]
#     third_sunday=fourth_week[calendar.SUNDAY]
#     fifth_sunday=fifth_week[calendar.SUNDAY]
#     # if first_week[calendar.SUNDAY] and fourth_week[calendar.SUNDAY]:
#     #     holi_day_1 = second_week[calendar.SUNDAY]
#     #     holi_day_2 = fourth_week[calendar.SUNDAY]
#     # else:
#     #     holi_day_1 = third_week[calendar.SUNDAY]
#     #     holi_day_2 = fifth_week[calendar.SUNDAY]
#
#     print((calendar.month_abbr[month], first_sunday,second_sunday,third_sunday,third_sunday,fifth_sunday))
#


cal = calendar.monthcalendar(2019, 9)
first_week = cal[0]
second_week = cal[1]
third_week = cal[2]
fourth_week=cal[3]
fifth_week = cal[4]

# If a Saturday presents in the first week, the second Saturday
# is in the second week.  Otherwise, the second Saturday must
# be in the third week.

if first_week[calendar.SATURDAY] and fourth_week[calendar.SATURDAY]:
    holi_day_1 = second_week[calendar.SATURDAY]
    holi_day_2 = fourth_week[calendar.SATURDAY]
else:
    holi_day_1 = third_week[calendar.SATURDAY]
    holi_day_2 = fifth_week[calendar.SATURDAY]

print(holi_day_1,holi_day_2)