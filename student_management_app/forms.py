from django import forms

from student_management_app.models import Courses, Staffs


class DateInput(forms.DateInput):
    input_type = "date"

class AddStudentForm(forms.Form):
    email = forms.CharField(label='EMAIL',max_length=50,widget = forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label='Password',max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label='First Name',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label='Last Name',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username  = forms.CharField(label='Username',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label='Address',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    courses = Courses.objects.all()
    course_list = []
    for course in courses:
        small_course = (course.id,course.Course_name)
        course_list.append(small_course)
        
    gender_choice = (
        ("Male","Male"),
        ("Female","Female")
    )    
    course_name = forms.ChoiceField(label='Course', choices=course_list,widget=forms.Select(attrs={"class":"form-control"}))    
    sex = forms.ChoiceField(label='Sex', choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    session_start= forms.CharField(label='Session Start',widget=DateInput(attrs={"class":"form-control"}))
    session_end = forms.CharField(label='Session End',widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label='Profile Pic',max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}))
    
    
class EditStudentForm(forms.Form):
    email = forms.CharField(label='EMAIL',max_length=50,widget = forms.EmailInput(attrs={"class":"form-control"}))    
    first_name = forms.CharField(label='First Name',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label='Last Name',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username  = forms.CharField(label='Username',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label='Address',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    courses = Courses.objects.all()
    course_list = []
    for course in courses:
        small_course = (course.id,course.Course_name)
        course_list.append(small_course)
        
    gender_choice = (
        ("Male","Male"),
        ("Female","Female")
    )    
    course_name = forms.ChoiceField(label='Course', choices=course_list,widget=forms.Select(attrs={"class":"form-control"}))    
    sex = forms.ChoiceField(label='Sex', choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    session_start= forms.CharField(label='Session Start',widget=DateInput(attrs={"class":"form-control"}))
    session_end = forms.CharField(label='Session End',widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label='Profile Pic',max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}),required=False)
    
    
    
class AddStaffForm(forms.Form):
    email = forms.CharField(label='EMAIL',max_length=50,widget = forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label='Password',max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label='First Name',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label='Last Name',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username  = forms.CharField(label='Username',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label='Address',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
  
class AddCourseForm(forms.Form):
    course = forms.CharField(label='Course Name',max_length=50,widget = forms.TextInput(attrs={"class":"form-control"}))
    

class AddSubjectForm(forms.Form):
    subject_name = forms.CharField(label='Subject Name',max_length=50,widget = forms.TextInput(attrs={"class":"form-control"}))
    
    courses = Courses.objects.all()
    staffs = Staffs.objects.all()
    course_list = []
    for course in courses:
        small_course = (course.id,course.Course_name)
        course_list.append(small_course)
    
    staff_list = []
    for staff in staffs:
      small_staff = (staff.id, staff.admin.first_name + " " + staff.admin.last_name)
      staff_list.append(small_staff)
    
    
    
    course_name = forms.ChoiceField(label='Course Name', choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    staff_name = forms.ChoiceField(label='Staff Name', choices=staff_list, widget=forms.Select(attrs={"class":"form-control"}))
 
  