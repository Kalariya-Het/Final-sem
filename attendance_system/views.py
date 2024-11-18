from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.views.generic import ListView,CreateView,UpdateView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.decorators import login_required
from .models import Person, City,Attendance,TrainingData,Holidays
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password,check_password
from weasyprint import HTML,CSS
from django.template.loader import render_to_string
from .forms import FacultyRegisteration,FacultyEdit,FacultyEditEmail
from .filters import AttendenceFilter
from datetime import date,datetime
import random
import string
import pickle
import base64
from playsound import playsound
from django.conf import settings 
from django.core.mail import send_mail ,EmailMessage
from ipware import get_client_ip
import smtplib
import re
import cv2
import os
import csv
import math
from PIL import Image
from threading import Thread
import numpy as np
import pandas as pd
import time,datetime
import face_recognition
from collections import defaultdict
import openpyxl
import xlsxwriter
import collections
from django.db.models import Sum
import cv2
import time
from django.shortcuts import render
# Create your views here.

dates_lis=[]
ids_lis=[]

#This function is used to display home page
def home(request):
    ip, is_routable = get_client_ip(request)
    print("ip of client is : ",ip)

    return render(request,'main.html')

#This function is used to display admin login page
def admin_page(request,id=None):
    msg=None
    username=str(request.session['fetch_username'])
    form=FacultyRegisteration()
    details=Person.objects.all()

    return render(request,'admin_login.html',{'form':form, 'id':0, 'details':details,'username':username})

#This function is used to display admin menu page
def admin_home(request):
    username=request.session['fetch_username']
    return render(request,'admin_menu.html',{'username':username})

#This function is used to verify admin credentials
def admin_login(request,id=None):
    msg=None
    if request.method=='POST':
        user=authenticate(request,username=request.POST.get('username'),password=request.POST.get('password'))
        if user != None:
            request.session['fetch_username']=request.POST.get('username')
            return render(request,'admin_menu.html',{'username':request.POST.get('username')})
        else:
            msg='Username or Password is Invalid'
        
    
    return render(request,'main.html',{'msg':msg})

#This function is used to edit details of faculty in Admin module
def faculty_edit(request,id):
    username=request.session['fetch_username']
    details=Person.objects.all()
    form=Person.objects.get(pk=id)
    form=FacultyEditEmail(instance=form)
    return render(request,'admin_login.html',{'form':form, 'id':id, 'details':details,'username':username})


#This function is used to add details of faculty in Admin module
def faculty_add(request, id):
    msg = ''
    er_msg = ''
    details = {}  # Initialize details if not already defined
    username = request.user.username if request.user.is_authenticated else None

    regex_1 = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}\w+[.]\w{2,3}$'
    regex_2 = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    
    # Default password
    default_password = 'demo@123'

    if request.method == 'POST':
        faculty_page_var = request.POST.get('faculty_page', '')
        print("value of faculty_page_var is:", faculty_page_var)

        # Determine if it's a new entry or an edit
        if id == 0:  # New faculty entry
            form = FacultyRegisteration(request.POST)
        else:  # Existing faculty data is being edited
            form = FacultyEditEmail(request.POST)

        if form.is_valid():  # Check if the form is valid
            inst = form.cleaned_data['inst']
            dept = form.cleaned_data['dept']
            reg_id = form.cleaned_data['reg_id']
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            email = form.cleaned_data['email']

            # Validate institution, department, and registration ID
            if inst is None or dept is None or reg_id is None:
                er_msg = "Institution, Department, or Registration ID cannot be None."
                return render(request, 'admin_login.html', {'form': form, 'er_msg': er_msg, 'id': id, 'details': details, 'username': username})

            # Check for unique registration ID for new entries
            if Person.objects.filter(reg_id=reg_id).exists() and id == 0:
                er_msg = "This Register ID is already in use."
                return render(request, 'admin_login.html', {'form': form, 'er_msg': er_msg, 'id': id, 'details': details, 'username': username})

            # Validate email format
            if not (re.search(regex_1, email) or re.search(regex_2, email)):
                er_msg = "Email != written in a proper manner."
                return render(request, 'admin_login.html', {'form': form, 'er_msg': er_msg, 'id': id, 'details': details, 'username': username})

            # Check for unique email for new entries
            if Person.objects.filter(email=email).exists() and id == 0:
                er_msg = "This Email is already in use."
                return render(request, 'admin_login.html', {'form': form, 'er_msg': er_msg, 'id': id, 'details': details, 'username': username})

            # Handling faculty edits
            if id != 0 and faculty_page_var != '1':  # Edit faculty details inside Admin module
                pk_ = request.POST.get('id')
                pi = Person.objects.get(pk=pk_)
                original_email = pi.email

                if original_email != email:  # If the email is changed
                    if Person.objects.filter(email=email).exists():  # Updated email != unique
                        er_msg = "This Email is already in use."
                        return render(request, 'admin_login.html', {'form': form, 'er_msg': er_msg, 'id': id, 'details': details, 'username': username})

                    # Assign the default password
                    result_str = default_password

                    password = make_password(result_str, "a")
                    pi.delete()  # Delete the old entry if necessary

                else:
                    password = pi.password  # Keep the old password if unchanged

            else:  # If new entry or email hasn't changed
                # Assign the default password
                result_str = default_password
                password = make_password(result_str, "a")

            # Save or update the faculty information
            if faculty_page_var != '1':
                if id == 0:  # To store new entry of faculty
                    reg = Person(fname=fname, lname=lname, email=email, password=password, inst=inst, dept=dept, reg_id=reg_id)
                    reg.save()
                    msg = 'Details of Faculty Saved Successfully'
                else:  # To store edited entry of faculty
                    reg = Person.objects.get(pk=id)
                    reg.fname = fname
                    reg.lname = lname
                    reg.email = email
                    reg.password = password
                    reg.inst = inst
                    reg.dept = dept
                    reg.reg_id = reg_id
                    reg.save()
                    msg = 'Details of Faculty Updated Successfully'

            if faculty_page_var == '1':  # To edit data in faculty via Faculty module
                pk_ = str(int(request.POST['id']))
                attend = Attendance.objects.filter(reg_id=reg_id, inst=inst, dept=dept)
                fet_obj = Person.objects.get(pk=pk_)
                fet_obj.is_pass_change = False
                fet_obj.fname = fname
                fet_obj.lname = lname
                fet_obj.inst = inst
                fet_obj.dept = dept
                fet_obj.save()
                msg = "Faculty Updated Successfully"
                name = f"{fet_obj.fname} {fet_obj.lname}"
                return render(request, 'faculty_update.html', {'form': form, 'id': pk_, 'msg': msg, 'name': name, 'attend': attend, 'username': username})

        else:
            er_msg = "Some fields need to be filled to save details."
            return render(request, 'admin_login.html', {'form': form, 'details': details, 'er_msg': er_msg, 'id': id, 'username': username})

    return render(request, 'admin_login.html', {'form': form, 'msg': msg, 'details': details, 'id': id, 'username': username})


# def send_welcome_email(fname, email, password):
#     subject = 'Welcome to CHARUSAT Facial based Attendance System'
#     text = f'Hi {fname}, Please keep your password: "{password}" to access your profile page.'

#     gmail_user = 'your_email@gmail.com'  # Replace with your email
#     gmail_pwd = 'your_password'  # Replace with your password
#     message = f'Subject: {subject}\n\n{text}'

#     with smtplib.SMTP('smtp.gmail.com', 587) as smtpserver:
#         smtpserver.ehlo()
#         smtpserver.starttls()
#         smtpserver.ehlo()
#         smtpserver.login(gmail_user, gmail_pwd)
#         smtpserver.sendmail(gmail_user, email, message)
#         print("Email sent successfully.")

#To display edit form for faculty in Admin module
def faculty_update(request,id):
    msg=None
    username=request.session['fetch_username']
    
    print("Faculty updation is ongoing...")
    pi=Person.objects.get(pk=id)
    pi.is_pass_change=False
    details=Person.objects.all()
    fm=FacultyEdit(request.POST,instance=pi)
    if request.method=='POST':
        if fm.is_valid():
            fm.save()
            msg='Faculty Updated Successfully'
        else:
            pi=Person.objects.get(pk=id)
            pi.is_pass_change=False
            fm=FacultyEdit(instance=pi)
            return render(request,'faculty_update.html',{'form':fm})
    return render(request,'admin_login.html',{'form':fm,'msg':msg,'details':details,'username':username})

#To delete faculty data from Admin module
def faculty_delete(request,id):
    username=request.session['fetch_username']
    if request.method=='POST':
        pi=Person.objects.get(pk=id)
        pi_str=str(Person.objects.get(pk=id))
        values=[]
        for word in set(pi_str.split()):
            indexes = [w.start() for w in re.finditer("value", pi_str)]
        indexes= [n+6 for n in indexes]
        quote_index=[]
        for index in indexes:
            quote_index.append(pi_str.find('"',index+1))
        
        for i in range(len(indexes)):
            values.append(pi_str[indexes[i]+1:quote_index[i]])
        
        training_data_obj=TrainingData.objects.filter(reg_id=values[3])
        if training_data_obj:  #Deletion in faculty also delte training data as well.
            training_data_obj.delete()
            
        attaendance_obj=Attendance.objects.filter(reg_id=values[3])
        if attaendance_obj:   #Deletion in faculty also delete attendance data as well.
            attaendance_obj.delete()
            

        pi.delete()
        form=FacultyRegisteration()
        msg= 'Faculty Deleted Succesfully '
        details=Person.objects.all()
        return render(request,'admin_login.html',{'form':form,'del_msg':msg,'details':details,'id':0,'username':username})

#To take pictures of faculty inside Admin module
def take_pic(request,det_msg=None):
    username=request.session['fetch_username']
    form=FacultyRegisteration()
    details=Person.objects.all()
    str_msg=None
    reg_id=request.POST['reg_list']
    print(reg_id)  
    pi=str(Person.objects.get(reg_id=reg_id))
    values=[]
    for word in set(pi.split()):
        indexes = [w.start() for w in re.finditer("value", pi)]
    indexes= [n+6 for n in indexes]
    quote_index=[]
    for index in indexes:
        quote_index.append(pi.find('"',index+1))
    
    for i in range(len(indexes)):
        values.append(pi[indexes[i]+1:quote_index[i]])
    
    print("Value is : ",values)

    video = cv2.VideoCapture(0)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(base_dir,"{}\{}\{}\{}".format('static','TrainingImage',values[4],values[8] ))
    xml_dir=os.path.join(base_dir,"{}".format('static'))
    print("IMage path :",image_dir)
    print("XML path :",xml_dir)
    harcascadePath = xml_dir+"\haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    sampleNum = 0
    while True:	       #Open Webcam
        ret, img = video.read()
        small_frame = cv2.resize(img, (0,0), fx=0.5, fy= 0.5)
        rgb_small_frame = small_frame[:,:,::-1]
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(30,30),flags = cv2.CASCADE_SCALE_IMAGE)
        if faces == ():
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, 'No Face is Detected',(220,220), font, 0.8, (255,0,0),1)

        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (10, 159, 255), 2)
            
            if sampleNum<=9:
                cv2.imwrite(image_dir+"\\" +reg_id + '.0' + str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
                
            else:
                cv2.imwrite(image_dir+"\\" +reg_id + '.' + str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
            
            
            #incrementing sample number
            sampleNum = sampleNum+1
        if sampleNum>99:
            str_msg="Images are stored..."
            break
        cv2.imshow("Face Training Panel",img)
        if cv2.waitKey(1) == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()
    TrainImages(request,reg_id)
    return render(request,'face_train.html',{'str_msg':str_msg,'det_msg':det_msg,'details':details,'username':username})



#To train images and stored inside database as numpy array
def TrainImages(request,reg_id):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pi=str(Person.objects.get(reg_id=reg_id))
    values=[]
    for word in set(pi.split()):
        indexes = [w.start() for w in re.finditer("value", pi)]
    indexes= [n+6 for n in indexes]
    quote_index=[]
    for index in indexes:
        quote_index.append(pi.find('"',index+1))
    
    for i in range(len(indexes)):
        values.append(pi[indexes[i]+1:quote_index[i]])

    image_dir = os.path.join(base_dir,"{}\{}\{}\{}".format('static','TrainingImage',values[4],values[8]))
    fields=['ID','Array']
    known_face_names=[]
    known_face_encodings=[]
    for root,dirs,files in os.walk(image_dir):
        for file in files:
            if re.findall( ( "^"+str(reg_id)+".10.jpg" ),file):
                path = os.path.join(root, file)
                #print("path is : ",path)
                img = face_recognition.load_image_file(path)
                #print("img is : ",img)
                label = file[:len(file)-4]
                #print("label is : ",label)
                try:
                    img_encoding = face_recognition.face_encodings(img)[0]
                    #print("Training img is : ",img_encoding)
                    
                    fet_train_obj=TrainingData.objects.filter(reg_id=reg_id)
                    fet_train_obj_str=" ".join([str(x) for x in fet_train_obj])
                    fet_train_obj_str_lis=fet_train_obj_str.split(' ')
                    
                    #print("Fet_train id is : ",fet_train_obj_str_lis," with length : ",len(fet_train_obj_str_lis))

                    if len(fet_train_obj_str_lis)>1:    #If already face_data is stored for the same faculty
                        train_obj=TrainingData.objects.get(pk=fet_train_obj_str_lis[0])
                        train_obj.array=base64.b64encode(pickle.dumps(img_encoding))
                        train_obj.save()
                        #print("Database row is updated.....")

                    else:                               #New face_data entry for faculty
                        train_obj=TrainingData(reg_id=reg_id,array=base64.b64encode(pickle.dumps(img_encoding)))
                        train_obj.save()
                        #print("Database row is inserted....")
                    known_face_names.append(label)
                    known_face_encodings.append(img_encoding)
                except IndexError as e:
                    take_pic(request,det_msg='Face Recognition data != done succesfully, please try again')

                
    
#To recognize the face capturing from webcam 
def recognize(request):
    face_locations = []
    face_encodings = []
    values = []
    names = []

    known_face_names = []
    known_face_encodings = []

    fet_train_obj = TrainingData.objects.all()

    for obj in fet_train_obj:
        known_face_names.append(obj.reg_id)
        known_face_encodings.append(pickle.loads(base64.b64decode(obj.array)))

    ip, is_routable = get_client_ip(request)
    # print("ip of client is in recognize : ",ip)
    video = cv2.VideoCapture(0)
    Timer_var = int(10)
    print("known face names : ", known_face_names)
    print("known face encoding : ", known_face_encodings)
    
    while True and Timer_var > 0:  # Webcam is open till timer ends
        check, frame = video.read()
        if not check or frame is None:  # Check if frame is valid
            print("Failed to capture image from the webcam.")
            break  # Exit the loop if frame is invalid
        
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, 'Press S to close.', (10, 20), font, 0.8, (255, 0, 0), 1)
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        # rgb_small_frame = small_frame[:, :, ::-1]
        rgb_small_frame = cv2.cvtColor(rgb_small_frame , cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        
        if len(face_locations) == 0:  # If no face is detected
            cv2.putText(frame, 'No Face is Detected, Time left is : ' + str(Timer_var) + ' seconds.', (30, 220), font, 0.8, (0, 0, 255), 1)
            prev = time.time()
            time.sleep(1)
            curr = time.time()

            if curr - prev >= 1:
                prev = curr
                Timer_var = Timer_var - 1
                print("Timer left to close is ", Timer_var, " seconds...")
        else:
            Timer_var = 10

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, np.array(face_encoding), tolerance=0.6)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            try:
                matches = face_recognition.compare_faces(known_face_encodings, np.array(face_encoding), tolerance=0.6)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

                # to get accuracy
                if face_distances[0] > 0.6:
                    rg = 0.4
                    linear_val = (1 - face_distances[0]) / (rg * 2)
                    answer = round(linear_val * 100, 2)

                    if answer < 40:
                        answer = round(answer * 2.5, 2)

                else:
                    rg = 0.6
                    linear_val = (1.0 - face_distances[0]) / (rg * 2.0)
                    answer = (round(linear_val + ((1 - round(linear_val, 2)) * math.pow(abs(round(linear_val - 0.5, 2)) * 2, 0.2)), 2) * 100) + 10
                    if answer > 95:
                        answer -= 6

                best_match_index = np.argmin(face_distances[0])

                for i in range(len(matches)):
                    if matches[i]:
                        name = known_face_names[i]
                        name = str(name)
                        face_names.append(name)
                        if name not in names:
                            names.append(name)
            except:
                pass

        if len(face_names) == 0:
            for (top, right, bottom, left) in face_locations:
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, 'Unknown', (left, top), font, 0.8, (255, 255, 255), 1)
        else:
            pi = str(Person.objects.get(reg_id=name))

            for word in set(pi.split()):
                indexes = [w.start() for w in re.finditer("value", pi)]
            indexes = [n + 6 for n in indexes]
            quote_index = []
            for index in indexes:
                quote_index.append(pi.find('"', index + 1))

            values = []
            if name not in values:
                for i in range(len(indexes)):
                    values.append(pi[indexes[i] + 1:quote_index[i]])

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name + '-' + values[0] + ' ' + values[1] + ' (' + str(answer) + '%)', (left, top), font, 0.8, (255, 255, 255), 1)

                print("After recognizing data : ", values)
                final_value = []
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

                attendance_obj = Attendance.objects.all()
                try:
                    in_time_obj = Attendance.objects.filter(reg_id=values[3]).filter(date=date)
                except:
                    in_time_obj = None

                if in_time_obj:
                    in_time_obj_str = " ".join([str(x) for x in in_time_obj])
                    in_time_obj_str_lis = in_time_obj_str.split(' ')

                    if (str(in_time_obj_str_lis[-4]) == 'False'):
                        fetch_obj = Attendance.objects.get(pk=in_time_obj_str_lis[0])

                        tmp_intime_str = str(fetch_obj.in_time)
                        tmp_outtime_str = str(timeStamp)
                        tmp_date = str(fetch_obj.date)
                        if fetch_obj.is_leave and (str(in_time_obj_str_lis[5]) == 'None'):

                            fetch_obj.in_time = timeStamp
                            fetch_obj.is_status = 1
                            fetch_obj.save()

                        else:
                            fetch_obj.out_time = timeStamp
                            tdelta = datetime.datetime.strptime(tmp_outtime_str, '%H:%M:%S') - datetime.datetime.strptime(tmp_intime_str, '%H:%M:%S')
                            tdelta = str(tdelta)
                            ddetlta_in = tmp_date.split('-')
                            ddelta_today = date.split('-')

                            tdelta_lis = tdelta.split(':')
                            total_min = int(tdelta_lis[0]) * 60 + int(tdelta_lis[1])
                            total_min = round(total_min / 60, 2)

                            if fetch_obj.is_leave:
                                if fetch_obj.shift_leave == '2':
                                    total_min = 7.50
                                else:
                                    total_min += 3.5

                            if ddetlta_in[2] == ddelta_today[2]:
                                fetch_obj.total_hour = total_min
                                fetch_obj.is_status = 1
                                fetch_obj.save()

        cv2.imshow("Face Recognition Panel", frame)
        if cv2.waitKey(1) == ord('s'):
            break

    video.release()
    cv2.destroyAllWindows()
    qs_obj = Attendance.objects.all().update(is_status=0)
    print("status changed to 0 ...")

    return render(request, 'main.html')

#To logout from Admin module
def logout(request):
    if request.session.get('fetch_username'):   #To delete session for username of Admin/Faculty
        del request.session['fetch_username']
    return render(request,'main.html')

#To login inside faculty via Faculty module after validating credentails
def faculty_login(request):
    message=None
    values=[]
    if request.method=='POST':
        rid=request.POST['fe_id']
        password=request.POST['fe_password']
        form=Person.objects.filter(reg_id=rid)
        key=Person.objects.values('id').get(reg_id=rid)['id']
        
        if len(form) == 0:
            message = "No matching ID is found."
            return render(request, 'main.html', {'message': message})

        pi=str(form)
        for word in set(pi.split()):
            indexes = [w.start() for w in re.finditer("value", pi)]
        indexes= [n+6 for n in indexes]
        quote_index=[]
        for index in indexes:
            quote_index.append(pi.find('"',index+1))

        if rid not in values:        
            for i in range(len(indexes)):
                values.append(pi[indexes[i]+1:quote_index[i]])

        print("inside faculty_login values is : ",values)
        request.session['fetch_username']=values[0]+" "+values[1]      #Assign Faculty name to cookie
        try:
            attend=Attendance.objects.filter(reg_id=rid).filter(inst=values[4]).filter(dept=values[8])
        except:
            attend=None
        pk=Person.objects.filter(reg_id=rid).filter(password=make_password(password,"a")).values('id')

        key=Person.objects.values('id').get(reg_id=rid)['id']

        first_pass_change=Person.objects.get(pk=key)

        if len(pk) == 1 and ( str(first_pass_change.is_pass_change) == 'True'):      #If credentails are valid and it is first time login by faculty
            return render(request,"password_change.html",{'rid':rid,'id':key})
        if len(pk) == 1:                                                           #If credentailsa are valid and faculty module is accessed.
            form=Person.objects.get(pk=key)
            pi=str(Person.objects.get(pk=key))
            values=[]
            for word in set(pi.split()):
                indexes = [w.start() for w in re.finditer("value", pi)]
            indexes= [n+6 for n in indexes]
            quote_index=[]
            for index in indexes:
                quote_index.append(pi.find('"',index+1))
            
            for i in range(len(indexes)):
                values.append(pi[indexes[i]+1:quote_index[i]])

            print("values in faculty login is : ",values)
            name_str=values[0]+" "+values[1]
            form=FacultyEdit(instance=form)

            return render(request,'faculty_update.html',{'form':form, 'id':key,'attend':attend,'name':name_str})
        else:
            message='Username or Password is Invalid'
        
    
    return render(request,'main.html',{'message':message})

#To forget password for any faculty in Faculty module
def pass_change(request,id):
    message=None
    form=None
    attend=None
    name_str=None
    rid=None
    if request.method=='POST':
        rid=request.POST['fe_id']
        password=request.POST['fe_password']
        key=request.POST['id']

        form=Person.objects.filter(reg_id=rid)
        
        pk=Person.objects.filter(reg_id=rid).values('id')
        key=Person.objects.values('id').get(reg_id=rid)['id']
        pi=str(Person.objects.get(pk=key))
        values=[]
        for word in set(pi.split()):
            indexes = [w.start() for w in re.finditer("value", pi)]
        indexes= [n+6 for n in indexes]
        quote_index=[]
        for index in indexes:
            quote_index.append(pi.find('"',index+1))
        
        for i in range(len(indexes)):
            values.append(pi[indexes[i]+1:quote_index[i]])

        print("values in faculty login is : ",values)
        name_str=values[0]+" "+values[1]
        try:
            attend=Attendance.objects.filter(reg_id=rid).filter(inst=values[4]).filter(dept=values[8])
        except:
            attend=None
        first_pass_change=Person.objects.get(pk=key)
        first_pass_change.password=make_password(password,"a")
        first_pass_change.is_pass_change=0
        first_pass_change.save()
        form=Person.objects.get(pk=key)
        form=FacultyRegisteration(instance=form)
    return render(request,'faculty_update.html',{'form':form,'attend':attend,'name':name_str,'rid':rid,'id':key})

#To show forget pass page for Admin module
def forget_pass_admin(request):
    message=None
    return render(request,'forget_pass_admin.html',{'message':message})

#To verify email is from Admin database or not
def forget_pass_admin_view(request):
    if request.method=='POST':
        email=request.POST['fe_email']
        Admin=get_user_model()
        try:
            admin=Admin.objects.get(email=email)
        except Admin.DoesNotExist:
            admin=None
        
        if admin:
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(6))
            print("Random password is : ",result_str)

            subject = 'Admin Side Password Request'
            text = 'Hey Admin, Please note down this code : "'+result_str+'" to create new password.'
            

            to=email
            gmail_user='jp739709@gmail.com'
            gmail_pwd='Indian02'
            message='Subject : {}\n\n{}'.format(subject,text)
            smtpserver=smtplib.SMTP('smtp.gmail.com',587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            smtpserver.login(gmail_user, gmail_pwd)
            smtpserver.sendmail(gmail_user,to,message)
            smtpserver.close()

            return render(request,'change_admin_pass.html',{'result_str':result_str,'email':email})
        else:
            message="This email address != stored in Admin Database."
            return render(request,'forget_pass_admin.html',{'message':message})

#To validate code and update new password for Admin module
def change_admin_pass(request):
    if request.method=='POST':
        email=request.POST['fe_email']
        code_enter=request.POST['fe_code']
        code_fetch=request.POST['email_code']
        password=request.POST['fe_password']
        
        if code_enter==code_fetch:
            Admin=get_user_model()
            admin=Admin.objects.get(email=email)
            admin.set_password(password)
            admin.save()
            print("Admin password is changed successfully...")
            msg="Admin password is changed successfully..."

        else:
            message="Entered Code != matched with the emailed one."
            return render(request,'change_admin_pass.html',{'message':message,'email':email,'result_str':code_fetch})

    return render(request,"main.html",{'msg':msg})


#To display forget password page for Faculty module
def forget_pass(request):
    return render(request,'forget_pass.html')        

#To validate email and update password for faculty in case of forget password for Faculty module
def forget_change_pass(request):
    message=None
    if request.method=='POST':
        email=request.POST['fe_email']
        regex_1 = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}\w+[.]\w{2,3}$'
        regex_2='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        print("fetched email for forget is :",email," and validation is : ",re.search(regex_1,email),re.search(regex_2,email))
        if re.search(regex_1,email) or re.search(regex_2,email):
            pi=Person.objects.filter(email=email).values('id')
            print("length of found pi is : ",len(pi)==0)
            if len(pi)==0:
                message="This Email address != found in database."
                return render(request,'forget_pass.html',{'message':message})

            key=Person.objects.values('id').get(email=email)['id']
            pi=str(Person.objects.get(pk=key))
            values=[]
            for word in set(pi.split()):
                indexes = [w.start() for w in re.finditer("value", pi)]
            indexes= [n+6 for n in indexes]
            quote_index=[]
            for index in indexes:
                quote_index.append(pi.find('"',index+1))
            
            for i in range(len(indexes)):
                values.append(pi[indexes[i]+1:quote_index[i]])

            print("values in faculty login is : ",values)
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(6))
            print("Random password is : ",result_str)

            forget_pass_change=Person.objects.get(pk=key)
            forget_pass_change.password=make_password(result_str,"a")
            forget_pass_change.is_pass_change=1
            forget_pass_change.save()
            #print("forgotten new password is saved inside database...")

            subject = 'Welcome to CHARUSAT Facial based Attendance System'
            text = 'Hi '+values[0]+', Please keep your password : "'+result_str+'" remember for access your profile page.'
            
            to=email
            gmail_user='jp739709@gmail.com'
            gmail_pwd='Indian02'
            message='Subject : {}\n\n{}'.format(subject,text)
            smtpserver=smtplib.SMTP('smtp.gmail.com',587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            smtpserver.login(gmail_user, gmail_pwd)
            smtpserver.sendmail(gmail_user,to,message)
            smtpserver.close()

            message="New Password is sent in the Email."
            return render(request,'main.html',{'message':message})
        else:
            message="Email != written in proper manner."
            return render(request,'forget_pass.html',{'message':message})
            
#To apply various search filter on attendance details of all faculties inside Admin module
def search(request):
    
    username=request.session['fetch_username']
    
    attendances = Attendance.objects.all()
    query_id=request.GET['reg_id']
    query_date=request.GET['f_date']
    query_inst=request.GET['f_inst']
    query_dept=request.GET['f_dept']
    month_name=[]
    if query_id == '' and query_date == '' and query_inst == '' and query_dept == '':
        print("1")
        pass
    if query_id == '' and query_date == '' and query_inst == '' and query_dept != '':
        print("2")
        pass
    if query_id == '' and query_date == '' and query_inst != '' and query_dept == '':
        print("3")
        attendances=Attendance.objects.filter(inst=query_inst)
    if query_id == '' and query_date == '' and query_inst != '' and query_dept != '':
        print("4")
        attendances=Attendance.objects.filter(inst=query_inst).filter(dept=query_dept)

        month_lis=attendances.values_list('date')
        id_lis=attendances.values_list('reg_id')
        total_hour_lis=attendances.values_list('total_hour')

        months=[]
        dates_lis=[]
        month_name=[]
        id_name=[]
        year_list=[]
        total_hour_list=[]
        ids_lis=[]

        for i in range(len(month_lis)):
            temp_str=''.join(str(month_lis[i]))
            index=temp_str.find(',',21)
            months.append(temp_str[21:index])

            temp_id=''.join(str(id_lis[i]))
            index=temp_id.find(',')
            id_name.append(int(temp_id[1:index]))

            index=temp_str.find(')')
            dates_lis.append(int(temp_str[23:index]))

            b_index=temp_str.find('(',1)+1
            e_index=temp_str.find(',',1)
            year_list.append(int(temp_str[b_index:e_index]))

            temp_total_hour=''.join(str(total_hour_lis[i]))
            b_index=temp_total_hour.find('(')+1
            e_index=temp_total_hour.find(',',1)

            if temp_total_hour[b_index:e_index]=='None':
                total_hour_list.append(temp_total_hour[b_index:e_index])
            else:
                total_hour_list.append(float(temp_total_hour[b_index:e_index]))

            
        ids_lis=id_name
        month_record_freq=collections.Counter(months)
        
        merged_list = tuple(zip(ids_lis, dates_lis,total_hour_list))
        
        months_set=[]
        [months_set.append(x) for x in months if x not in months_set]
        
        id_name=set(id_name)
        id_name=list(id_name)
        month_dict={'1':'January','2':'February','3':'March','4':'April','5':'May','6':'June','7':'July','8':'August','9':'September','10':'October','11':'November','12':'December'}
        temp_key=list(month_dict.keys())
        temp_values=list(month_dict.values())
        month_counter_values=list(month_record_freq.values())
        for i in range(len(months_set)):
            month_name.append(temp_values[int(months_set[i])-1])
        
        res = defaultdict(list)


        for key,value,hour in merged_list:
            try:
                if hour=='None':                   
                    pass
                elif hour>7.49:
                    res[key].append(value)
                else:
                    pass
            except KeyError:
                if hour>7.49:
                    res[key]=value
                else:
                    pass


        base_dir = os.path.dirname(os.path.abspath(__file__))
        excel_dir = os.path.join(base_dir,"{}\{}".format('static','Report'))
        for i in range(len(month_name)):
            excel_path=excel_dir+"\\"+query_inst+"_"+query_dept+"_"+month_name[i]+".xlsx"
            #print("Excel file worked is : ",excel_path)
            workbook=xlsxwriter.Workbook(excel_path)   
            ws=workbook.add_worksheet()
            ws.write('A1','Dates/Reg_ID',workbook.add_format({'bold': 1}))
            format1=workbook.add_format({'bg_color':'#FF0000'})
            format2=workbook.add_format({'bg_color':'#00FF00'})
            g_font=workbook.add_format({'font_color':'green'})
            r_font=workbook.add_format({'font_color':'red'})
            h_font=workbook.add_format({'font_color':'blue'})
            if month_name[i]=='January' or month_name[i]=='March' or month_name[i]=='May' or month_name[i]=='July' or month_name[i]=='August' or month_name[i]=='October' or month_name[i]=='December':
                ws.write_column('A2',(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31))
                ws.write('A34','Present Days : ')
                ws.write('A35','Total Hours : ')
                
                fet_date_lis=str(Holidays.objects.values_list('day',flat=True).filter(year=year_list[0]).filter(month=month_name[i]))
                b_index=fet_date_lis.find('[')+2
                e_index=fet_date_lis.find(']')-1
                fet_date_lis=fet_date_lis[b_index:e_index]
                
                if fet_date_lis != '':
                    int_date=[int(i) for i in fet_date_lis.split(" ")]
                else:
                    int_date=None
                
                if i==0:
                    for m in range(0,month_counter_values[i]):
                        id__name=ids_lis[0:month_counter_values[i]]
                        id__set=list(set(id__name))
                        #print("id_name after dividing in months inside i=0 if for 31: ",id__set)
                        ids__lis=ids_lis[0:month_counter_values[i]]
                        dates__lis=dates_lis[0:month_counter_values[i]]
                        hours__lis=total_hour_list[0:month_counter_values[i]]
                        merged__list = tuple(zip(ids__lis, dates__lis,hours__lis))

                        
                        res_ = defaultdict(list)
                        hours=defaultdict(list)
                        for key,value,hour in merged__list:
                            try:
                                if hour=='None':
                                    pass
                                else:
                                    hours[key]=float(hours.get(key))+float(hour)
                            except:
                                hours[key]=float(hour)

                        for key,value,hour in merged__list:
                            try:
                                if hour=='None':
                                    
                                    pass
                                elif (hour)>7.49:
                                    
                                    res_[key].append(value)
                                else:
                                    
                                    pass
                        
                            except KeyError:
                                if hour>7.49:
                                    res_[key]=value
                                else:
                                    pass
                        #print("Dictinoary after dividing in months inside i=0 if for 31: ",str(res_))
                        ws.write_row('B1',id__set,workbook.add_format({'bold': 1}))
                        for k in range(len(id__set)):
                            ws.write_column(chr(ord('B')+k)+'2',('A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A'),r_font)
                            present_lis=res_.get(id__set[k])
                            #print("values after dividing in months inside i=0 if for 31: ",present_lis)
                            if int_date != None:
                                for j in range(len(int_date)):
                                    ws.write(chr(ord('B')+k)+str(int_date[j]+1),'H',h_font)

                            if present_lis != None:
                                for j in range(len(present_lis)):
                                    ws.write(chr(ord('B')+k)+str(present_lis[j]+1),'P',g_font)
                                    
                                
                                ws.write(chr(ord('B')+k)+str(34),len(present_lis))
                                
                            else:
                                ws.write(chr(ord('B')+k)+str(34),0)
                            
                            if int_date != None:
                                ws.conditional_format( chr(ord('B')+k)+str(34), {'type':'cell','criteria':'>=','value':(31-len(int_date))//2 ,'format':format2} )
                                ws.conditional_format( chr(ord('B')+k)+str(34), {'type':'cell','criteria':'<','value':(31-len(int_date))//2,'format':format1} )
                            else:
                                ws.conditional_format( chr(ord('B')+k)+str(34), {'type':'cell','criteria':'>=','value':(31)//2 ,'format':format2} )
                                ws.conditional_format( chr(ord('B')+k)+str(34), {'type':'cell','criteria':'<','value':(31)//2,'format':format1} )

                        hour_value_list=list(hours.values())
                        for k in range(len(hour_value_list)):
                            ws.write(chr(ord('B')+k)+str(35),hour_value_list[k])
                        chart=workbook.add_chart({'type':'bar'})
                        chart.add_series({'categories':'=Sheet1!$B$1:$'+chr(ord('B')+len(id__set))+'$1','values':'=Sheet1!$B$34:$'+chr(ord('B')+len(id__set))+'$34'})
                        chart.set_title({'name':'Monthly Report of Faculties Attendance'})
                        chart.set_x_axis({'name':'Number of Present Days'})
                        chart.set_y_axis({'name':'Faculty IDs'})
                        ws.insert_chart('B37',chart)

                        chart=workbook.add_chart({'type':'bar'})
                        chart.add_series({'categories':'=Sheet1!$B$1:$'+chr(ord('B')+len(id__set))+'$1','values':'=Sheet1!$B$35:$'+chr(ord('B')+len(id__set))+'$35'})
                        chart.set_title({'name':'Monthly Report of Faculties Attendance'})
                        chart.set_x_axis({'name':'Total Working Hours'})
                        chart.set_y_axis({'name':'Faculty IDs'})
                        ws.insert_chart('K37',chart)




                else:
                    for m in range(month_counter_values[i-1],month_counter_values[i-1]+month_counter_values[i]):
                        id__name=ids_lis[month_counter_values[i-1]:month_counter_values[i-1]+month_counter_values[i]]
                        id__set=list(set(id__name))
                        #print("id_name after dividing in months inside i!=0 else for 31: ",id__name)
                        ids__lis=ids_lis[month_counter_values[i-1]:month_counter_values[i-1]+month_counter_values[i]]
                        dates__lis=dates_lis[month_counter_values[i-1]:month_counter_values[i-1]+month_counter_values[i]]
                        hours__lis=total_hour_list[month_counter_values[i-1]:month_counter_values[i-1]+month_counter_values[i]]
                        merged__list = tuple(zip(ids__lis, dates__lis,hours__lis))
                        res_ = defaultdict(list)
                        hours=defaultdict(list)
                        for key,value,hour in merged__list:
                            try:
                                if hour=='None':
                                    pass
                                else:
                                    hours[key]=float(hours.get(key))+float(hour)
                            except:
                                hours[key]=float(hour)

                        for key,value,hour in merged__list:
                            try:
                                if hour=='None':
                                    pass
                                elif (hour)>7.49:
                                    res_[key].append(value)
                                else:
                                    pass

                            except KeyError:
                                if hour>7.49:
                                    res_[key]=value
                                else:
                                    pass
                        #print("Dictinoary after dividing in months inside i!=0 else for 31: ",str(res_))
                        ws.write_row('B1',id__set,workbook.add_format({'bold': 1}))
                        for k in range(len(id__set)):
                            ws.write_column(chr(ord('B')+k)+'2',('A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A'),r_font)
                            present_lis=res_.get(id__set[k])
                            #print("values after dividing in months inside i!=0 else for 31: ",present_lis)
                            if int_date != None:
                                for j in range(len(int_date)):
                                    ws.write(chr(ord('B')+k)+str(int_date[j]+1),'H',h_font)

                            if present_lis != None:
                                for j in range(len(present_lis)):
                                    ws.write(chr(ord('B')+k)+str(present_lis[j]+1),'P',g_font)
                                
                                ws.write(chr(ord('B')+k)+str(34),len(present_lis))
                                
                            else:
                                ws.write(chr(ord('B')+k)+str(34),0)
                            if int_date != None:
                                ws.conditional_format( chr(ord('B')+k)+str(34), {'type':'cell','criteria':'>=','value':(31-len(int_date))//2,'format':format2} )
                                ws.conditional_format( chr(ord('B')+k)+str(34), {'type':'cell','criteria':'<','value':(31-len(int_date))//2,'format':format1} )
                            else:
                                ws.conditional_format( chr(ord('B')+k)+str(34), {'type':'cell','criteria':'>=','value':(31)//2,'format':format2} )
                                ws.conditional_format( chr(ord('B')+k)+str(34), {'type':'cell','criteria':'<','value':(31)//2,'format':format1} )

                        hour_value_list=list(hours.values())
                        for k in range(len(hour_value_list)):
                            ws.write(chr(ord('B')+k)+str(35),hour_value_list[k])

                        chart=workbook.add_chart({'type':'bar'})
                        chart.add_series({'categories':'=Sheet1!$B$1:$'+chr(ord('B')+len(id__set))+'$1','values':'=Sheet1!$B$34:$'+chr(ord('B')+len(id__set))+'$34'})
                        chart.set_title({'name':'Monthly Report of Faculties Attendance'})
                        chart.set_x_axis({'name':'Number of Present Days'})
                        chart.set_y_axis({'name':'Faculty IDs'})
                        ws.insert_chart('B37',chart)

                        chart=workbook.add_chart({'type':'bar'})
                        chart.add_series({'categories':'=Sheet1!$B$1:$'+chr(ord('B')+len(id__set))+'$1','values':'=Sheet1!$B$35:$'+chr(ord('B')+len(id__set))+'$35'})
                        chart.set_title({'name':'Monthly Report of Faculties Attendance'})
                        chart.set_x_axis({'name':'Total Working Hours'})
                        chart.set_y_axis({'name':'Faculty IDs'})
                        ws.insert_chart('K37',chart)


            if month_name[i]=='April' or month_name[i]=='June' or month_name[i]=='September' or month_name[i]=='November':
                ws.write_column('A2',(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30))
                ws.write('A33','Present Days : ')
                ws.write('A34','Total Hours : ')
                fet_date_lis=str(Holidays.objects.values_list('day',flat=True).filter(year=year_list[0]).filter(month=month_name[i]))
                b_index=fet_date_lis.find('[')+2
                e_index=fet_date_lis.find(']')-1
                fet_date_lis=fet_date_lis[b_index:e_index]
                if fet_date_lis != '':
                    int_date=[int(i) for i in fet_date_lis.split(" ")]
                else:
                    int_date=None
                
                if i==0:
                    for m in range(0,month_counter_values[i]):
                        
                        ids__lis=ids_lis[0:month_counter_values[i]]
                        id__name=ids__lis[0:month_counter_values[i]]
                        id__set=list(set(id__name))
                        #print("id_name after dividing in months inside i=0 if for 30: ",id__set)
                        dates__lis=dates_lis[0:month_counter_values[i]]
                        hours__lis=total_hour_list[0:month_counter_values[i]]
                        merged__list = tuple(zip(ids__lis, dates__lis,hours__lis))
                        res_ = defaultdict(list)
                        hours=defaultdict(list)
                        for key,value,hour in merged__list:
                            try:
                                if hour=='None':
                                    pass
                                else:
                                    hours[key]=float(hours.get(key))+float(hour)
                            except:
                                hours[key]=float(hour)

                        for key,value,hour in merged__list:
                            try:
                                if hour=='None':
                                    pass
                                elif (hour)>7.49:
                                    res_[key].append(value)
                                else:
                                    pass
                                
                            except KeyError:
                                if hour>7.49:
                                    res_[key]=value
                                else:
                                    pass
                        #print("Dictinoary after dividing in months inside i=0 if for 30: ",str(res_))
                        ws.write_row('B1',id__set,workbook.add_format({'bold': 1}))
                        for k in range(len(id__set)):
                            ws.write_column(chr(ord('B')+k)+'2',('A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A'),r_font)
                            present_lis=res_.get(id__set[k])
                            #print("values after dividing in months inside i=0 if for 30: ",present_lis)
                            if int_date != None:
                                for j in range(len(int_date)):
                                    ws.write(chr(ord('B')+k)+str(int_date[j]+1),'H',h_font)
                            if present_lis != None:
                                for j in range(len(present_lis)):
                                    ws.write(chr(ord('B')+k)+str(present_lis[j]+1),'P',g_font)
                                
                                ws.write(chr(ord('B')+k)+str(33),len(present_lis))
                                
                            else:
                                ws.write(chr(ord('B')+k)+str(33),0)
                            if int_date != None:
                                ws.conditional_format( chr(ord('B')+k)+str(33), {'type':'cell','criteria':'>=','value':(30-len(int_date))//2,'format':format2} )
                                ws.conditional_format( chr(ord('B')+k)+str(33), {'type':'cell','criteria':'<','value':(30-len(int_date))//2,'format':format1} )
                            else:
                                ws.conditional_format( chr(ord('B')+k)+str(33), {'type':'cell','criteria':'>=','value':(30)//2,'format':format2} )
                                ws.conditional_format( chr(ord('B')+k)+str(33), {'type':'cell','criteria':'<','value':(30)//2,'format':format1} )
                        
                        hour_value_list=list(hours.values())
                        for k in range(len(hour_value_list)):
                            ws.write(chr(ord('B')+k)+str(34),hour_value_list[k])

                        chart=workbook.add_chart({'type':'bar'})
                        chart.add_series({'categories':'=Sheet1!$B$1:$'+chr(ord('B')+len(id__set))+'$1','values':'=Sheet1!$B$33:$'+chr(ord('B')+len(id__set))+'$33'})
                        chart.set_title({'name':'Monthly Report of Faculties Attendance'})
                        chart.set_x_axis({'name':'Number of Present Days'})
                        chart.set_y_axis({'name':'Faculty IDs'})
                        ws.insert_chart('B37',chart)

                        chart=workbook.add_chart({'type':'bar'})
                        chart.add_series({'categories':'=Sheet1!$B$1:$'+chr(ord('B')+len(id__set))+'$1','values':'=Sheet1!$B$34:$'+chr(ord('B')+len(id__set))+'$34'})
                        chart.set_title({'name':'Monthly Report of Faculties Attendance'})
                        chart.set_x_axis({'name':'Total Working Hours'})
                        chart.set_y_axis({'name':'Faculty IDs'})
                        ws.insert_chart('K37',chart)

                else:
                    for m in range(month_counter_values[i-1],month_counter_values[i-1]+month_counter_values[i]):
                        id__name=ids_lis[month_counter_values[i-1]:month_counter_values[i-1]+month_counter_values[i]]
                        id__set=list(set(id__name))
                        #print("id_name after dividing in months inside i!=0 else for 30: ",id__set)
                        ids__lis=ids_lis[month_counter_values[i-1]:month_counter_values[i-1]+month_counter_values[i]]
                        dates__lis=dates_lis[month_counter_values[i-1]:month_counter_values[i-1]+month_counter_values[i]]
                        hours__lis=total_hour_list[month_counter_values[i-1]:month_counter_values[i-1]+month_counter_values[i]]
                        merged__list = tuple(zip(ids__lis, dates__lis,hours__lis))
                        res_ = defaultdict(list)
                        hours=defaultdict(list)
                        for key,value,hour in merged__list:
                            try:
                                if hour=='None':
                                    pass
                                else:
                                    hours[key]=float(hours.get(key))+float(hour)
                            except:
                                hours[key]=float(hour)

                        for key,value,hour in merged__list:
                            try:
                                if hour=='None':
                                    pass
                                elif (hour)>7.49:
                                    res_[key].append(value)
                                else:
                                    pass

                            except KeyError:
                                if hour>7.49:
                                    res_[key]=value
                                else:
                                    pass

                        #print("Dictinoary after dividing in months inside i!=0 else for 30: ",str(res_))
                        ws.write_row('B1',id__set,workbook.add_format({'bold': 1}))
                        for k in range(len(id__set)):
                            ws.write_column(chr(ord('B')+k)+'2',('A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A'),r_font)
                            present_lis=res_.get(id__set[k])
                            #print("values after dividing in months inside i!=0 else for 30: ",present_lis)
                            if int_date != None:
                                for j in range(len(int_date)):
                                    ws.write(chr(ord('B')+k)+str(int_date[j]+1),'H',h_font)
                            if present_lis != None:
                                for j in range(len(present_lis)):
                                    ws.write(chr(ord('B')+k)+str(present_lis[j]+1),'P',g_font)
                                
                                ws.write(chr(ord('B')+k)+str(33),len(present_lis))
                                
                            else:
                                ws.write(chr(ord('B')+k)+str(33),0)
                            if int_date != None:
                                ws.conditional_format( chr(ord('B')+k)+str(33), {'type':'cell','criteria':'>=','value':(30-len(int_date))//2,'format':format2} )
                                ws.conditional_format( chr(ord('B')+k)+str(33), {'type':'cell','criteria':'<','value':(30-len(int_date))//2,'format':format1} )
                            else:
                                ws.conditional_format( chr(ord('B')+k)+str(33), {'type':'cell','criteria':'>=','value':(30)//2,'format':format2} )
                                ws.conditional_format( chr(ord('B')+k)+str(33), {'type':'cell','criteria':'<','value':(30)//2,'format':format1} )
                        
                        hour_value_list=list(hours.values())
                        for k in range(len(hour_value_list)):
                            ws.write(chr(ord('B')+k)+str(34),hour_value_list[k])

                        chart=workbook.add_chart({'type':'bar'})
                        chart.add_series({'categories':'=Sheet1!$B$1:$'+chr(ord('B')+len(id__set))+'$1','values':'=Sheet1!$B$33:$'+chr(ord('B')+len(id__set))+'$33'})
                        chart.set_title({'name':'Monthly Report of Faculties Attendance'})
                        chart.set_x_axis({'name':'Number of Present Days'})
                        chart.set_y_axis({'name':'Faculty IDs'})
                        ws.insert_chart('B37',chart)

                        chart=workbook.add_chart({'type':'bar'})
                        chart.add_series({'categories':'=Sheet1!$B$1:$'+chr(ord('B')+len(id__set))+'$1','values':'=Sheet1!$B$34:$'+chr(ord('B')+len(id__set))+'$34'})
                        chart.set_title({'name':'Monthly Report of Faculties Attendance'})
                        chart.set_x_axis({'name':'Total Working Hours'})
                        chart.set_y_axis({'name':'Faculty IDs'})
                        ws.insert_chart('K37',chart)
        
            workbook.close()






    if query_id == '' and query_date != '' and query_inst == '' and query_dept == '':
        print("5")
        attendances=Attendance.objects.filter(date=query_date)
    if query_id == '' and query_date != '' and query_inst == '' and query_dept != '':
        print("6")
        attendances=Attendance.objects.filter(date=query_date)
    if query_id == '' and query_date != '' and query_inst != '' and query_dept =='':
        print("7")
        attendances=Attendance.objects.filter(date=query_date).filter(inst=query_inst)
    if query_id ==  '' and query_date != '' and query_inst != '' and query_dept !=  '':
        print("8")
        attendances=Attendance.objects.filter(date=query_date).filter(inst=query_inst).filter(dept=query_dept)
    if query_id != '' and query_date == '' and query_inst == '' and query_dept ==  '':
        print("9")
        attendances=Attendance.objects.filter(reg_id=query_id)
    if query_id != '' and query_date == '' and query_inst == '' and query_dept != '':
        print("10")
        attendances=Attendance.objects.filter(reg_id=query_id)
    if query_id != '' and query_date == '' and query_inst != '' and query_dept == '':
        print("11")
        attendances=Attendance.objects.filter(reg_id=query_id).filter(inst=query_inst)
    if query_id != '' and query_date == '' and query_inst != '' and query_dept != '':
        print("12")
        attendances=Attendance.objects.filter(reg_id=query_id).filter(inst=query_inst).filter(dept=query_dept)
    if query_id != '' and query_date != '' and query_inst == '' and query_dept == '':
        print("13")
        attendances=Attendance.objects.filter(reg_id=query_id).filter(date=query_date)
    if query_id != '' and query_date != '' and query_inst == '' and query_dept != '':
        print("14")
        attendances=Attendance.objects.filter(reg_id=query_id).filter(date=query_date)
    if query_id != '' and query_date != '' and query_inst != '' and query_dept == '':
        print("15")
        attendances=Attendance.objects.filter(reg_id=query_id).filter(date=query_date).filter(inst=query_inst)
    if query_id != '' and query_date != '' and query_inst != '' and query_dept != '':
        print("16")
        attendances=Attendance.objects.filter(reg_id=query_id).filter(date=query_date).filter(inst=query_inst).filter(dept=query_dept)

    return render(request, 'attendance.html',{'attend':attendances,'username':username,'month':month_name,'inst':query_inst,'dept':query_dept})

#To display attendance page in Admin module
def attendance(request):
    username=request.session['fetch_username']
    attend=Attendance.objects.all()
     
    return render(request,'attendance.html',{'attend':attend,'username':username})

#To display holiday pade in Admin module
def holiday_page(request):

    return render(request,"holiday_page.html")

#To store holidays inside database from Admin module
def holidays(request):
    str_msg=None
    if request.method=='POST':
        year=int(request.POST['year'])
        month=request.POST['month']
        day=request.POST.getlist('day')
        month_dict={'0':'January','1':'February','2':'March','3':'April','4':'May','5':'June','6':'July','7':'August','8':'September','9':'October','10':'November','11':'December'}
        day = [int(i) for i in day]
        day.sort()

        #print("Details of holidays are --> Year : ",year," Month : ",month," Days : ",day)
        day = [str(i) for i in day]
        day_str=' '.join(day)
        month=month_dict.get(month)
        #print("String of dates is : ",day_str)
        holiday_obj=Holidays.objects.filter(year=year).filter(month=month)
        if holiday_obj:                     #To update existing entry of holiday of that particular month
            holiday_lis=str(holiday_obj).split(" ")
            #print("Holiday list's pk from db is : ",holiday_lis[2])
            holiday=Holidays.objects.get(pk=int(holiday_lis[2]))
            holiday.day=day_str
            holiday.save()
            str_msg="Holidays are updated inside database."
        else:                               #To store new entry of holiday of that particular month
            holiday=Holidays(year=year,month=month,day=day_str)
            holiday.save()
            str_msg="Holidays are stored inside database."
    
    return render(request,"holiday_page.html",{'str_msg':str_msg})

#To download excel file directly
def report(request):
    if request.method=='POST':
        base_dir = os.path.dirname(os.path.abspath(__file__))
        excel_dir = os.path.join(base_dir,"{}\{}".format('static','Report'))
        month_name=request.POST['month_list']
        query_inst=request.POST['f_inst']
        query_dept=request.POST['f_dept']
        
        filename=excel_dir+"\\"+query_inst+"_"+query_dept+"_"+month_name+".xlsx"
        print("filename is : ",filename)
        if os.path.exists(filename):
            with open(filename,'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' +query_inst+"_"+query_dept+"_"+ month_name+".xlsx"
                return response

#To download pdf file directly
def pdf_report(request):
    if request.method == 'POST':
        base_dir = os.path.dirname(os.path.abspath(__file__))
        excel_dir = os.path.join(base_dir, "{}\{}".format('static', 'Report'))

        month_name = request.POST["month_name_pdf"]
        month = month_name

        query_inst = request.POST ['f_inst']
        query_dept = request.POST ['f_dept']
        
        month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7 :'July',
                      8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        for key, value in month_dict.items():
            if month_name == value:
                month_name = key

        attendances = Attendance.objects.filter(inst=query_inst).filter(dept=query_dept).filter(date__month=month_name)
        filename = excel_dir + "\\" + query_inst + "_" + query_dept + "_" + str(month) + ".pdf"
        response = HttpResponse(content_type='application/pdf')
        response ['Content-Disposition'] = 'attechment; filename='+ query_inst + "_" + query_dept + "_" + str(month) + '.pdf'
        response ['Content-Transfer-Encoding'] = 'binary'
        html_string = render_to_string(
            'report_pdf.html', {'attend': attendances,'month_name':month,'dept':query_dept,'inst':query_inst , 'total': len(attendances)}
        )

        html = HTML(string=html_string)

        result = html.write_pdf()

        with open(filename,'wb') as output:
            output.write(result)
            output.flush()

            output = open(output.name, 'rb')
            response.write(output.read())
            return response


#To display face_train page from Admin module
def face_train(request):
    details=Person.objects.all()
    username=request.session['fetch_username']
    return render(request,'face_train.html',{'details':details,'username':username})

#To display leave page from Admin module
def leave_page(request):
    details=Person.objects.all()
    username=request.session['fetch_username']
    return render(request,'leave_page.html',{'details':details})

#To assign particular leave to particular faculty from Admin module
def leave_grant(request):
    if request.method=='POST':
        details=Person.objects.all()
        fet_id=request.POST['reg_list']
        fet_date=datetime.datetime.strptime( str(request.POST['datefield']),'%Y-%m-%d' )
        fet_date=fet_date.date()
        
        fet_type=request.POST['type_leave']
        fet_shift=request.POST['type_shift']
        obj=str(Person.objects.filter(reg_id=fet_id))
        #print("Date is : ",fet_date," with the type : ",type(fet_date))

        values=[]
        for word in set(obj.split()):
            indexes = [w.start() for w in re.finditer("value", obj)]
        indexes= [n+6 for n in indexes]
        quote_index=[]
        for index in indexes:
            quote_index.append(obj.find('"',index+1))
            
        for i in range(len(indexes)):
            values.append(obj[indexes[i]+1:quote_index[i]])
        
        attend_filter=Attendance.objects.filter(reg_id=fet_id).filter(date=fet_date)
        attend_filter_lis=str(attend_filter).split(" ")
        if attend_filter:
            #print("first thing is : ",attend_filter_lis[2])
            attend_obj=Attendance.objects.get(pk=attend_filter_lis[2])
            if fet_shift=='2':
                attend_obj.total_hour=7.50
            else:
                attend_obj.total_hour=None
            attend_obj.is_leave=1
            attend_obj.type_leave=fet_type
            attend_obj.shift_leave=fet_shift
            attend_obj.save()
        else:
            if fet_shift=='2':
                attend=Attendance(reg_id=fet_id,inst=values[4],dept=values[8],date=fet_date,total_hour=7.50,is_leave=1,type_leave=fet_type,shift_leave=fet_shift)
                attend.save()
            else:
                attend=Attendance(reg_id=fet_id,inst=values[4],dept=values[8],date=fet_date,is_leave=1,type_leave=fet_type,shift_leave=fet_shift)
                attend.save()


        msg="Leave Granted to Faculty..."
    return render(request,'leave_page.html',{'details':details,'msg':msg})

class PersonListView(ListView):
    model = Person
    context_object_name = 'people'


class PersonCreateView(CreateView):
    model = Person
    form_class = FacultyRegisteration
    success_url = reverse_lazy('person_changelist')


class PersonUpdateView(UpdateView):
    model = Person
    form_class = FacultyRegisteration
    success_url = reverse_lazy('person_changelist')

#To load departments which are dependent on institute
def load_cities(request):
    country_id = request.GET.get('inst')
    cities = City.objects.filter(inst_id=country_id)
    return render(request, 'city_dropdown_list_options.html', {'cities': cities})