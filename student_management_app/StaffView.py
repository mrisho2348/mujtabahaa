import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers


from student_management_app.models import Attendance, AttendanceReport, Courses, SessionYearModel, Students, Subject


def staff_home(request):
    return render(request,"staff_template/staff_home.html")

def staff_take_attendance(request):
    subjects = Subject.objects.filter(staff_id=request.user.id)    
    session_years = SessionYearModel.objects.all()
    return render(request,"staff_template/staff_take_attendance.html",{"subjects":subjects,"session_years":session_years})



@csrf_exempt
def get_students(request):
    subject_id=request.POST.get("subject")
    session_year=request.POST.get("session_year")

    subject=Subject.objects.get(id=subject_id)
    session_model=SessionYearModel.objects.get(id=session_year)
    students=Students.objects.filter(course_id=subject.course_id,session_id=session_model)
    list_data=[]

    for student in students:
        data_small={"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)




@csrf_exempt
def save_attendance_data(request):
    student_ids=request.POST.get("student_ids")
    subject_id=request.POST.get("subject_id")
    attendance_date=request.POST.get("attendance_date")
    session_year_id=request.POST.get("session_year_id")

    subject_model=Subject.objects.get(id=subject_id)
    session_model=SessionYearModel.objects.get(id=session_year_id)
    json_sstudent=json.loads(student_ids)
    #print(data[0]['id'])


    try:
        attendance=Attendance(subject_id=subject_model,attendance_date=attendance_date,session_id=session_model)
        attendance.save()

        for stud in json_sstudent:
             student=Students.objects.get(admin_id=stud['id'])
             attendance_report=AttendanceReport(student_id=student,attendance_id=attendance,status=stud['status'])
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")
    
    
def staff_update_attendance(request):
    subjects = Subject.objects.filter(staff_id=request.user.id) 
    session_year_id = SessionYearModel.objects.all()
    return render(request,"staff_template/staff_update_attendance.html",{"subjects":subjects,"session_years":session_year_id})  

@csrf_exempt
def get_attendance_date(request):
     subject = request.POST.get("subject_id")
     session_year_id = request.POST.get("session_year_id")
     print(subject)
     print(session_year_id)
     subject_obj = Subject.objects.get(id=subject)
     session_year_obj = SessionYearModel.objects.get(id=session_year_id)
     attendance = Attendance.objects.filter(subject_id=subject_obj,session_id=session_year_obj)
     attendance_obj = []
     
     for attendance_single in attendance:
         data = {
             "id":attendance_single.id,
             "attendance_date":str(attendance_single.attendance_date),
             "session_year_id":attendance_single.session_id.id
             }
         attendance_obj.append(data)
         
     return JsonResponse(json.dumps(attendance_obj),content_type="application/json",safe=False)  
 
@csrf_exempt
def get_student_attendance(request):  
    attendance_date=request.POST.get("attendance_date_id")     
    attendance_date_id=Attendance.objects.get(id=attendance_date)
    attendance_data =AttendanceReport.objects.filter(attendance_id=attendance_date_id)   
    
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)



@csrf_exempt
def save_updateattendance(request):
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get("attendance_date")     
    attendance=Attendance.objects.get(id=attendance_date)     
    json_sstudent=json.loads(student_ids)
    #print(data[0]['id'])


    try:
        for stud in json_sstudent:
             student=Students.objects.get(admin_id=stud['id'])
             attendance_report=AttendanceReport.objects.get(student_id=student,attendance_id=attendance)
             attendance_report.status =stud["status"]
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")
    
