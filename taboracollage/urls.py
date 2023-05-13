"""
URL configuration for taboracollage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
from taboracollage import settings
from student_management_app import StudentView, views,HodView,StaffView

urlpatterns = [
    path('', include('student_management_app.urls')),
    path('admin/', admin.site.urls),
    path('', views.ShowLogin, name='login'),
    path('GetUserDetails', views.GetUserDetails, name='GetUserDetails'),
    path('dologin', views.DoLogin, name='DoLogin'),
    path('admin_home', HodView.admin_home, name='admin_home'),   
    path('add_staff', HodView.add_staff, name='addstaff'),
    path('add_staff_save', HodView.add_staff_save, name='add_staff_save'),   
    path('add_course', HodView.add_course, name='addcourse'),   
    path('add_course_save', HodView.add_course_save, name='addcoursesave'),    
    path('add_student', HodView.add_student, name='add_student'),   
    path('add_student_save', HodView.add_student_save, name='add_student_save'),    
    path('add_subject', HodView.add_subject, name='addsubject'),   
    path('add_subject_save', HodView.add_subject_save, name='addsubjectsave'),    
    path('manage_staff', HodView.manage_staff, name='manage_staff'),   
    path('manage_student', HodView.manage_student, name='manage_student'),   
    path('manage_course', HodView.manage_course, name='manage_course'),   
    path('manage_subject', HodView.manage_subject, name='manage_subject'),   
    path('edit_staff/<str:staff_id>', HodView.edit_staff, name='edit_staff'),   
    path('edit_staff_save', HodView.edit_staff_save, name='edit_staff_save'),      
    path('edit_student/<str:student_id>', HodView.edit_student, name='edit_student'),   
    path('edit_student_save', HodView.edit_student_save, name='edit_student_save'),   
    path('edit_course/<str:course_id>', HodView.edit_course, name='edit_course'),   
    path('edit_course_save', HodView.edit_course_save, name='edit_course_save'),   
    path('edit_subject/<str:subject_id>', HodView.edit_subject, name='edit_subject'),   
    path('edit_subject_save', HodView.edit_subject_save, name='edit_subject_save'),
    path('manage_session', HodView.manage_session, name='manage_session'),   
    path('manage_session_save', HodView.manage_session_save, name='manage_session_save'),
    
    # staff url paths  
    path('staff_home', StaffView.staff_home, name='staff_home'),  
    path('staff_take_attendance', StaffView.staff_take_attendance, name='staff_take_attendance'),  
    path('get_students', StaffView.get_students, name='get_students'),  
    path('save_attendance_data', StaffView.save_attendance_data, name='save_attendance_data'),  
     
    # student url paths  
    path('student_home', StudentView.student_home, name='student_home'),       
    path('logout_user', views.logout_user, name='logout_user'),  # Move this line here
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)