from django.shortcuts import render,redirect
from django.http import HttpResponse
import mysql.connector
from . models import Candidate,Student,Contact,Admin,Election,Voting,Cand,Candidateresults,Emailid,Sem
import smtplib
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import cv2 as cv
import numpy as np
from pathlib import Path
from datetime import datetime
from django.utils import timezone
# Create your views here.

def index(request):
    #return HttpResponse("hi")
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)        
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        ) 
        mycursor =conn.cursor()
        #retrive post details       
        name=request.POST['name']
        rollno=request.POST['roll']  
        pwd=request.POST['pass']     
        branch=request.POST['pro']
        section=request.POST['sec']
        email=request.POST['email']
        contact=request.POST['mob']
        address=request.POST['addr'] 
        age=request.POST['age']
        semester=request.POST['sem']
        gender=request.POST['gen'] 
        status=0
        mycursor.execute("insert into voter(name,rollnumber,email,password,branch,section,semester,mobile,image,gender,age,address,status) values('"+name+"','"+str(rollno)+"','"+email+"','"+pwd+"','"+branch+"','"+section+"','"+semester+"','"+str(contact)+"','"+filename+"','"+gender+"','"+str(age)+"','"+address+"','"+str(status)+"')")
        conn.commit()
        return render(request,'getotp.html')
    else:
        return render(request,'index.html')

def getotp(request):
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="online_voting"
        )
        mycursor = conn.cursor()
        # retrive post details
        email = request.POST['email']
        #for otp in range(0,4):
        otp=str(random.randint(1000,9999))

        mycursor.execute("insert into verify(email,otp) values('"+email+"','"+otp+"')")
        conn.commit()
        #result = mycursor.fetchone()
        #pwd=str(result)
        #if (result != None):
            # SMTP server configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'pendyalaspandana530@gmail.com'
        # for App Password enable 2-step verification then u can create app password
        smtp_password = 'pnghffowfbdminym'

        # Email content
        subject = 'Email Verification'
        body = 'This is a Email verification mail sent from kits.'+'One time Password '+ otp
        sender_email = 'pendyalaspandana530@gmail.com'
        receiver_email = email

        # Create a message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            return render(request,'otp.html', {'status': 'Password sent to given mail ID'})
        
    else:
        return render(request, 'getotp.html')
    
def otp(request):
     if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="online_voting" 
        )
        mycursor = conn.cursor()
        # retrive post details
        email =request.POST['email']
        otp = request.POST['otp']
        mycursor.execute("select email from verify where otp='"+otp+"'")
        result=mycursor.fetchone()
        em=result[0]
        mail='pendyalaspandana530@gmail.com'
       
        if(result!=None):
            mycursor.execute("UPDATE voter SET status = 1 WHERE email ='"+em+"'")
            conn.commit()
            return render(request,'index.html')
            
        else:
            return render(request,'otp.html',{'status':'invalid otp'})


def login_admin(request):
    if request.method == 'POST':
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        
        )
        mycursor = conn.cursor()
        #retrive post details       
        
        email=request.POST['email']
        pwd=request.POST['pass']     
        
        mycursor.execute("select * from admin where email='"+email+"' and password='"+pwd+"'")
        result=mycursor.fetchone()
        if(result!=None):
            request.session['email'] = email
            return render (request,'admin_dashboard.html',{'email':email})
            #redirect('studenthome')
        else:
            messages.warning(request, 'Invalid credentials!')
            return render(request,'login_admin.html',{'status':'invalid credentials'})    
    else:
        return render(request,'login_admin.html')
def login_student(request):
    if request.method == 'POST':
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        
        )
        mycursor = conn.cursor()
        #retrive post details       
        
        email=request.POST['email']
        pwd=request.POST['pass']  
        mycursor.execute("select status from voter where email='"+email+"' and password='"+pwd+"'") 
        result=mycursor.fetchone()
        status=result[0]    
        if(status==1):
            mycursor.execute("select * from voter where email='"+email+"' and password='"+pwd+"'")
            result=mycursor.fetchone()

            if(result!=None):
                request.session['email'] = email
                return render(request, 'student_dashboard.html', {"email" : email})
                #redirect('studenthome')
            else:
                messages.warning(request, 'Invalid credentials!')
                return render(request,'login_student.html',{'status':'invalid credentials'}) 
        else:
            messages.warning(request, 'Your account has been not verified.')
            return render(request,'login_student.html',{'status':'login activity has been deactivated'})
           
    else:
        return render(request,'login_student.html')
def login_candidate(request):
    if request.method == 'POST':
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        
        )
        mycursor = conn.cursor()
        #retrive post details       
        
        email=request.POST['email']
        pwd=request.POST['pass']     
        mycursor.execute("select status from candidate where email='"+email+"' and password='"+pwd+"'") 
        result=mycursor.fetchone()
        status=result[0] 
        if(status==1):
            mycursor.execute("select * from candidate where email='"+email+"' and password='"+pwd+"'")
            result=mycursor.fetchone()

            if(result!=None):
                request.session['email'] = email
                return render(request, 'candidate_dashboard.html', {"email" : email})
            else:
                messages.warning(request, 'Invalid credentials!')
                return render(request,'login_candidate.html',{'status':'invalid credentials'}) 
        else:
            messages.warning(request, 'Your account has been deactivated.')
            return render(request,'login_candidate.html',{'status':'login activity has been deactivated'})

    else:
        return render(request,'login_candidate.html')
def contact(request):
    if request.method == 'POST':
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        
        )
        mycursor = conn.cursor()
        #retrive post details       
        
        fname=request.POST['fname']
        lname=request.POST['lname']  
        rollno=request.POST['rollno']
        email=request.POST['email1']     
        msg1=request.POST['msg']   
           
        mycursor.execute("insert into contact(firstname,lastname,rollnumber,email,message) values('"+fname+"','"+lname+"','"+rollno+"','"+email+"','"+msg1+"') ")
        conn.commit()
        messages.success(request, 'Admin will contact you soon!')
        return render(request,'contact.html')
    else:
        return render(request,'contact.html')
   
def forget_password_admin(request): 
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="online_voting"
        )
        mycursor = conn.cursor()
        # retrive post details
        email = request.POST['user_email']
        #for otp in range(0,4):
        otp=str(random.randint(1000,9999))

        mycursor.execute("insert into forget(email,otp) values('"+email+"','"+otp+"')")
        conn.commit()
        #result = mycursor.fetchone()
        #pwd=str(result)
        #if (result != None):
            # SMTP server configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'pendyalaspandana530@gmail.com'
# for App Password enable 2-step verification then u can create app password
        smtp_password = 'pnghffowfbdminym'

# Email content
        subject = 'Password recovery'
        body = 'This is a Password recovery email sent from kits.'+'One time Password '+ otp
        sender_email = 'pendyalaspandana530@gmail.com'
        receiver_email = email

# Create a message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            return render(request, 'change_password_admin.html', {'status': 'Password sent to given mail ID'})
        
    else:
        return render(request, 'forget_password_admin.html')
def forget_password_candidate(request): 
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="online_voting"
        )
        mycursor = conn.cursor()
        # retrive post details
        email = request.POST['user_email']
        #for otp in range(0,4):
        otp=str(random.randint(1000,9999))

        mycursor.execute("insert into forget(email,otp) values('"+email+"','"+otp+"')")
        conn.commit()
        #result = mycursor.fetchone()
        #pwd=str(result)
        #if (result != None):
            # SMTP server configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'pendyalaspandana530@gmail.com'
# for App Password enable 2-step verification then u can create app password
        smtp_password = 'pnghffowfbdminym'

# Email content
        subject = 'Password recovery'
        body = 'This is a Password recovery email sent from kits.'+'One time Password '+ otp
        sender_email = 'pendyalaspandana530@gmail.com'
        receiver_email = email

# Create a message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            return render(request,'change_password_candidate.html', {'status': 'Password sent to given mail ID'})
        
    else:
        return render(request, 'forget_password_candidate.html')
def forget_password_student(request): 
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="online_voting"
        )
        mycursor = conn.cursor()
        # retrive post details
        email = request.POST['user_email']
        #for otp in range(0,4):
        otp=str(random.randint(1000,9999))

        mycursor.execute("insert into forget(email,otp) values('"+email+"','"+otp+"')")
        conn.commit()
        #result = mycursor.fetchone()
        #pwd=str(result)
        #if (result != None):
            # SMTP server configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'pendyalaspandana530@gmail.com'
# for App Password enable 2-step verification then u can create app password
        smtp_password = 'pnghffowfbdminym'

# Email content
        subject = 'Password recovery'
        body = 'This is a Password recovery email sent from kits.'+'One time Password '+ otp
        sender_email = 'pendyalaspandana530@gmail.com'
        receiver_email = email

# Create a message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            return render(request, 'change_password_student.html', {'status': 'Password sent to given mail ID'})
        
    else:
        return render(request, 'forget_password_student.html')
def change_password_admin(request):
   # return HttpResponse("<h3>Welcome hnc</h3>")
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="online_voting" 
        )
        mycursor = conn.cursor()
        # retrive post details
        otp = request.POST['otpcode']
        npwd = request.POST['newpassword']
        mycursor.execute("select email from forget where otp='"+otp+"'")
        result=mycursor.fetchone()
        em=result[0]
        mail='pendyalaspandana530@gmail.com'
       
        if(result!=None):
            mycursor.execute("UPDATE admin SET password ='"+npwd+"' WHERE email ='"+em+"'")
            conn.commit()
            return render(request,'login_admin.html')
            
        else:
            return render(request,'change_password_admin.html',{'status':'invalid otp'})
def change_password_candidate(request):
   # return HttpResponse("<h3>Welcome hnc</h3>")
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="online_voting"
        )
        mycursor = conn.cursor()
        # retrive post details
        otp = request.POST['otpcode']
        npwd = request.POST['newpassword']
        mycursor.execute("select email from forget where otp='"+otp+"'")
        result=mycursor.fetchone()
        em=result[0]     
        mail='pendyalaspandana@gmail.com'
       
        if(result!=None):
            mycursor.execute("UPDATE candidate SET password ='"+npwd+"' WHERE email ='"+em+"'")
            conn.commit()
            return render(request,'login_candidate.html')    
        else:
            return render(request,'change_password_candidate.html',{'status':'invalid otp'})
def change_password_student(request):
   # return HttpResponse("<h3>Welcome hnc</h3>")
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="online_voting"
        )
        mycursor = conn.cursor()
        # retrive post details
        otp = request.POST['otpcode']
        npwd = request.POST['newpassword']
        mycursor.execute("select email from forget where otp='"+otp+"'")
        result=mycursor.fetchone()
        em=result[0]
        mail='pendyalaspandana9@gmail.com'
       
        if(result!=None):
            mycursor.execute("UPDATE voter SET password ='"+npwd+"' WHERE email ='"+em+"'")
            conn.commit()
            return render(request,'login_student.html')
            
        else:
            return render(request,'change_password_student.html',{'status':'invalid otp'})
def update_password_admin(request):
    if "email" in request.session:
        email=request.session['email']
    else:
        return render(request,"login_admin.html")
    if request.method == 'POST':        
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        ) 
        mycursor =conn.cursor()
        #retrive post details     
        old_pass=request.POST['current_password']
        new_pass=request.POST['new_password1']
        new_pass1=request.POST['new_password2']
        mycursor.execute("update admin SET password='"+new_pass+"' where email='"+email+"'")
        conn.commit()
        messages.success(request, 'Password updated')
        return render(request,'update_password_admin.html')
    else:
        return render(request,'update_password_admin.html')
def update_password_cand(request):
    if "email" in request.session:
        email=request.session['email']
    else:
        return render(request,"login_candidate.html")
    if request.method == 'POST':        
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        ) 
        mycursor =conn.cursor()
        #retrive post details     
        old_pass=request.POST['current_password']
        new_pass=request.POST['new_password1']
        new_pass1=request.POST['new_password2']
        mycursor.execute("update candidate SET password='"+new_pass+"' where email='"+email+"'")
        conn.commit()
        messages.success(request, 'Password updated')
        return render(request,'update_password_cand.html')
    else:
        return render(request,'update_password_cand.html') 
def update_password_stud(request):
    if "email" in request.session:
        email=request.session['email']
    else:
        return render(request,"login_student.html")
    if request.method == 'POST':        
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        ) 
        mycursor =conn.cursor()
        #retrive post details     
        old_pass=request.POST['current_password']
        new_pass=request.POST['new_password1']
        new_pass1=request.POST['new_password2']
        mycursor.execute("update voter SET password='"+new_pass+"' where email='"+email+"'")
        conn.commit()
        messages.success(request, 'Password updated')
        return render(request,'update_password_stud.html')
    else:
        return render(request,'update_password_stud.html')  
def add_candidate(request):
    #return HttpResponse("hi")
    if "email" in request.session:
        email=request.session['email']
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)       
            conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="online_voting"
            ) 
            mycursor =conn.cursor()
            #retrive post details       
            name=request.POST['name']
            rollno=request.POST['rollno']      
            branch=request.POST['pro']
            semester=request.POST['sem'] 
            section=request.POST['sec']
            position=request.POST['position']
            email=request.POST['email']
            pwd=request.POST['pass'] 
            contact=request.POST['mob']
            address=request.POST['addr'] 
            age=request.POST['age']
            gender=request.POST['gender']
            status=1
            mycursor.execute("insert into candidate(name,rollnumber,email,password,branch,section,position,semester,mobile,image,gender,age,address,status) values('"+name+"','"+str(rollno)+"','"+email+"','"+pwd+"','"+branch+"','"+section+"','"+position+"','"+semester+"','"+str(contact)+"','"+filename+"','"+gender+"','"+str(age)+"','"+address+"','"+str(status)+"')")
            conn.commit()
            messages.success(request, 'Candidate added')
            return render(request,'add_candidate.html')
        else:
            return render(request,'add_candidate.html')
    else:
        return render(request,'login_admin.html')
            
def edit_candidate(request,candidate_id):
    #return HttpResponse("hi")
    if "email" in request.session:
        email=request.session['email']
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)        
            conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="online_voting"
            ) 
            mycursor =conn.cursor()
            #retrive post details       
            name=request.POST['name']
            rollno=request.POST['rollno']      
            branch=request.POST['pro']
            semester=request.POST['sem'] 
            section=request.POST['sec']
            position=request.POST['position']
            email=request.POST['email']
            pwd=request.POST['pass'] 
            contact=request.POST['mob']
            address=request.POST['addr'] 
            age=request.POST['age']
            gender=request.POST['gender'] 
            status=1
            mycursor.execute("update candidate SET name='"+name+"',rollnumber='"+str(rollno)+"',email='"+email+"',password='"+pwd+"',branch='"+branch+"',semester='"+semester+"',section='"+section+"',position='"+position+"',mobile='"+str(contact)+"',image='"+filename+"',gender='"+gender+"',age='"+str(age)+"',address='"+address+"',status='"+str(status)+"' where candidate_id='"+str(candidate_id)+"'")
            conn.commit()
            #messages.success(request, 'Candidate details updated')
            return render(request,'show_candidate.html')
        else:
            conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="online_voting"
            )
            mycursor = conn.cursor()
            #retrive post details       
            mycursor.execute("select * from candidate where candidate_id='"+candidate_id+"'")
            result=mycursor.fetchall()
            candidates=[]  
            candidate=None
            for x in result:
                candidate = Candidate()
                candidate.candidate_id=x[0]
                candidate.name=x[1]  
                candidate.rollnumber=x[2]
                candidate.email=x[3]
                candidate.password=x[4]  
                candidate.branch=x[5]
                candidate.semester=x[6]
                candidate.section=x[7]
                candidate.position=x[8]  
                candidate.image=x[9]
                candidate.mobile=x[10]
                candidate.gender=x[11]  
                candidate.age=x[12]
                candidate.address=x[13]  
                candidate.status=x[14]
                candidates.append(candidate)
            return render(request,'edit_candidate.html',{'candidate':candidate})
    else:
        return render(request,'login_admin.html')
        
def edit_student(request,studentid):
    #return HttpResponse("hi")
    if "email" in request.session:
        email=request.session['email']
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)        
            conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="online_voting"
            ) 
            mycursor =conn.cursor()
            #retrive post details       
            name=request.POST['name']
            rollno=request.POST['rollno']      
            branch=request.POST['pro']
            semester=request.POST['sem'] 
            section=request.POST['sec']
            email=request.POST['email']
            pwd=request.POST['pass'] 
            contact=request.POST['mob']
            address=request.POST['addr'] 
            age=request.POST['age']
            gender=request.POST['gender'] 
            status=1
            mycursor.execute("update voter SET name='"+name+"',rollnumber='"+str(rollno)+"',email='"+email+"',password='"+pwd+"',branch='"+branch+"',semester='"+semester+"',section='"+section+"',image='"+filename+"',mobile='"+contact+"',gender='"+gender+"',age='"+age+"',address='"+address+"',status='"+str(status)+"' where studentid='"+str(studentid)+"'")
            conn.commit()
            #messages.success(request, 'Student details updated')
            return render(request,'display_student.html')
        else:
            conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="online_voting"
            )
            mycursor = conn.cursor()
            #retrive post details       
            mycursor.execute("select * from voter where studentid='"+studentid+"'")
            result=mycursor.fetchall()
            students=[]  
            student=None 
            for x in result:
                student=Student()
                student.name=x[1]  
                student.studentid=x[0]
                student.rollnumber=x[2]
                student.branch=x[3]
                student.email=x[4]
                student.password=x[5]  
                student.semester=x[6]
                student.section=x[7] 
                student.image=x[8]
                student.mobile=x[9]
                student.gender=x[10]  
                student.age=x[11]
                student.address=x[12]  
                student.status=x[13]
                students.append(student)
            return render(request,'edit_student.html',{'student':student})
    else:
        return render(request,'login_admin.html')
def edit_election(request,electionid):
    #return HttpResponse("hi")
    if "email" in request.session:
        email=request.session['email']
    else:
        return render(request,'login_admin.html')
    if request.method == 'POST':       
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
            ) 
        mycursor =conn.cursor()
        #retrive post details       
        electionname=request.POST['electionname']
        starttime=request.POST['starttime']      
        endtime=request.POST['endtime']
        voters=request.POST['selectedsemester'] 
        date=request.POST['date']
        mycursor.execute("update election SET electionname='"+electionname+"',starttime='"+str(starttime)+"',endtime='"+str(endtime)+"',voters='"+str(voters)+"',date='"+str(date)+"' where electionid='"+str(electionid)+"'")
        conn.commit()
        #messages.success(request, 'Election details updated')
        return redirect('manage_election')
    else:
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
        mycursor = conn.cursor()
        #retrive post details       
        mycursor.execute("select * from election where electionid='"+electionid+"'")
        result=mycursor.fetchall()
        print(result)
        elections=[]  
        for x in result:
            election = Election()
            election.electionid=x[0]
            election.electionname=x[1]
            election.starttime=x[2]
            election.endtime=x[3]
            election.voters=x[4]  
            election.date=x[5]
            election.status=x[6]
            elections.append(election)
        return render(request,'edit_election.html',{'election':election})
   
def display_contact(request):
    if "email" in request.session:
        email=request.session['email']
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
        mycursor = conn.cursor()
        #retrive post details       
        mycursor.execute("select * from contact")
        result=mycursor.fetchall()
        contacts=[]  
        for x in result:
            contact = Contact()
            contact.id=x[0]
            contact.firstname=x[1]  
            contact.lastname=x[2]
            contact.rollnumber=x[3]
            contact.email=x[4]
            contact.message=x[5]  
            contacts.append(contact)
        return render(request,'display_contact.html',{'student_list':contacts}) 
    else:
        return render(request,'login_admin.html')
def show_candidate(request):
    if "email" in request.session:
        email=request.session['email']
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
        mycursor = conn.cursor()
        #retrive post details       
        mycursor.execute("select * from candidate")
        result=mycursor.fetchall()
        candidates=[]  
        for x in result:
            candidate = Candidate()
            candidate.candidate_id=x[0]
            candidate.name=x[1]
            candidate.rollnumber=x[2]
            candidate.email=x[3]
            candidate.password=x[4]  
            candidate.branch=x[5]
            candidate.semester=x[6]
            candidate.section=x[7]
            candidate.position=x[8]  
            candidate.image=x[9]
            candidate.mobile=x[10]
            candidate.gender=x[11]  
            candidate.age=x[12]
            candidate.address=x[13]  
            candidate.status=x[14]
            candidates.append(candidate)
        return render(request,'show_candidate.html',{'student_list':candidates})
    else:
        return render(request,'login_admin.html')
def display_student(request):
    if "email" in request.session:
        email=request.session['email']
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        
        )
        mycursor = conn.cursor()
        #retrive post details       
        mycursor.execute("select * from voter")
        result=mycursor.fetchall()
        students=[]  
        for x in result:
            student=Student()
            student.studentid=x[0]
            student.name=x[1]  
            student.rollnumber=x[2]
            student.branch=x[3]
            student.email=x[4]
            student.password=x[5]  
            student.semester=x[6]
            student.section=x[7] 
            student.image=x[8]
            student.mobile=x[9]
            student.gender=x[10]  
            student.age=x[11]
            student.address=x[12]  
            student.status=x[13]
            students.append(student)
        return render(request,'display_student.html',{'student_list':students})
    else:
        return render(request,'login_admin.html')
    
def update_profile_admin(request):
    email=''
    if "email" in request.session:
        email=request.session['email']
    else:
        return render(request,'login_admin.html')
    if request.method == 'POST': 
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
        mycursor = conn.cursor()
        #retrive post details       
        name=request.POST['name']
        email=request.POST['email']
        pwd=request.POST['pass'] 
        mycursor.execute("update admin SET name='"+name+"',password='"+pwd+"'where email='"+email+"'")
        conn.commit()
        messages.success(request, 'Profile updated')
        return redirect('update_profile_admin')
    else:
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
        mycursor = conn.cursor()
        #retrive post details       
        mycursor.execute("select * from admin where email='"+email+"'")
        result=mycursor.fetchall()
        admins=[]  
        for x in result:
            admin = Admin()
            admin.admin_id=x[0]
            admin.name=x[1]
            admin.email=x[2]
            admin.password=x[3]  
            admins.append(admin)
        return render(request,'update_profile_admin.html',{'student_list':admins})
def update_profile_cand(request):
    email=''
    if "email" in request.session:
        email=request.session['email']
    else:
        return render(request,'login_candidate.html')
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename) 
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
        mycursor = conn.cursor()
        #retrive post details       
        name=request.POST['name']
        rollno=request.POST['rollno']      
        branch=request.POST['pro']
        semester=request.POST['sem'] 
        section=request.POST['sec']
        email=request.POST['email']
        pwd=request.POST['pass'] 
        contact=request.POST['mob']
        address=request.POST['addr'] 
        position=request.POST['position']
        age=request.POST['age']
        gender=request.POST['gender'] 
        status=1
        mycursor.execute("update candidate SET name='"+name+"',rollnumber='"+str(rollno)+"',email='"+email+"',password='"+pwd+"',branch='"+branch+"',semester='"+semester+"',section='"+section+"',position='"+position+"',mobile='"+str(contact)+"',image='"+filename+"',gender='"+gender+"',age='"+str(age)+"',address='"+str(address)+"',status='"+str(status)+"' where email='"+email+"'")
        conn.commit()
        messages.success(request, 'Profile updated')
        return redirect('update_profile_cand')
    else:
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
        mycursor = conn.cursor()
        #retrive post details       
        mycursor.execute("select * from candidate where email='"+email+"'")
        result=mycursor.fetchall()
        candidates=[]  
        for x in result:
            candidate = Candidate()
            candidate.candidate_id=x[0]
            candidate.name=x[1]
            candidate.rollnumber=x[2]
            candidate.email=x[3]
            candidate.password=x[4]  
            candidate.branch=x[5]
            candidate.semester=x[6]
            candidate.section=x[7]
            candidate.position=x[8]  
            candidate.image=x[9]
            candidate.mobile=x[10]
            candidate.gender=x[11]  
            candidate.age=x[12]
            candidate.address=x[13]  
            candidate.status=x[14]
            candidates.append(candidate)
        return render(request,'update_profile_cand.html',{'student_list':candidates})       
def update_profile_stud(request):
    email=''
    if "email" in request.session:
        email=request.session['email']  
    else:
        return render(request,'login_student.html')
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
        mycursor = conn.cursor()
        #retrive post details       
        name=request.POST['name']
        rollno=request.POST['rollno']      
        branch=request.POST['pro']
        semester=request.POST['sem'] 
        section=request.POST['sec']
        email=request.POST['email']
        pwd=request.POST['pass'] 
        contact=request.POST['mob']
        address=request.POST['addr'] 
        age=request.POST['age']
        gender=request.POST['gender'] 
        status=1
        mycursor.execute("update voter SET name='"+name+"',rollnumber='"+str(rollno)+"',email='"+email+"',password='"+pwd+"',branch='"+branch+"',semester='"+semester+"',section='"+section+"',mobile='"+str(contact)+"',image='"+filename+"',gender='"+gender+"',age='"+str(age)+"',address='"+address+"',status='"+str(status)+"' where email='"+email+"'")
        conn.commit()
        messages.success(request, 'Profile updated')
        return redirect('update_profile_stud')
    else:
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
        mycursor = conn.cursor()
        #retrive post details       
        mycursor.execute("select * from voter where email='"+email+"'")
        result=mycursor.fetchall()
        students=[]  
        for x in result:
            student=Student()
            student.studentid=x[0]
            student.name=x[1]  
            student.rollnumber=x[2]
            student.branch=x[3]
            student.email=x[4]
            student.password=x[5]  
            student.semester=x[6]
            student.section=x[7] 
            student.image=x[8]
            student.mobile=x[9]
            student.gender=x[10]  
            student.age=x[11]
            student.address=x[12]  
            student.status=x[13]
            students.append(student)
        return render(request,'update_profile_stud.html',{'student_list':students}) 
def logout_admin(request):
    if "email" in request.session:
        email=request.session['email']      
        del request.session['email']
        request.session.modified = True
        return render(request,'login_admin.html') 
    else:
        return render(request,'login_admin.html')
 
def logout_candidate(request):
    del request.session['email']
    request.session.modified = True
    return render(request,'login_candidate.html') 
    
def logout_student(request):
    del request.session['email']
    request.session.modified = True
    return render(request,'login_student.html')

def delete_student(request,studentid):
    if "email" in request.session:
        email=request.session['email']
    #return HttpResponse("hi")
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="online_voting"
            ) 
        mycursor =conn.cursor()      
        mycursor.execute("delete from voter where studentid='"+studentid+"'")
        conn.commit()
        return redirect('display_student')
    else:
        return render(request,'login_admin.html')
def delete_candidate(request,candidate_id):
    if "email" in request.session:
        email=request.session['email']  
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="online_voting"
            ) 
        mycursor =conn.cursor()      
        mycursor.execute("delete from candidate where candidate_id='"+candidate_id+"'")
        conn.commit()
        return redirect('show_candidate')
    else:
        return render(request,'login_admin.html')
def delete_election(request,electionid):
    if "email" in request.session:
        email=request.session['email']
    #return HttpResponse("hi")
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="online_voting"
            ) 
        mycursor =conn.cursor()      
        mycursor.execute("delete from election where electionid='"+electionid+"'")
        conn.commit()
        return redirect('manage_election')
    else:
        return render(request,'login_admin.html')
def admin_dashboard(request):
    if "email" in request.session:
        email=request.session['email']
        return render(request,'admin_dashboard.html',{'email':email})
    else:
        return render(request,'login_admin.html') 
def candidate_dashboard(request):
    if "email" in request.session:
        email=request.session['email']
        return render(request,'candidate_dashboard.html',{'email':email})
    else:
        return render(request,'login_candidate.html') 
def student_dashboard(request):
    if "email" in request.session:
        email=request.session['email']
        return render(request,'student_dashboard.html',{'email':email})
    else:
        return render(request,'login_student.html') 
    
def error1(request):
    return render(request,'error1.html') 

def error(request):
    return render(request,'error.html') 

def error2(request):
    return render(request,'error2.html')

def error3(request):
    return render(request,'error3.html')

def completed(request):
    return render(request,'completed.html')
    
def election(request):
    email=''
    if "email" in request.session:
        email=request.session['email']
    else:
        return render(request,'login_admin.html')
    if request.method == 'POST': 
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
        mycursor = conn.cursor()
        #retrive post details       
        name=request.POST['electionname']
        starttime=request.POST['starttime']
        endtime=request.POST['endtime'] 
        date=request.POST['date']
        voters=request.POST['selectedsemester']
        mycursor.execute("insert into election(electionname,starttime,endtime,voters,date) values('"+name+"','"+starttime+"','"+endtime+"','"+voters+"','"+date+"')")
        conn.commit()
        return redirect('election')
    else:
        return render(request,'election.html')

def mse(img1, img2):
   h, w = img1.shape
   diff = cv.subtract(img1, img2)
   err = np.sum(diff**2)
   mse = err/(float(h*w))
#    print(diff)
#    print(err)
#    print(mse)
   return mse, diff

def vote(request):
    email=''
    if "email" in request.session:
        email=request.session['email']
    else:
        return render(request,'login_student.html')
    #validate duration for vote
    
    if request.method == 'POST':
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
        mycursor = conn.cursor()
        mycursor.execute("select electionid from election where status=1")
        result=mycursor.fetchone()
        electionid=result[0]
        # print(electionid)
        mycursor.execute("select studentid from voter where email='"+email+"'")
        result=mycursor.fetchone()
        studentid=result[0] 
        # print(studentid)
            
        president=request.POST['president']
        vicepresident=request.POST['vicepresident']
        secretary=request.POST['secretary']
        treasurer=request.POST['treasurer']
        mycursor.execute("insert into voting(electionid,studentid,president,vicepresident,secretary,treasurer) values('"+str(electionid)+"','"+str(studentid)+"','"+president+"','"+vicepresident+"','"+secretary+"','"+treasurer+"')")
        conn.commit()
        return redirect('completed')
    else:
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
        mycursor = conn.cursor()
        mycursor.execute("select electionid from election where status=1")
        result=mycursor.fetchone()
        electionid=result[0]
        # print(electionid)
        mycursor.execute("select studentid from voter where email='"+email+"'")
        result=mycursor.fetchone()
        studentid=result[0] 
        # print(studentid)
        mycursor.execute("select id from voting where studentid='"+str(studentid)+"' and electionid='"+str(electionid)+"'")
        result=mycursor.fetchone()
        if(result!=None):
            return redirect('error3')
        else:
            conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="online_voting"
            )
            mycursor = conn.cursor()
            mycursor.execute("select starttime,endtime,date from election where status=1")
            result=mycursor.fetchone()
            starttime=str(result[0])
            endtime=str(result[1])
            date=str(result[2])
            t1 = datetime.strptime(starttime, "%H:%M:%S")
            t2 = datetime.strptime(endtime, "%H:%M:%S")
            current = timezone.localdate()
            current_date=str(current)


            # print(date)
            # print(current_date)
            # get difference
            # delta = t2 - t1
            # timelimit=delta.total_seconds()
            # print(timelimit)
            initial=t1.time()
            end=t2.time()
            t3 = datetime.now()
            current_dateTime = t3.time()
            if(not (current_dateTime > initial and current_dateTime < end ) or current_date != date):
                return render(request,'error2.html')

            cam = cv.VideoCapture(0)   
            s, img = cam.read()
            if s:
                cv.namedWindow("cam-test")
                cv.imshow("cam-test",img)     
                cv.waitKey(0)
                cv.destroyWindow("cam-test")
               
                cv.imwrite("images\\filename.jpg",img)
            
            path=Path(__file__).resolve().parent.parent
            path=str(path)+'\\images\\filename.jpg'
            # print(path)
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="online_voting"
                )
            mycursor = conn.cursor()
            mycursor.execute("select image,semester from voter where email='"+email+"'")
            result=mycursor.fetchone()
            orr=result[0]
            #print(orr)
            imgOriginal = cv.imread(path)
            #print(imgOriginal)
            path=Path(__file__).resolve().parent.parent
            path=str(path)+'\\media\\'+orr
            imgLatest = cv.imread(path)
            #print(imgLatest)

            # print('difference      ',imgOriginal-imgLatest)

            # if  imgOriginal.shape != imgLatest.shape:
            #     imgLatest = cv.resize(imgLatest, imgOriginal.shape[:2][::-1])
                #print("shapes converted")

            # convert the images to grayscale
            img1 = cv.cvtColor(imgOriginal, cv.COLOR_BGR2GRAY)
            img2 = cv.cvtColor(imgLatest, cv.COLOR_BGR2GRAY)

            error, diff = mse(img1, img2)
            print("error is ",error)
            #print("error is ",error)
            #print("diff is ",diff)
            if(error>15):
                #print(error)
                return render(request,'error1.html')
            
            conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="online_voting"
            )
            mycursor = conn.cursor()
            
            sem=result[1]
            #print(sem)
            mycursor.execute("SELECT electionid FROM election WHERE voters LIKE '%"+sem+"%' AND status=1")
            result = mycursor.fetchone()
            if result:
                sem = result[0]
                #print("sem    : ",sem)
            else:
                print("No records found")
            # print("result is")
            # print(str(result))
            #select * from election where voters like '%sem%'
            if(result==None):
                return render(request,'error.html')
            else:
                conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="online_voting"
                )
                mycursor = conn.cursor()
            #retriving semesters
                mycursor.execute("select voters from election where status=1")
                result=mycursor.fetchone()
                semester=result[0]
                s=semester.split(',')
                sems=[]
                for x in s:
                    n=Sem()
                    n.semester=x
                    sems.append(n)
                #retriving president candidates
                mycursor.execute("select name from candidate where position='President'")
                result=mycursor.fetchall()
                #print(result)
                cands=[]
                for x in result:
                    n=Cand()
                    n.cand_president=x[0]
                    cands.append(n)

                #retriving vice-president candidates
                mycursor.execute("select name from candidate where position='Vice-President'")
                result=mycursor.fetchall()
                #print(result)
                cands1=[]
                for x in result:
                    n=Cand()
                    n.cand_vicepresident=x[0]
                    cands1.append(n)
    
                #retriving Secretarycandidates
                mycursor.execute("select name from candidate where position='Secretary'")
                result=mycursor.fetchall()
                #print(result)
                cands2=[]
                for x in result:
                    n=Cand()
                    n.cand_secretary=x[0]
                    cands2.append(n)
                
            #retriving  treasurer candidates
                mycursor.execute("select name from candidate where position='Treasurer'")
                result=mycursor.fetchall()
                #print(result)
                cands3=[]
                for x in result:
                    n=Cand()
                    n.cand_treasurer=x[0]
                    cands3.append(n)
        return render(request,'vote.html',{'sem':sems,'cand':cands,'cand1':cands1,'cand2':cands2,'cand3':cands3})
  
            
def manage_election(request):
    if "email" in request.session:
        email=request.session['email']
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
        mycursor = conn.cursor()
        #retrive post details       
        mycursor.execute("select * from election")
        result=mycursor.fetchall()
        elections=[]  
        for x in result:
            election = Election()
            election.electionid=x[0]
            election.electionname=x[1]
            election.starttime=x[2]
            election.endtime=x[3]
            election.voters=x[4]  
            election.date=x[5]
            election.status=x[6]
            elections.append(election)
        return render(request,'manage_election.html',{'student_list':elections})
    else:
        return render(request,'login_admin.html')

def changetoinvalid(request,candidate_id):
     conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
     mycursor = conn.cursor()
    #retrive post details       
     mycursor.execute("update candidate set status=0 where candidate_id='"+candidate_id+"'")
     conn.commit()
     return redirect('show_candidate')

def changetovalid(request,candidate_id):
     
     conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
     mycursor = conn.cursor()
    #retrive post details       
     mycursor.execute("update candidate set status=1 where candidate_id='"+candidate_id+"'")
     conn.commit()
     return redirect('show_candidate')
def changetovalidelection(request,electionid):
     
     conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
     mycursor = conn.cursor()
    #retrive post details       
     mycursor.execute("update election set status=1 where electionid='"+electionid+"'")
     conn.commit()
     sendmail()
     return redirect('manage_election')
def changetoinvalidelection(request,electionid):
     conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
     mycursor = conn.cursor()
    #retrive post details       
     mycursor.execute("update election set status=0 where electionid='"+electionid+"'")
     conn.commit()
     return redirect('manage_election')
def candidate_list(request):
    if "email" in request.session:
        email=request.session['email']
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
        mycursor = conn.cursor()
        #retrive post details       
        mycursor.execute("select * from candidate")
        result=mycursor.fetchall()
        candidates=[]  
        for x in result:
            candidate = Candidate()
            candidate.candidate_id=x[0]
            candidate.name=x[1]
            candidate.rollnumber=x[2]
            candidate.email=x[3]
            candidate.password=x[4]  
            candidate.branch=x[5]
            candidate.semester=x[6]
            candidate.section=x[7]
            candidate.position=x[8]  
            candidate.image=x[9]
            candidate.mobile=x[10]
            candidate.gender=x[11]  
            candidate.age=x[12]
            candidate.address=x[13]  
            candidate.status=x[14]
            candidates.append(candidate)
        return render(request,'candidate_list.html',{'student_list':candidates})
    else:
        return render(request,'login_admin.html')
def votings(request):
    if "email" in request.session:
        email=request.session['email']
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
        mycursor = conn.cursor()
        #retrive post details       
        mycursor.execute("select * from voting")
        result=mycursor.fetchall()
        votings=[]  
        for x in result:
            voting = Voting()
            voting.id=x[0]
            voting.electionid=x[1]
            voting.studentid=x[2]
            voting.president=x[3]
            voting.vicepresident=x[4] 
            voting.secretary=x[5] 
            voting.treasurer=x[6] 
            votings.append(voting)
        return render(request,'votings.html',{'student_list':votings}) 
    else:
        return render(request,'login_admin.html')

def sendmail():
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
        )
        mycursor = conn.cursor()
        #retrive post details       
        mycursor.execute("select voters,starttime,endtime,date from election where status=1")
        result=mycursor.fetchone()
        semester=str(result[0])
        starttime=result[1]
        endtime=result[2]
        date=result[3]
        s=semester.split(',')
        emails=[]
        for x in s:
            mycursor.execute("select email from voter where semester='"+x+"'")
            result=mycursor.fetchall()
            for x in result:
                n=Emailid()
                n.mail=x[0]
                emails.append(n)
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'pendyalaspandana530@gmail.com'
        # for App Password enable 2-step verification then u can create app password
        smtp_password = 'pnghffowfbdminym'
        print(emails)
        for email_obj in emails:
            email = email_obj.mail
            # Email content
            subject = 'Elections'
            body = 'This is a notification for the election timings mail sent from kits.'+' from '+ str(starttime) +' to ' + str(endtime) +' on ' + str(date)
            sender_email = 'pendyalaspandana530@gmail.com'
            receiver_email = email

            # Create a message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            "msg['To'] = receiver_email"
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            text=msg.as_string()
        # Connect to SMTP server and send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, receiver_email, text)
                # return render(request,'otp.html', {'status': 'Password sent to given mail ID'})
def results(request):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="online_voting"
    )
    mycursor = conn.cursor()
    mycursor.execute("select starttime,endtime,date from election where status=1")
    result=mycursor.fetchone()
    starttime=str(result[0])
    endtime=str(result[1])
    date=str(result[2])
    t1 = datetime.strptime(starttime, "%H:%M:%S")
    t2 = datetime.strptime(endtime, "%H:%M:%S")
    current = timezone.localdate()
    current_date=str(current)
    initial=t1.time()
    end=t2.time()
    t3 = datetime.now()
    current_dateTime = t3.time()
    print(date)
    print(current_dateTime)
    print(initial)
    print(end)
    if( (current_dateTime > initial and current_dateTime < end ) or current_date != date):
        return render(request,'error4.html')
    # president
    mycursor = conn.cursor()
    mycursor.execute("SELECT president,count(president) FROM `voting` group by president")
    result=mycursor.fetchall()
    fields = [col[0] for col in mycursor.description]
    result_list = [dict(zip(fields, row)) for row in result]
    result_dict = {row['president']: row['count(president)'] for row in result_list}
    res=[]
    max_value = max(result_dict.values())
    max_president = max(result_dict, key=result_dict.get)
    x=Candidateresults()
    x.candidatename=max_president
    x.candidaterole='President'
    x.noofvotes=max_value
    res.append(x)
    #vicepresident
    mycursor = conn.cursor()
    mycursor.execute("SELECT vicepresident,count(vicepresident) FROM `voting` group by vicepresident")
    result=mycursor.fetchall()
    fields = [col[0] for col in mycursor.description]
    result_list = [dict(zip(fields, row)) for row in result]
    result_dict = {row['vicepresident']: row['count(vicepresident)'] for row in result_list}
    max_value = max(result_dict.values())
    max_vicepresident = max(result_dict, key=result_dict.get)
    x=Candidateresults()
    x.candidatename=max_vicepresident
    x.candidaterole='Vice-President'
    x.noofvotes=max_value
    res.append(x)
    #secreatry
    mycursor = conn.cursor()
    mycursor.execute("SELECT secretary,count(secretary) FROM `voting` group by secretary")
    result=mycursor.fetchall()
    fields = [col[0] for col in mycursor.description]
    result_list = [dict(zip(fields, row)) for row in result]
    result_dict = {row['secretary']: row['count(secretary)'] for row in result_list}
    max_value = max(result_dict.values())
    max_secretary = max(result_dict, key=result_dict.get)
    x=Candidateresults()
    x.candidatename=max_secretary
    x.candidaterole='Secretary'
    x.noofvotes=max_value
    res.append(x)
    #treasurer
    mycursor = conn.cursor()
    mycursor.execute("SELECT treasurer,count(treasurer) FROM `voting` group by treasurer")
    result=mycursor.fetchall()
    fields = [col[0] for col in mycursor.description]
    result_list = [dict(zip(fields, row)) for row in result]
    result_dict = {row['treasurer']: row['count(treasurer)'] for row in result_list}
    max_value = max(result_dict.values())
    max_treasurer = max(result_dict, key=result_dict.get)
    x=Candidateresults()
    x.candidatename=max_treasurer
    x.candidaterole='Treasurer'
    x.noofvotes=max_value
    res.append(x)
    return render(request,"results.html",{'student_list':res})
    


