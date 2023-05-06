from django import forms

from student_management_app.models import Courses


class DateInput(forms.DateInput):
    input_type = "date"

class AddStudentForm(forms.Form):
    email = forms.CharField(label='EMAIL',max_length=50,widget = forms.EmailInput())
    password = forms.CharField(label='Password',max_length=50,widget=forms.PasswordInput())
    first_name = forms.CharField(label='First Name',max_length=50)
    last_name = forms.CharField(label='Last Name',max_length=50)
    username  = forms.CharField(label='Username',max_length=50)
    address = forms.CharField(label='Address',max_length=50)
    courses = Courses.objects.all()
    course_list = []
    for course in courses:
        small_course = (course.id,course.Course_name)
        course_list.append(small_course)
        
    gender_choice = (
        ("Male","Male"),
        ("Female","Female")
    )    
    course_name = forms.ChoiceField(label='Course', choices=course_list)    
    sex = forms.ChoiceField(label='Sex', choices=gender_choice)
    session_start= forms.CharField(label='Session Start',widget=DateInput())
    session_end = forms.CharField(label='Session End',widget=DateInput())
    profile_pic = forms.FileField(label='Profile Pic',max_length=50)
    