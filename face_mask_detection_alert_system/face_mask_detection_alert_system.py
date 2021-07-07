# -*- coding: utf-8 -*-
"""face_mask_detection_alert_system.ipynb

Porfolio project Made by Muhammad Haseeb Farooq
contact: hf.haseebfarooq@gmail.com
Original file is located at
    https://colab.research.google.com/drive/1tqYLr4xuPlvMcFb5gBYL4m4McvERc-ki
"""

# import necessary libraries
from keras.models import load_model
import cv2
import numpy as np
import tkinter
from tkinter import messagebox
import smtplib

#initialize Tkinter
root = tkinter.Tk()
root.withdraw()


#load trained model
model = load_model('models/face_mask_model.h5')

#classifier to detect face
face_det_classifier=cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')

#capture video
vid_source=cv2.VideoCapture(0)

#creating dictionaires for details of mask detection
#if green than mask is on and if not than red color will show

test_dict={0: 'Mask On', 1:'No Mask'}
rect_color_dict={0:{0,255,0},1:{0,0,255}}

#Note 0 is for Mask and 1 is for No mask class

SUBJECT = "Subject"
TEXT = "Face Mask Policy Violated"

#implementing a logic with while and for loop

while(True):
    
    ret, img = vid_source.read()
    grayscale_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_det_classifier.detectMultiScale(grayscale_img,1.3,5)
    
    for (x,y,w,h) in faces:
        
        face_img = grayscale_img[y:y+w,x:x+w]
        resized_img = cv2.resize(face_img,(112,112))
        normalized_img = resized_img/255.0
        reshaped_img = np.reshape(normalized_img,(1,112,112,1))
        result = model.predict(reshape_img)
        
        label=np.argmax(result,axis=1)[0]
        
        cv2.rectangle(img,(x,y),(x+w,y+h),rect_color_dict[label],2)
        cv2.rectangle(img,(x,y-40),(x+w,y),rect_color_dict[label],-1)
        cv2.putText(img,text_dict[label],(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,0),2)
        
        #IF STATEMENT FOR WARNING
        if (label==1):
            messagebox.showwarning("warning","Wear a Face Mask")
            #logic for sending email as alear
            '''
            message = 'Subject: {}\n\n{}'.format{SUBJECT, TEXT}
            mail= setplib.SMTP('smtp.gmail.com', 587)
            mail.echo()
            mail.starttls()
            mail.login('email address', 'password')
            mail.sendmail('email address', 'email address', message)
            mail.close
    
            '''
        else:
            pass
            break
        
        cv2.imshow('Live Video Feed', img)
        key= cv2.waitkey(1)
        
        if(key==27):#escape key
            break
    
    vid_source.release()
    cv2.destroyAllWindow()
    #source.release()