from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from student_management_app.forms import AddCourseForm, AddStaffForm, AddStudentForm, AddSubjectForm, EditStudentForm
from student_management_app.models import Courses, CustomUser, Staffs, Students, Subject
from django.core.exceptions import ObjectDoesNotExist



def HodViews(request):
    return render(request,"hod_template/home_content.html")


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
        
def add_course_save(request):
    if request.method!= "POST":
        return HttpResponse("Method not allowed")
    
    else:
        forms = AddCourseForm(request.POST,request.FILES)
        
        if forms.is_valid():            
            course=forms.cleaned_data["course"]
            try:            
            # course_model = Courses.objects.create()
              course_model = Courses(Course_name = course)
              course_model.save()
              messages.success(request,"course Successfully added")
              return HttpResponseRedirect(reverse("addcourse"))  
          
            except:  
                messages.error(request,"failed to add course")
                return HttpResponseRedirect(reverse("addcourse"))
        

def add_course(request):
    forms = AddCourseForm()
    return render(request,"hod_template/add_course.html",{"forms":forms})   


 
def add_subject_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    
    else:        
        forms = AddSubjectForm(request.POST)
        if forms.is_valid():
            subject_name = forms.cleaned_data["subject_name"]
            course_id = forms.cleaned_data["course_name"]
            staff_id = forms.cleaned_data["staff_name"]
            
            try:
                course = Courses.objects.get(id=course_id)
                staff = CustomUser.objects.get(id=staff_id)
                
                subject = Subject(subject_name=subject_name, course_id=course, staff_id=staff)
                subject.save()
                
                messages.success(request, "Subject successfully added")
                return HttpResponseRedirect(reverse("addsubject"))  
            
            except ObjectDoesNotExist:
                messages.error(request, "Failed to add subject. Course or staff not found.")
                return HttpResponseRedirect(reverse("addsubject"))
            
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return HttpResponseRedirect(reverse("addsubject"))
            

def add_subject(request):
    forms = AddSubjectForm()
    return render(request,"hod_template/add_subject.html",{"forms":forms})    
               
 
def add_student_save(request):
    if request.method!= "POST":
        return HttpResponse("Method not allowed")    
    else:
        forms = AddStudentForm(request.POST,request.FILES)
        
        if forms.is_valid():            
            first_name=forms.cleaned_data["first_name"]
            last_name=forms.cleaned_data["last_name"]
            email=forms.cleaned_data["email"]
            password=forms.cleaned_data["password"]
            address=forms.cleaned_data["address"]
            username=forms.cleaned_data["username"] 
            sex=forms.cleaned_data["sex"]
            course_id=forms.cleaned_data["course_name"] 
            session_start=forms.cleaned_data["session_start"]
            session_end=forms.cleaned_data["session_end"]  
        
            if request.FILES.get("profile_pic"):
               profile_pic=request.FILES.get("profile_pic",False)  
               fs = FileSystemStorage()        
               filename = fs.save(profile_pic.name,profile_pic)
               profile_pic_url = fs.url(filename)
           
            else:
               profile_pic_url = None  
            try:
                user= CustomUser.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name,user_type=3)
                user.students.address = address
                course_obj = Courses.objects.get(id=course_id)             
                user.students.course_id = course_obj
                user.students.session_start_year = session_start
                user.students.session_end_year = session_end
                user.students.gender = sex
                user.students.profile_pic =profile_pic_url             
                user.save()
                messages.success(request,"Successfully added students")
                return HttpResponseRedirect(reverse("add_student"))  
             
            except:
               messages.error(request,"failed to add students")
               return HttpResponseRedirect(reverse("add_student")) 
           
        else:
            forms = AddStudentForm(request.POST)   
            return render(request,"hod_template/add_student.html",{"forms":forms}) 
        

def add_student(request):    
    forms  = AddStudentForm()
    return render(request,"hod_template/add_student.html",{"forms":forms})   

  
def manage_student(request):  
    students=Students.objects.all()  
    return render(request,"hod_template/manage_student.html",{"students":students})   
  
def manage_course(request):  
    courses=Courses.objects.all()  
    return render(request,"hod_template/manage_course.html",{"courses":courses})   
  
def manage_staff(request):  
    staffs=Staffs.objects.all()  
    return render(request,"hod_template/manage_staff.html",{"staffs":staffs})  
def manage_subject(request):
    subjects =Subject.objects.all() 
    return render(request,"hod_template/manage_subject.html",{"subjects":subjects})
  
def edit_staff(request,staff_id):  
    staffs=Staffs.objects.get(admin_id=staff_id)  
    return render(request,"hod_template/edit_staff.html",{"staffs":staffs,"id":staff_id})  


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    
    else:
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        username = request.POST.get("username")
        
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
        course_id = cleaned_data["course_name"]
        session_start = cleaned_data["session_start"]
        session_end = cleaned_data["session_end"]

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
            student.session_start_year = session_start
            student.session_end_year = session_end
            course = Courses.objects.get(id=course_id)
            student.course_id = course
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
    forms.fields['course_name'].initial  = students.course_id
    forms.fields['sex'].initial  = students.gender
    forms.fields['session_start'].initial  = students.session_start_year
    forms.fields['session_end'].initial  = students.session_end_year
    forms.fields['profile_pic'].initial  = students.profile_pic
    return render(request,"hod_template/edit_student.html",{"forms":forms,"id":student_id,"username":students.admin.username})     

    
def edit_course(request,course_id):  
    courses=Courses.objects.get(id=course_id)  
    return render(request,"hod_template/edit_course.html",{"courses":courses,"id": course_id})  

def edit_course_save(request):  
    if request.method!= "POST":
        return HttpResponse("Method not allowed")
    
    else:
        course_name = request.POST.get("course")
        course_id = request.POST.get("course_id")
        
        try:
            course_modal = Courses.objects.get(id=course_id)
            course_modal.Course_name = course_name
            course_modal.save()
            
            messages.success(request,"course is successfully added")
            return HttpResponseRedirect(reverse("edit_course",args=[course_id]))
        except:
            messages.error(request,"course failed to be edited")
            return HttpResponseRedirect(reverse("edit_course",args=[course_id]))
                
            
    subjects=Subject.objects.all()  
    return render(request,"hod_template/manage_subject.html",{"subjects":subjects})       


def edit_subject(request,subject_id):  
    subject=Subject.objects.get(id=subject_id)  
    courses= Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type = 2)
    return render(request,"hod_template/edit_subject.html",{"subject":subject,"staffs":staffs, "courses":courses,"id":subject_id}) 

def edit_subject_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")

    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        course_id = request.POST.get("course")
        staff_id = request.POST.get("staff")

        try:
            subject_modal = Subject.objects.get(id=subject_id)
            subject_modal.subject_name = subject_name

            staff_modal = CustomUser.objects.get(id=staff_id)
            subject_modal.staff_id = staff_modal

            course_modal = Courses.objects.get(id=course_id)
            subject_modal.course_id = course_modal

            subject_modal.save()
            messages.success(request, "Subject successfully edited")
            return HttpResponseRedirect(reverse("edit_subject", args=[subject_id]))

        except Subject.DoesNotExist:
            messages.error(request, "Failed to edit subject. Subject does not exist.")
            return HttpResponseRedirect(reverse("edit_subject", args=[subject_id]))

        except CustomUser.DoesNotExist:
            messages.error(request, "Failed to edit subject. Staff does not exist.")
            return HttpResponseRedirect(reverse("edit_subject", args=[subject_id]))

        except Courses.DoesNotExist:
            messages.error(request, "Failed to edit subject. Course does not exist.")
            return HttpResponseRedirect(reverse("edit_subject", args=[subject_id])) 
    subjects=Subject.objects.all()  
    return render(request,"hod_template/manage_subject.html",{"subjects":subjects})     



       
        
            
        