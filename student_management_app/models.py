from django.db import models
from django.utils.crypto import get_random_string
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
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)  
    surname = models.CharField(max_length=100)    
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10)    
    phone_number = models.CharField(max_length=20)
    school_segment = models.CharField(max_length=100)
    current_class = models.CharField(max_length=100)
    birth_certificate_id = models.CharField(max_length=100)
    allergies = models.TextField(blank=True, null=True)
    current_year = models.IntegerField(blank=True, null=True)
    is_finished = models.BooleanField(default=False)
    address = models.CharField(max_length=200)
    street_address = models.CharField(max_length=200)
    house_number = models.CharField(max_length=20)
    health_status = models.CharField(max_length=200)
    physical_disability = models.CharField(max_length=200)
    profile_pic = models.FileField(null=True, blank=True)
    birth_certificate_photo = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    objects = models.Manager()



    def __str__(self):
        return self.first_name + " " + self.last_name
    
    
    
class Parent(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    TYPE_CHOICES = [
        ('parent', 'Parent'),
        ('guardian', 'Guardian'),
        ('sponsor', 'Sponsor'),
    ]
    
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    occupation = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    national_id = models.CharField(max_length=20)
    status = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    parent_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    student = models.OneToOneField(Students, on_delete=models.CASCADE, related_name='parent')
    fcm_token = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)       
    objects = models.Manager()    
    def __str__(self):
        return self.name   
    
    
    
         
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
            


    
        
    