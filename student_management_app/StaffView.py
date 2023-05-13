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
    session_model=SessionYearModel.object.get(id=session_year)
    students=Students.objects.filter(course_id=subject.course_id,session_id=session_model)
    list_data=[]

    for student in students:
        data_small={"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)


# @csrf_exempt
# def get_students(request):
#     subject_id = request.POST.get('subject')
#     session_year = request.POST.get('session_year')

#     subject = Subject.objects.get(id=subject_id)
#     session_model = SessionYearModel.objects.get(subject=session_year)
#     students = Students.objects.filter(course_id=subject.course_id, session_id=session_model)

#     list_student = []
#     for student in students:
#         data_small = {"id": student.admin_id.id, "name": student.admin_id.first_name + " " + student.admin_id.last_name}
#         list_student.append(data_small)
#     return JsonResponse(list_student, safe=False)

# @csrf_exempt
# def save_attendance_data(request):
#     student_ids = request.POST.getlist('student_ids[]')
#     attendance_date = request.POST.get("attendance_date")
#     subject_id = request.POST.get("subject_id")
#     session_year = request.POST.get("session_year")
    
#     subject_model = Subject.objects.get(id=subject_id)
#     session_model = SessionYearModel.objects.get(id=session_year)
#     json_student = json.loads(student_ids)
#     # dict_student[0]['id']
#     attendance = Attendance(subject_id=subject_model,attendance_date=attendance_date,session_id=session_model)
#     attendance.save()
    
    
#     for stud in json_student:
#         student = Students.objects.get(admin_id=stud['id'])
#         attendance_report = AttendanceReport(student_id=student,attendance_id=attendance.id,status=stud['status'])
#         attendance_report.save()
#     return HttpResponse("Ok")

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
        attendance=Attendance(subject_id=subject_model,attendance_date=attendance_date,session_year_id=session_model)
        attendance.save()

        for stud in json_sstudent:
             student=Students.objects.get(admin=stud['id'])
             attendance_report=AttendanceReport(student_id=student,attendance_id=attendance,status=stud['status'])
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")
