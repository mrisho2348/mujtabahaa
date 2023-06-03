import json
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from student_management_app.forms import  AddSessionYearForm, AddStaffForm, AddStudentForm, AddSubjectForm, EditStaffForm, EditStudentForm
from student_management_app.models import Attendance, AttendanceReport, CustomUser, FeedBackStaff, FeedBackStudent, LeaveReportStaffs, LeaveReportStudent, SessionYearModel, Staffs, Students, Subject
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect


def admin_home(request):
  
    staff_count = Staffs.objects.all().count()
    subject_count = Subject.objects.all().count()
   
    subject_count_list = []

        
    subject_all = Subject.objects.all()
    subject_list = []
    student_count_in_subject_list = []
    for subject in subject_all:
     
          subject_list.append(subject.subject_name)
      
          
    staff_all = Staffs.objects.all()
    attendance_present_staff_list = []
    attendance_absent_staff_list = []
    staff_name_list = []
    for staff in staff_all:
        couse_id = Subject.objects.filter(staff_id=staff.admin.id) 
        attendance = Attendance.objects.filter(subject_id__in=couse_id ).count()
        leaves = LeaveReportStaffs.objects.filter(staff_id=staff.id,leave_status=1).count()
        attendance_present_staff_list.append(attendance) 
        attendance_absent_staff_list.append(leaves) 
        staff_name_list.append(staff.admin.username)  
        
        
    student_all = Students.objects.all()
    attendance_absent_student_list = []
    attendance_present_student_list = []
    student_name_list = []
    for student in student_all:        
        attendance = AttendanceReport.objects.filter(student_id=student.id,status=True).count()
        absent = AttendanceReport.objects.filter(student_id=student.id,status=False).count()
        leaves = LeaveReportStudent.objects.filter(student_id=student.id,leave_status=1).count()
        attendance_present_student_list.append(attendance) 
        attendance_absent_student_list.append(leaves+absent) 
        student_name_list.append(student.admin.username)  
    return render(request,"hod_template/home_content.html",{"staff_count":staff_count,"subject_count":subject_count,"subject_count_list":subject_count_list,"subject_list":subject_list,"student_count_in_subject_list":student_count_in_subject_list,"attendance_present_staff_list":attendance_present_staff_list,"attendance_absent_staff_list":attendance_absent_staff_list,"staff_name_list":staff_name_list,"student_name_list":student_name_list,"attendance_present_student_list":attendance_present_student_list,"attendance_absent_student_list":attendance_absent_student_list})



def get_class_choices(request):
    segment = request.GET.get('segment')

    SCHOOL_SEGMENT_CHOICES = (
        ("Nursery", "Nursery Level"),
        ("Primary", "Primary Level"),
        ("Secondary", "Secondary Level"),
    )

    NURSERY_CLASS_CHOICES = [
        ("Baby", "Baby"),
        ("KG1", "KG1"),
        ("KG2", "KG2")
    ]

    PRIMARY_CLASS_CHOICES = [
        ("I", "I"),
        ("II", "II"),
        ("III", "III"),
        ("IV", "IV"),
        ("V", "V"),
        ("VI", "VI")
    ]

    SECONDARY_CLASS_CHOICES = [
        ("Form I", "Form I"),
        ("Form II", "Form II"),
        ("Form III", "Form III"),
        ("Form IV", "Form IV")
    ]

    if segment == "Nursery":
        choices = NURSERY_CLASS_CHOICES
    elif segment == "Primary":
        choices = PRIMARY_CLASS_CHOICES
    elif segment == "Secondary":
        choices = SECONDARY_CLASS_CHOICES
    else:
        choices = []

    return JsonResponse({'choices': choices})

def add_staff(request):  
    forms = AddStaffForm()  
    return render(request,"hod_template/add_staff.html",{"forms":forms})

def add_staff_save(request):
    if request.method!= "POST":
        return HttpResponse("Method not allowed")
    
    else:
        forms = AddStaffForm(request.POST)
        
        if forms.is_valid():
            email=forms.cleaned_data["email"] 
            password=forms.cleaned_data["password"]          
            first_name=forms.cleaned_data["first_name"]
            last_name=forms.cleaned_data["last_name"]
            username=forms.cleaned_data["username"]            
            address=forms.cleaned_data["address"]            
            try:
                 user= CustomUser.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name,user_type=2)
                 user.staffs.address = address
                 user.save()
                 messages.success(request,"Successfully added staff")
                 return HttpResponseRedirect(reverse("addstaff"))  
             
            except:
                messages.error(request,"failed to save staff")
                return HttpResponseRedirect(reverse("addstaff"))
    
        else:
            forms = AddStaffForm(request.POST)   
            return render(request,"hod_template/add_student.html",{"forms":forms})     
        

        

  


 
def add_subject_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    
    else:        
        forms = AddSubjectForm(request.POST)
        if forms.is_valid():
            subject_name = forms.cleaned_data["subject_name"]            
            staff_id = forms.cleaned_data["staff_name"]
            
            try:
                
                staff = CustomUser.objects.get(id=staff_id)
                
                subject = Subject(subject_name=subject_name, staff_id=staff)
                subject.save()
                
                messages.success(request, "Subject successfully added")
                return HttpResponseRedirect(reverse("addsubject"))  
            
            except ObjectDoesNotExist:
                messages.error(request, "Failed to add subject.  or staff not found.")
                return HttpResponseRedirect(reverse("addsubject"))
            
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return HttpResponseRedirect(reverse("addsubject"))
            

def add_subject(request):
    forms = AddSubjectForm()
    return render(request,"hod_template/add_subject.html",{"forms":forms})    
               
 
def add_student_save(request):
    if request.method == "POST":
        try:
            # Extract form data
            segment = request.POST.get('school_segment')
            full_name = request.POST.get('full_name')
            address = request.POST.get('address')
            street_address = request.POST.get('street_address')
            house_number = request.POST.get('house_number')
            health_status = request.POST.get('health_status')
            physical_disability = request.POST.get('physical_disability')
            student_photo = request.FILES.get('student_photo')
            birth_certificate_id = request.POST.get('birth_certificate_id')
            birth_certificate_photo = request.FILES.get('birth_certificate_photo')
            allergies = request.POST.get('allergies')
            current_year = request.POST.get('current_year')
            is_finished = request.POST.get('is_finished')
            current_class = request.POST.get('current_class')
            gender = request.POST.get('student_gender')
            
            father_name = request.POST.get('father_name')
            father_phone_number = request.POST.get('father_phone_number')
            father_address = request.POST.get('father_address')
            father_street_address = request.POST.get('father_street_address')
            father_house_number = request.POST.get('father_house_number')
            father_national_id = request.POST.get('father_national_id')
            father_status = request.POST.get('father_status')
            father_profession = request.POST.get('father_occupation')
            
            mother_name = request.POST.get('mother_name')
            mother_phone_number = request.POST.get('mother_phone_number')
            mother_address = request.POST.get('mother_address')
            mother_street_address = request.POST.get('mother_street_address')
            mother_house_number = request.POST.get('mother_house_number')
            mother_national_id = request.POST.get('mother_national_id')
            mother_status = request.POST.get('mother_status')
            mother_profession = request.POST.get('mother_occupation')
            
            guardian_name = request.POST.get('guardian_name')
            guardian_phone_number = request.POST.get('guardian_phone_number')
            guardian_address = request.POST.get('guardian_address')
            guardian_street_address = request.POST.get('guardian_street_address')
            guardian_house_number = request.POST.get('guardian_house_number')
            guardian_national_id = request.POST.get('guardian_national_id')
            guardian_gender = request.POST.get('guardian_gender')
            guardian_status = request.POST.get('guardian_status')
            guardian_profession = request.POST.get('guardian_occupation')
            
            sponsor_name = request.POST.get('sponsor_name')
            sponsor_phone_number = request.POST.get('sponsor_phone_number')
            sponsor_street_address = request.POST.get('sponsor_street_address')
            sponsor_address = request.POST.get('sponsor_address')
            sponsor_house_number = request.POST.get('sponsor_house_number')
            sponsor_national_id = request.POST.get('sponsor_national_id')
            sponsor_status = request.POST.get('sponsor_status')
            sponsor_profession = request.POST.get('sponsor_profession')
            

            # Save the form data to the database
            try:
                # Save the student's profile picture
                student_photo_url = None
                if student_photo:
                    fs = FileSystemStorage()
                    filename = fs.save(student_photo.name, student_photo)
                    student_photo_url = fs.url(filename)

                # Save the birth certificate photo
                birth_certificate_photo_url = None
                if birth_certificate_photo:
                    fs = FileSystemStorage()
                    filename = fs.save(birth_certificate_photo.name, birth_certificate_photo)
                    birth_certificate_photo_url = fs.url(filename)

                # Save the student record
                username = full_name.replace(" ", "")  # Remove spaces from full_name to create a username
                first_name, *last_name_parts = full_name.split(" ")  # Split full_name into first_name and last_name parts

# Join the remaining last_name_parts if any
                last_name = " ".join(last_name_parts) if last_name_parts else None
# Create the user with the updated values
                user = CustomUser.objects.create_user(username=username, password=None, email=None, first_name=first_name, last_name=last_name, user_type=3)

# Create a new instance of the Students model
                student = Students()
                student.full_name = full_name
                student.address = address
                student.street_address = street_address
                student.house_number = house_number
                student.health_status = health_status
                student.physical_disability = physical_disability
                student.profile_pic = student_photo_url
                student.gender = gender
                student.birth_certificate_id = birth_certificate_id
                student.birth_certificate_photo = birth_certificate_photo_url
                student.allergies = allergies
                student.current_year = current_year
                student.school_segment = segment
                student.current_class = current_class
                student.is_finished = is_finished

                student.father_name = father_name
                student.father_phone_number = father_phone_number
                student.father_address = father_address
                student.father_street_address = father_street_address
                student.father_house_number = father_house_number
                student.father_national_id = father_national_id
                student.father_status = father_status
                student.father_profession = father_profession

                student.mother_name = mother_name
                student.mother_phone_number = mother_phone_number
                student.mother_address = mother_address
                student.mother_street_address = mother_street_address
                student.mother_house_number = mother_house_number
                student.mother_national_id = mother_national_id
                student.mother_status = mother_status
                student.mother_profession = mother_profession

                student.guardian_name = guardian_name
                student.guardian_phone_number = guardian_phone_number
                student.guardian_street_address = guardian_street_address
                student.guardian_address = guardian_address
                student.guardian_house_number = guardian_house_number
                student.guardian_national_id = guardian_national_id
                student.guardian_status = guardian_status
                student.guardian_gender = guardian_gender
                student.guardian_profession = guardian_profession

                student.sponsor_name = sponsor_name
                student.sponsor_phone_number = sponsor_phone_number
                student.sponsor_address = sponsor_address
                student.sponsor_street_address = sponsor_street_address
                student.sponsor_house_number = sponsor_house_number
                student.sponsor_national_id = sponsor_national_id
                student.sponsor_status = sponsor_status
                student.sponsor_profession = sponsor_profession

# Assign the student instance to the user's 'students' attribute
                user.students = student                      
               
                student.save()
                user.save()
                 
                messages.success(request, "Successfully added student")
                return redirect("add_student")
            except Exception as e:
                messages.error(request, f"Error saving student record: {str(e)}")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect("add_student")
        

def add_student(request):
    form = AddStudentForm()
    if request.method == 'POST':
        # Process form submission
        pass

    context = {
        'form': form
    }
    return render(request, 'hod_template/add_student.html', context)

def single_student_detail(request,student_id):
    return render(request,"hod_template/student_details.html")  

  
def manage_student(request):
    per_page = request.GET.get('per_page', 3)  # Get the number of items to display per page from the request
    students = Students.objects.all()
    paginator = Paginator(students, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "hod_template/manage_student.html", {"students": students, "page_obj": page_obj})
 
def student_list(request):
    search_query = request.GET.get('search', '')
    students = Students.objects.all()
    
    if search_query:
        students = students.filter(registration_number__icontains=search_query)
    
    paginator = Paginator(students, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "paginator.html", {"students": students, "page_obj": page_obj})  
  

  
def manage_staff(request):       
    per_page = request.GET.get('per_page', 3)  # Get the number of items to display per page from the request
    staffs=Staffs.objects.all() 
    paginator = Paginator(staffs, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"hod_template/manage_staff.html",{"staffs":staffs,"page_obj":page_obj})  


def manage_subject(request):   
    per_page = request.GET.get('per_page', 3)  # Get the number of items to display per page from the request
    subjects =Subject.objects.all() 
    paginator = Paginator(subjects, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"hod_template/manage_subject.html",{"subjects":subjects,"page_obj":page_obj})
  
def edit_staff(request,staff_id): 
    request.session['staff_id'] = staff_id 
    staffs = Staffs.objects.get(admin = staff_id)
    forms = EditStaffForm()
    forms.fields['email'].initial = staffs.admin.email
    forms.fields['first_name'].initial = staffs.admin.first_name
    forms.fields['last_name'].initial = staffs.admin.last_name
    forms.fields['username'].initial = staffs.admin.username
    forms.fields['address'].initial = staffs.address
    return render(request,"hod_template/edit_staff.html",{"forms":forms,"id":staff_id,"username":staffs.admin.username})     


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    
    
    staff_id = request.session.get("staff_id")
    if staff_id is None :
        return HttpResponseRedirect(reverse("manage_staff"))
    
    forms = EditStaffForm(request.POST)    
    if forms.is_valid():           
        first_name = forms.cleaned_data["first_name"]
        last_name = forms.cleaned_data["last_name"]
        email = forms.cleaned_data["email"]
        address = forms.cleaned_data["address"]
        username = forms.cleaned_data["username"]
        
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
        
            staff = Staffs.objects.get(admin_id=staff_id)
            staff.address = address
            staff.save()
            messages.success(request, "Successfully edited staff")
            return HttpResponseRedirect(reverse("edit_staff", args=[staff_id]))
        
        except CustomUser.DoesNotExist:
            messages.error(request, "Failed to edit staff. User does not exist.")
            return HttpResponseRedirect(reverse("edit_staff", args=[staff_id]))
        
        except Staffs.DoesNotExist:
            messages.error(request, "Failed to edit staff. Staff does not exist.")
            return HttpResponseRedirect(reverse("edit_staff", args=[staff_id]))
        
def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")

    student_id = request.session.get("student_id")
    if student_id is None:
        return HttpResponseRedirect(reverse("manage_student"))

    form = EditStudentForm(request.POST, request.FILES)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        email = cleaned_data["email"]
        first_name = cleaned_data["first_name"]
        last_name = cleaned_data["last_name"]
        address = cleaned_data["address"]
        username = cleaned_data["username"]
        sex = cleaned_data["sex"]
       
        session_year = cleaned_data["session_year_id"]
        

        profile_pic_url = None
        profile_pic = request.FILES.get("profile_pic")
        if profile_pic:
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

        try:
            user = CustomUser.objects.get(id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            student = Students.objects.get(admin_id=student_id)
            student.address = address
            student.gender = sex
            session_d = SessionYearModel.objects.get(id = session_year)
            student.session_id = session_d
       
            if profile_pic_url:
                student.profile_pic = profile_pic_url
            student.save()

            del request.session['student_id']
            messages.success(request, "Successfully edited student")
            return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": student_id}))

        except (CustomUser.DoesNotExist, Students.DoesNotExist):
            messages.error(request, "Failed to edit student")
            return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": student_id}))

    students = Students.objects.get(admin=student_id)
    return render(request, "hod_template/edit_student.html", {"forms": form, "id": student_id, "username": students.admin.username})

   
def edit_student(request,student_id):
    request.session['student_id'] = student_id       
    students=Students.objects.get(admin=student_id)  
    forms = EditStudentForm()
    forms.fields['email'].initial  = students.admin.email    
    forms.fields['first_name'].initial  = students.admin.first_name
    forms.fields['last_name'].initial  = students.admin.last_name
    forms.fields['username'].initial  = students.admin.username
    forms.fields['address'].initial  = students.address
  
    forms.fields['sex'].initial  = students.gender
    forms.fields['session_year_id'].initial  = students.session_id  
    forms.fields['profile_pic'].initial  = students.profile_pic
    return render(request,"hod_template/edit_student.html",{"forms":forms,"id":student_id,"username":students.admin.username})     

    
      


def edit_subject(request,subject_id):  
    request.session['subject_id'] = subject_id
    subjects = Subject.objects.get(id = subject_id)
    forms = AddSubjectForm() 
    forms.fields['subject_name'].initial =subjects.subject_name
    
    forms.fields['staff_name'].initial = subjects.staff_id.id
    return render(request,"hod_template/edit_subject.html",{"forms":forms,"id":subject_id}) 

def edit_subject_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    
    subject_id = request.session.get("subject_id")
    if subject_id is None:
        return HttpResponseRedirect(reverse("manage_subject"))
    
    
    forms = AddSubjectForm(request.POST)
    if forms.is_valid():
        subject_name = forms.cleaned_data["subject_name"]
        
        staff_id = forms.cleaned_data["staff_name"]
        

        try:
            subject_modal = Subject.objects.get(id=subject_id)
            subject_modal.subject_name = subject_name

            staff_modal = CustomUser.objects.get(id=staff_id)
            subject_modal.staff_id = staff_modal

      

            subject_modal.save()
            messages.success(request, "Subject successfully edited")
            return HttpResponseRedirect(reverse("edit_subject", args=[subject_id]))

        except Subject.DoesNotExist:
            messages.error(request, "Failed to edit subject. Subject does not exist.")
            return HttpResponseRedirect(reverse("edit_subject", args=[subject_id]))

        except CustomUser.DoesNotExist:
            messages.error(request, "Failed to edit subject. Staff does not exist.")
            return HttpResponseRedirect(reverse("edit_subject", args=[subject_id]))


    subjects=Subject.objects.all()  
    return render(request,"hod_template/manage_subject.html",{"subjects":subjects})     


def manage_session(request):
    forms = AddSessionYearForm()
    return render(request,"hod_template/manage_session.html",{"forms":forms})

  
  
def manage_session_save(request):
    if request.method!= "POST":  
        return HttpResponseRedirect(reverse("manage_session"))
    
    else:
        forms = AddSessionYearForm(request.POST)
        
        if forms.is_valid():
            session_start = forms.cleaned_data["session_start"]
            session_end = forms.cleaned_data["session_end"] 
            
            try:                          
               sessions = SessionYearModel(session_start_year=session_start,session_end_year=session_end)
               sessions.save()
               messages.success(request,"session year is successfully added")
               return HttpResponseRedirect(reverse("manage_session"))

            except:
                messages.error(request,"add of session year failed")
                return HttpResponseRedirect(reverse("manage_session"))
        
            
@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_object = CustomUser.objects.filter(email=email).exists()
    if user_object:
        return HttpResponse(True)
    
    else:
        return HttpResponse(False)
    
    
@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_object = CustomUser.objects.filter(username=username).exists()
    if user_object:
        return HttpResponse(True)
    
    else:
        return HttpResponse(False)


def  student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    return render(request,"hod_template/student_feedback_message.html",{"feedbacks":feedbacks})

def staff_feedback_message(request):
    feedbacks = FeedBackStaff.objects.all()
    return render(request,"hod_template/staff_feedback_message.html",{"feedbacks":feedbacks})


@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")
    try:    
      feedback = FeedBackStudent.objects.get(id=feedback_id)
      feedback.feedback_reply = feedback_message
      feedback.save() 
      return HttpResponse(True)
    except:
       return HttpResponse(False)  
   
            
@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")
    try:    
      feedback = FeedBackStaff.objects.get(id=feedback_id)
      feedback.feedback_reply = feedback_message
      feedback.save() 
      return HttpResponse(True)
    except:
       return HttpResponse(False)           
   
def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    return render(request,"hod_template/student_leave_view.html",{"leaves":leaves})



def student_approve_leave(request,leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))

def student_disapprove_leave(request,leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def staff_leave_view(request):
    leaves = LeaveReportStaffs.objects.all()
    return render(request,"hod_template/staff_leave_view.html",{"leaves":leaves})

def staff_approve_leave(request,leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def staff_disapprove_leave(request,leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def admin_view_attendance(request):
    subjects = Subject.objects.all()   
    session_years = SessionYearModel.objects.all()
    return render(request,"hod_template/admin_view_attendance.html",{"subjects":subjects,"session_years":session_years})

@csrf_exempt
def admin_get_student_attendance(request):
    attendance_date=request.POST.get("attendance_date_id")     
    attendance_date_id=Attendance.objects.get(id=attendance_date)
    attendance_data =AttendanceReport.objects.filter(attendance_id=attendance_date_id)   
    
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def admin_get_attendance_date(request):
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
 
 
def admin_save_updateattendance(request):
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get("attendance_date")     
    attendance=Attendance.objects.get(id=attendance_date)     
    json_sstudent=json.loads(student_ids)



    try:
        for stud in json_sstudent:
             student=Students.objects.get(admin_id=stud['id'])
             attendance_report=AttendanceReport.objects.get(student_id=student,attendance_id=attendance)
             attendance_report.status =stud["status"]
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")
    
    

def  admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request,"hod_template/admin_profile.html",{"user":user})  

def edit_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    
    else:
       first_name = request.POST.get("first_name")
       last_name = request.POST.get("last_name")
       password = request.POST.get("password")
       try:           
          customuser = CustomUser.objects.get(id=request.user.id)
          customuser.first_name = first_name
          customuser.last_name = last_name
          if password!= "" and password!=None:
              customuser.set_password(password)     
                         
          customuser.save()
          messages.success(request,"profile is successfully edited")
          return HttpResponseRedirect(reverse("admin_profile"))
      
       except:
            messages.error(request,"editing  of profile  failed")
            return HttpResponseRedirect(reverse("admin_profile"))
        
    



       
    