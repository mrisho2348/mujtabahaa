from django import urls
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from student_management_app.forms import AddStudentForm
from student_management_app.models import Courses, CustomUser, Staffs, Students, Subject


def HodViews(request):
    return render(request,"hod_template/home_content.html")


def add_staf(request):    
    return render(request,"hod_template/add_staff.html")

def add_staff_save(request):
    if request.method!= "POST":
        return HttpResponse("Method not allowed")
    
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        username = request.POST.get("username")  
        try:
             user= CustomUser.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name,user_type=2)
             user.staffs.address = address
             user.save()
             messages.success(request,"Successfully added staff")
             return HttpResponseRedirect("/add_staff")  
             
        except:
            messages.error(request,"failed to save staff")
            return HttpResponseRedirect("/add_staff")
        
        
def add_course_save(request):
    if request.method!= "POST":
        return HttpResponse("Method not allowed")
    
    else:
        
        course = request.POST.get("course")
        try:            
          # course_model = Courses.objects.create()
          course_model = Courses(Course_name = course)
          course_model.save()
          messages.success(request,"course Successfully added")
          return HttpResponseRedirect("/add_course")  
          
        except:  
            messages.error(request,"failed to add course")
            return HttpResponseRedirect("/add_course")
        

def add_course(request):
    return render(request,"hod_template/add_course.html")   


 
def add_subject_save(request):
    if request.method!= "POST":
        return HttpResponse("Method not allowed")
    
    else:        
        subject_name= request.POST.get("subject_name")
        course_id = request.POST.get("course")
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id = staff_id)
        try:            
          # course_model = Courses.objects.create()
          subject = Subject(subject_name=subject_name,course_id=course,staff_id=staff)
          subject.save()
          messages.success(request,"subject Successfully added")
          return HttpResponseRedirect("/add_subject")  
          
        except:  
            messages.error(request,"failed to add subject")
            return HttpResponseRedirect("/add_subject")
        

def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/add_subject.html",{"staffs":staffs,"courses":courses})    
               
 
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
                return HttpResponseRedirect("/add_student")  
             
            except:
               messages.error(request,"failed to add students")
               return HttpResponseRedirect("/add_student") 
           
        else:
            forms = AddStudentForm(request.POST)   
            return render(request,"hod_template/add_student.html",{"forms":forms}) 
        

def add_student(request):
    courses = Courses.objects.all()
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
    if request.method!= "POST":
        return HttpResponse("Method not allowed")  
    
    else:
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        username = request.POST.get("username")  
        
        try:
           user = CustomUser.objects.get(id=staff_id)
           user.first_name = first_name
           user.last_name = last_name
           user.email = email
           user.username = username
           user.save()
        
           staff_modal = Staffs.objects.get(admin=staff_id)
           staff_modal.address = address
           staff_modal.save()
           messages.success(request,"Successfully  staff edited")
           return HttpResponseRedirect("/edit_staff/"+staff_id)  
             
        except:
            messages.error(request,"failed to edit staff")
            return HttpResponseRedirect("/edit_staff/"+staff_id)
        
        
def edit_student_save(request):  
    if request.method!= "POST":
        return HttpResponse("Method not allowed")  
    
    else:
        student_id = request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")        
        address = request.POST.get("address")
        username = request.POST.get("username")  
        sex = request.POST.get("sex")
        course_id = request.POST.get("course")
        session_start= request.POST.get("session_start") 
        session_end = request.POST.get("session_end")
        
        if request.FILES.get("profile_pic"):            
            profile_pic = request.FILES.get("profile_pic",False)
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name,profile_pic)
            profile_pic_url = fs.url(filename)
            
        else:
            profile_pic_url = None   
        # profile_pic = request.POST.get("profile_pic")
         
        
        try:
           user = CustomUser.objects.get(id=student_id)
           user.first_name = first_name
           user.last_name = last_name
           user.email = email
           user.username = username
           user.save()
        
           student_modal = Students.objects.get(admin_id=student_id)
           student_modal.address = address
           student_modal.gender = sex
           student_modal.session_start_year = session_start
           student_modal.session_end_year  = session_end        
           courseobj = Courses.objects.get(id =course_id)
           student_modal.course_id = courseobj
           if profile_pic_url!=None:               
             student_modal.profile_pic  = profile_pic_url
           student_modal.save()      
           messages.success(request,"Successfully  student edited")
           return HttpResponseRedirect("/edit_student/"+student_id)  
             
        except:
            messages.error(request,"failed to edit student")
            return HttpResponseRedirect("/edit_student/"+student_id)

   
def edit_student(request,student_id):  
    courses = Courses.objects.all()
    students=Students.objects.get(admin=student_id)  
    return render(request,"hod_template/edit_student.html",{"students":students,"courses":courses,"id":student_id})     

    
def edit_course(request,course_id):  
    courses=Courses.objects.get(id=course_id)  
    return render(request,"hod_template/edit_course.html",{"courses":courses,"id":course_id})  

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
            return HttpResponseRedirect("/edit_course/"+course_id)
        except:
            messages.error(request,"course failed to be edited")
            return HttpResponseRedirect("/edit_course/"+course_id)
                
            
    subjects=Subject.objects.all()  
    return render(request,"hod_template/manage_subject.html",{"subjects":subjects})       


def edit_subject(request,subject_id):  
    subject=Subject.objects.get(id=subject_id)  
    courses= Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type = 2)
    return render(request,"hod_template/edit_subject.html",{"subject":subject,"staffs":staffs, "courses":courses,"id":subject_id}) 

def edit_subject_save(request): 
    if request.method!="POST":
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
            course_modal = Courses.objects.get(id = course_id)
            subject_modal.course_id = course_modal
            subject_modal.save()
            messages.success(request,"subject is successfully edited")
            return HttpResponseRedirect("/edit_subject/"+subject_id)           
            
        except:
            messages.error(request,"subject failed to be edited") 
            return HttpResponseRedirect("/edit_subject/"+subject_id)  
    subjects=Subject.objects.all()  
    return render(request,"hod_template/manage_subject.html",{"subjects":subjects})     



       
        
            
        