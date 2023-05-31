from django import forms

from student_management_app.models import Courses, SessionYearModel, Staffs


class DateInput(forms.DateInput):
    input_type = "date"

class AddStudentForm(forms.Form):
    registration_number = forms.CharField(label='REGISTRATION NUMBER', max_length=50, widget=forms.EmailInput(attrs={"class":"form-control", "autocomplete":"off"}))
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label='First Name', max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label='Last Name', max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label='Address', max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    
    # Course choices
    course_list = []
    courses = Courses.objects.all()
    for course in courses:
        small_course = (course.id, course.Course_name)
        course_list.append(small_course)
    course_name = forms.ChoiceField(label='Course', choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    
    # Session year choices
    session_year_list = []
    sessions = SessionYearModel.objects.all()
    for session in sessions:
        small_session_list = (session.id, str(session.session_start_year) + " To " + str(session.session_end_year))
        session_year_list.append(small_session_list)
    session_year_id = forms.ChoiceField(label='Session Year', choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    
    # Gender choices
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )
    sex = forms.ChoiceField(label='Sex', choices=gender_choice, widget=forms.Select(attrs={"class":"form-control"}))
    
    # Additional fields
    street = forms.CharField(label='Street', max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    house_number = forms.CharField(label='House Number', max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    shea_name = forms.CharField(label="Shea's Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    shehas_phone_number = forms.CharField(label="Sheha's Phone Number", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    father_name = forms.CharField(label="Father's Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    father_phone_number = forms.CharField(label="Father's Phone Number", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    father_street_address = forms.CharField(label="Father's Street Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    father_house_number = forms.CharField(label="Father's House Number", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    general_address = forms.CharField(label='General Address', max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    mother_name = forms.CharField(label="Mother's Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    mother_street_address = forms.CharField(label="Mother's Street Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    mother_house_number = forms.CharField(label="Mother's House Number", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    mother_phone_number = forms.CharField(label="Mother's House Number", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    
    
class EditStudentForm(forms.Form):
    email = forms.CharField(label='EMAIL',max_length=50,widget = forms.EmailInput(attrs={"class":"form-control"}))    
    first_name = forms.CharField(label='First Name',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label='Last Name',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username  = forms.CharField(label='Username',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label='Address',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    course_list = []    
    courses = Courses.objects.all()    
    for course in courses:
           small_course = (course.id,course.Course_name)
           course_list.append(small_course)
           
   
        # course_list = []    
    
    session_year_list = []    
    sessions = SessionYearModel.objects.all()    
    for session in sessions:
           small_session_list = (session.id,str(session.session_start_year)+" To "+str(session.session_end_year))
           session_year_list.append(small_session_list)
           
    
        # session_year_list = []     
    gender_choice = (
        ("Male","Male"),
        ("Female","Female")
    )    
    course_name = forms.ChoiceField(label='Course', choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))    
    sex = forms.ChoiceField(label='Sex', choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id= forms.ChoiceField(label='Session Year',choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label='Profile Pic',max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}),required=False)
    
    
    
class AddStaffForm(forms.Form):
    email = forms.CharField(label='EMAIL',max_length=50,widget = forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label='Password',max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label='First Name',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label='Last Name',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username  = forms.CharField(label='Username',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label='Address',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    
class EditStaffForm(forms.Form):
    email = forms.CharField(label='EMAIL',max_length=50,widget = forms.EmailInput(attrs={"class":"form-control"}))
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
      small_staff = (staff.admin_id, staff.admin.first_name + " " + staff.admin.last_name)
      staff_list.append(small_staff)   
    
    
    course_name = forms.ChoiceField(label='Course Name', choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    staff_name = forms.ChoiceField(label='Staff Name', choices=staff_list, widget=forms.Select(attrs={"class":"form-control"}))
 
class AddSessionYearForm(forms.Form):
    session_start = forms.DateField(label='Session start year',widget = forms.DateInput(attrs={"class":"form-control","placeholder":"Enter session start year","type":"date"}))
    session_end = forms.DateField(label='Session end year',widget = forms.DateInput(attrs={"class":"form-control","placeholder":"Enter session end year","type":"date"}))
    

  