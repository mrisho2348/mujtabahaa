
from datetime import datetime
from time import strptime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from student_management_app.models import Attendance, AttendanceReport,  CustomUser, FeedBackStudent, LeaveReportStudent, Students, Subject
from student_management_app.templatetags.custom_filters import strftime


def student_home(request):
    student_object = Students.objects.get(admin=request.user.id)
    attendance_present = AttendanceReport.objects.filter(student_id=student_object,status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=student_object,status=False).count()
    attendance_total = AttendanceReport.objects.filter(student_id=student_object).count()
    # course = Courses.objects.get(id=student_object.course_id.id)
    subject_total = Subject.objects.filter(course_id=course).count()
    subject_data = Subject.objects.filter(course_id=student_object.course_id)
    subject_name = []
    data_present = []
    data_absent = []
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance,status=True,student_id=student_object.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance,status=False,student_id=student_object.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)
    return render(request,"student_template/student_home.html",{"attendance_total":attendance_total,"attendance_present":attendance_present,"attendance_absent":attendance_absent,"subject_total":subject_total,"subject_name":subject_name,"data_present":data_present,"data_absent":data_absent})



def student_view_attendance(request):
    students = Students.objects.get(admin_id=request.user.id)
    print(students)
    courses =students.course_id
    print(courses)
    subjects = Subject.objects.filter(course_id=courses)
    return render(request,"student_template/student_view_attendance.html",{"subjects":subjects})


def student_view_attendance_post(request):
    subject_id = request.POST.get("subject")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    
    start_date_parse = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date_parse = datetime.strptime(end_date, "%Y-%m-%d").date()
    subject_obj = Subject.objects.get(id=subject_id)
    user_obj = CustomUser.objects.get(id = request.user.id)
    student_obj = Students.objects.get(admin=user_obj)
    attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse,end_date_parse),subject_id=subject_obj)
    attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance,student_id = student_obj)
    
    for attendance_report in attendance_reports:
        print("Date: "+str(attendance_report.attendance_id.attendance_date), "status: " + str(attendance_report.status))
        
    return render(request,"student_template/student_attendance_data.html",{"attendance_reports":attendance_reports}) 




def student_sendfeedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    return render(request,"student_template/student_feedback.html",{"feedback_data":feedback_data})

def student_sendfeedback_save(request):
    if request.method!= "POST":
        return HttpResponseRedirect(reverse("student_sendfeedback"))
    
    else:
       feedback_msg = request.POST.get("feedback_msg") 
       student_obj = Students.objects.get(admin=request.user.id)
       try:           
          feedback_report = FeedBackStudent(student_id=student_obj,feedback=feedback_msg,feedback_reply="")
          feedback_report.save()
          messages.success(request,"feedback Successfully  sent")
          return HttpResponseRedirect(reverse("student_sendfeedback"))  
             
       except:
            messages.error(request,"feedback failed to be sent")
            return HttpResponseRedirect(reverse("student_sendfeedback"))

def   student_apply_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    student_leave_report =LeaveReportStudent.objects.filter(student_id=student_obj)
    return render(request,"student_template/student_leave_template.html",{"student_leave_report":student_leave_report})



def student_apply_leave_save(request):
    if request.method!= "POST":
        return HttpResponseRedirect(reverse("student_apply_leave"))
    
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")     
        staff_obj = Students.objects.get(admin=request.user.id)
       
        try:            
          leave_report =LeaveReportStudent(student_id=staff_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
          leave_report.save()
          messages.success(request,"Successfully  staff apply leave ")
          return HttpResponseRedirect(reverse("student_apply_leave"))  
             
        except:
            messages.error(request,"failed for staff to apply for leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))
        
        


def  student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    students = Students.objects.get(admin=user)
    return render(request,"student_template/student_profile.html",{"user":user,"students":students})  

def student_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_profile"))
    
    else:
       first_name = request.POST.get("first_name")
       last_name = request.POST.get("last_name")
       password = request.POST.get("password")
       address = request.POST.get("address")
       try:           
          customuser = CustomUser.objects.get(id=request.user.id)
          customuser.first_name = first_name
          customuser.last_name = last_name
          if password!= "" and password!=None:
              customuser.set_password(password)     
                         
          customuser.save()
          students = Students.objects.get(admin=customuser.id)
          students.address = address
          messages.success(request,"profile is successfully edited")
          return HttpResponseRedirect(reverse("student_profile"))
      
       except:
            messages.error(request,"editing  of profile  failed")
            return HttpResponseRedirect(reverse("student_profile"))
        

    