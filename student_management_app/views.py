from django.contrib.auth import logout,login
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from student_management_app.emailBackEnd import EmailBackend
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

def members(request):  
  return render(request,'myfirst.html')

def ShowLogin(request):  
  return render(request,'login.html')



def DoLogin(request):
  if request.method!="POST":
    return HttpResponse("<h2>Method Not allowed")
  
  else:
    user = EmailBackend.authenticate(request,request.POST.get("email"),request.POST.get("password"))
    if user!=None:    
      login(request,user)        
      return HttpResponseRedirect("/admin_home")
    else:
      messages.error(request,"Invalid Login Details")
      return HttpResponseRedirect("/")
    
    
def GetUserDetails(request):
  user = request.user
  if user.is_authenticated:
    return HttpResponse("User : "+user.email+" usertype : " + user.usertype)
  else:
    return HttpResponse("Please login first")   
  
  
def logout_user(request):
  logout(request)
  return HttpResponseRedirect("/")
    
  