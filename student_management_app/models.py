from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects=models.Manager()
class CustomUser(AbstractUser):
    user_type_data = ((1,"HOD"),(2,"Staff"),(3,"Student"))
    user_type = models.CharField(default=1,choices=user_type_data,max_length=10)

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    
class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    fcm_token = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now_add=True)      
    objects = models.Manager()


      
      
class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)    
    staff_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)       
    objects = models.Manager()
    

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
       
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    address = models.TextField()
    street_address = models.CharField(max_length=100)
    house_number = models.CharField(max_length=50)
    health_status = models.CharField(max_length=100)
    physical_disability = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='student_photos')
    birth_certificate_id = models.CharField(max_length=50, blank=True, null=True)
    birth_certificate_photo = models.ImageField(upload_to='birth_certificate_photos', blank=True, null=True)
    allergies = models.CharField(max_length=100, blank=True, null=True)
    current_year = models.IntegerField(blank=True, null=True)
    is_finished = models.BooleanField(default=False)
    school_segment_choices = (
        ("Nursery", "Nursery Level"),
        ("Primary", "Primary Level"),
        ("Secondary", "Secondary Level"),
    )
    school_segment = models.CharField(max_length=50, choices=school_segment_choices)
    current_class = models.CharField(max_length=50)

    father_name = models.CharField(max_length=50)
    father_phone_number = models.CharField(max_length=50)
    father_address = models.TextField()
    father_street_address = models.CharField(max_length=50)
    father_house_number = models.CharField(max_length=50)
    father_national_id = models.CharField(max_length=50)
    father_status_choices = (
        ("Deceased", "Deceased"),
        ("Alive", "Alive"),
    )
    father_status = models.CharField(max_length=50, choices=father_status_choices)
    father_profession = models.CharField(max_length=50)
    
    mother_name = models.CharField(max_length=50)
    mother_phone_number = models.CharField(max_length=50)
    mother_address = models.TextField()
    mother_street_address = models.CharField(max_length=50)
    mother_house_number = models.CharField(max_length=50)
    mother_national_id = models.CharField(max_length=50)
    mother_status = models.CharField(max_length=50)
    mother_profession = models.CharField(max_length=50)
    
    guardian_name = models.CharField(max_length=50, blank=True, null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
        
    )
    guardian_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')    
    guardian_phone_number = models.CharField(max_length=50, blank=True, null=True)
    guardian_address = models.TextField()
    guardian_street_address = models.CharField(max_length=50, blank=True, null=True)
    guardian_house_number = models.CharField(max_length=50, blank=True, null=True)
    guardian_national_id = models.CharField(max_length=50, blank=True, null=True)
    guardian_status = models.CharField(max_length=50, blank=True, null=True)
    guardian_profession = models.CharField(max_length=50, blank=True, null=True)
    
    sponsor_name = models.CharField(max_length=50, blank=True, null=True)
    sponsor_phone_number = models.CharField(max_length=50, blank=True, null=True)
    sponsor_address = models.TextField()
    sponsor_street_address = models.CharField(max_length=50, blank=True, null=True)
    sponsor_house_number = models.CharField(max_length=50, blank=True, null=True)
    sponsor_national_id = models.CharField(max_length=50, blank=True, null=True)
    sponsor_status = models.CharField(max_length=50, blank=True, null=True)
    sponsor_profession = models.CharField(max_length=50, blank=True, null=True) 
    # Other fields...    
         
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fcm_token = models.TextField(default="")
    objects = models.Manager()
        
class Attendance(models.Model):
    id = models.AutoField(primary_key=True)  
    subject_id = models.ForeignKey(Subject,on_delete=models.DO_NOTHING)
    attendance_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)  
    objects = models.Manager()


class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)  
    student_id = models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance,on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)   
    objects = models.Manager()
    
class LeaveReportStudent(models.Model):
     id = models.AutoField(primary_key=True)     
     student_id = models.ForeignKey(Students,on_delete=models.DO_NOTHING)
     leave_date = models.DateTimeField(auto_now_add=True)
     leave_message = models.TextField()
     leave_status = models.IntegerField(default=0)    
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now_add=True)   
     objects = models.Manager()
     
     
class LeaveReportStaffs(models.Model):
     id = models.AutoField(primary_key=True)     
     staff_id = models.ForeignKey(Staffs,on_delete=models.DO_NOTHING)
     leave_date = models.DateTimeField(auto_now_add=True)
     leave_message = models.TextField()
     leave_status = models.IntegerField(default=0)    
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now_add=True)   
     objects = models.Manager()
     
     
class FeedBackStudent(models.Model):
     id = models.AutoField(primary_key=True)     
     student_id = models.ForeignKey(Students,on_delete=models.DO_NOTHING)
     feedback = models.CharField(max_length=255)     
     feedback_reply = models.TextField()    
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now_add=True)   
     objects = models.Manager()
     
     
class FeedBackStaff(models.Model):
     id = models.AutoField(primary_key=True)     
     staff_id = models.ForeignKey(Staffs,on_delete=models.DO_NOTHING)
     feedback = models.CharField(max_length=255)     
     feedback_reply = models.TextField()    
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now_add=True)   
     objects = models.Manager() 
     
class NotificationStudent(models.Model):
     id = models.AutoField(primary_key=True)     
     student_id = models.ForeignKey(Students,on_delete=models.DO_NOTHING)     
     message = models.TextField()       
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now_add=True)   
     objects = models.Manager()     
     
class NotificationStaff(models.Model):
     id = models.AutoField(primary_key=True)     
     staff_id = models.ForeignKey(Staffs,on_delete=models.DO_NOTHING)     
     message = models.TextField()       
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now_add=True)   
     objects = models.Manager()   
     
     
    
    
@receiver(post_save,sender=CustomUser)  
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type ==1:
            AdminHOD.objects.create(admin = instance)
        if instance.user_type ==2:
            Staffs.objects.create(admin = instance)
        if instance.user_type ==3:
            Students.objects.create(admin = instance,address="",profile_pic="",gender="")
 
@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type ==1:
        instance.adminhod.save()    
    if instance.user_type ==2:
        instance.staffs.save()    
    if instance.user_type ==3:
        instance.students.save()    
            


    
        
    