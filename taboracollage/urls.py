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
    path('accounts/',include('django.contrib.auth.urls')),
    path('', views.ShowLogin, name='login'),
    path('GetUserDetails', views.GetUserDetails, name='GetUserDetails'),
    path('dologin', views.DoLogin, name='DoLogin'),
    path('admin_home', HodView.admin_home, name='admin_home'),   
    path('add_staff', HodView.add_staff, name='addstaff'),
    path('add_staff_save', HodView.add_staff_save, name='add_staff_save'),   
    # path('add_course', HodView.add_course, name='addcourse'),   
    # path('add_course_save', HodView.add_course_save, name='addcoursesave'),    
    path('add_student', HodView.add_student, name='add_student'),   
    path('add_student_save', HodView.add_student_save, name='add_student_save'),    
    path('add_subject', HodView.add_subject, name='addsubject'),   
    path('add_subject_save', HodView.add_subject_save, name='addsubjectsave'),    
    path('manage_staff', HodView.manage_staff, name='manage_staff'),   
    path('manage_student', HodView.manage_student, name='manage_student'),   
    # path('manage_course', HodView.manage_course, name='manage_course'),   
    path('manage_subject', HodView.manage_subject, name='manage_subject'),   
    path('edit_staff/<str:staff_id>', HodView.edit_staff, name='edit_staff'),   
    path('edit_staff_save', HodView.edit_staff_save, name='edit_staff_save'),      
    path('edit_student/<str:student_id>', HodView.edit_student, name='edit_student'),   
    path('edit_student_save', HodView.edit_student_save, name='edit_student_save'),   
    # path('edit_course/<str:course_id>', HodView.edit_course, name='edit_course'),   
    # path('edit_course_save', HodView.edit_course_save, name='edit_course_save'),   
    path('edit_subject/<str:subject_id>', HodView.edit_subject, name='edit_subject'),   
    path('edit_subject_save', HodView.edit_subject_save, name='edit_subject_save'),
    path('manage_session', HodView.manage_session, name='manage_session'),   
    path('manage_session_save', HodView.manage_session_save, name='manage_session_save'),
    path('check_email_exist', HodView.check_email_exist, name='check_email_exist'),
    path('check_username_exist', HodView.check_username_exist, name='check_username_exist'),
    path('student_feedback_message', HodView.student_feedback_message, name='student_feedback_message'),
    path('student_feedback_message_replied', HodView.student_feedback_message_replied, name='student_feedback_message_replied'),
    path('staff_feedback_message_replied', HodView.staff_feedback_message_replied, name='staff_feedback_message_replied'),
    path('staff_feedback_message', HodView.staff_feedback_message, name='staff_feedback_message'),
    path('student_leave_view', HodView.student_leave_view, name='student_leave_view'),  
    path('staff_leave_view', HodView.staff_leave_view, name='staff_leave_view'), 
    path('student_approve_leave/<str:leave_id>', HodView.student_approve_leave, name='student_approve_leave'),  
    path('student_disapprove_leave/<str:leave_id>', HodView.student_disapprove_leave, name='student_disapprove_leave'), 
    path('staff_approve_leave/<str:leave_id>', HodView.staff_approve_leave, name='staff_approve_leave'), 
    path('staff_disapprove_leave/<str:leave_id>', HodView.staff_disapprove_leave, name='staff_disapprove_leave'), 
    path('admin_view_attendance', HodView.admin_view_attendance, name='admin_view_attendance'), 
    path('admin_get_student_attendance', HodView.admin_get_student_attendance, name='admin_get_student_attendance'), 
    path('admin_get_attendance_date', HodView.admin_get_attendance_date, name='admin_get_attendance_date'), 
    path('admin_save_updateattendance', HodView.admin_save_updateattendance, name='admin_save_updateattendance'), 
    path('admin_profile', HodView.admin_profile, name='admin_profile'), 
    path('edit_profile_save', HodView.edit_profile_save, name='edit_profile_save'), 
    path('single_student_detail/<str:student_id>', HodView.single_student_detail, name='single_student_detail'),
    path('students', HodView.student_list, name='student-list'), 
    path('get_class_choices', HodView.get_class_choices, name='get_class_choices'),  
    
    # staff url paths  
    path('staff_home', StaffView.staff_home, name='staff_home'),  
    path('staff_take_attendance', StaffView.staff_take_attendance, name='staff_take_attendance'),  
    path('get_students', StaffView.get_students, name='get_students'),  
    path('save_attendance_data', StaffView.save_attendance_data, name='save_attendance_data'),  
    path('get_attendance_date', StaffView.get_attendance_date, name='get_attendance_date'),  
    path('get_student_attendance', StaffView.get_student_attendance, name='get_student_attendance'),  
    path('staff_update_attendance', StaffView.staff_update_attendance, name='staff_update_attendance'),  
    path('save_updateattendance', StaffView.save_updateattendance, name='save_updateattendance'),  
    path('staff_apply_leave', StaffView.staff_apply_leave, name='staff_apply_leave'),  
    path('staff_apply_leave_save', StaffView.staff_apply_leave_save, name='staff_apply_leave_save'),  
    path('staff_sendfeedback', StaffView.staff_sendfeedback, name='staff_sendfeedback'),  
    path('staff_sendfeedback_save', StaffView.staff_sendfeedback_save, name='staff_sendfeedback_save'),  
    path('staff_profile', StaffView.staff_profile, name='staff_profile'),  
    path('staff_profile_save', StaffView.staff_profile_save, name='staff_profile_save'),  
    
   
     
    # student url paths  
    path('student_home', StudentView.student_home, name='student_home'),       
    path('student_view_attendance', StudentView.student_view_attendance, name='student_view_attendance'),       
    path('student_view_attendance_post', StudentView.student_view_attendance_post, name='student_view_attendance_post'),   
    path('student_apply_leave', StudentView.student_apply_leave, name='student_apply_leave'),  
    path('student_apply_leave_save', StudentView.student_apply_leave_save, name='student_apply_leave_save'),  
    path('student_sendfeedback', StudentView.student_sendfeedback, name='student_sendfeedback'),  
    path('student_sendfeedback_save', StudentView.student_sendfeedback_save, name='student_sendfeedback_save'),    
    path('student_profile', StudentView.student_profile, name='student_profile'),    
    path('student_profile_save', StudentView.student_profile_save, name='student_profile_save'),    
    path('logout_user', views.logout_user, name='logout_user'),  # Move this line here
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)