import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from db import retrieve, insertData
# from PIL import ImageGrab
import time
import uuid
from models.models import Person
from PIL import Image as im
from multi_crop import crop_face


path = 'image_list'
images = []
classNames = []
ImageNames=[]
myList = os.listdir(path)
tolerance=0.6
#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
def captureScreen(bbox=(300,300,690+300,530+300)):
    capScr = np.array(ImageGrab.grab(bbox))
    capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
    return capScr

def first_insert_record():
    print("Record Not Found !")
    val=int(input("Press '1' to Insert your record In Database  \n Press '2' to Exit"))
    if(val==1):
        name=input("Enter the name:\t")
        id=str(uuid.uuid4())
        adhar_no=int(input("Enter the adhar no:\t"))
        mobile_no=int(input("Enter your mobile no:\t"))
        address=input("Enter your address:\t")
        ptype=input("Person type:\t")
        threat=input("Threat YES | NO:\t")
        imgfile=input("Enter the image file path:\t")
        # img_arr=captureScreen()
        # imgfile=imgfile.replace(imgfile.split('.')[0],id)
        # imgfile = im.fromarray(img_arr)
        # imgfile=imgfile.save(path+'/'+id+'.jpg')
        per=Person(name, id, adhar_no, imgfile, address, mobile_no, ptype, threat)
        insertData(per.name, per.id, per.adhar_no, per.imgfile, per.address, per.mobile_no, per.ptype, per.threat)
        return exit(1)


# print(myList)
if(len(myList)<1):
    first_insert_record()
else:
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
        ImageNames.append(f'{cl}')
    # print(classNames)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


encodeListKnown = findEncodings(images)
print('Encoding Complete')

####################################################################################################
# ----------------------------Using Live webcam-----------------------------------------------------


# cap = cv2.VideoCapture(0)

# while True:
#     success, img = cap.read()
# # img = captureScreen()
#     imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

#     facesCurFrame = face_recognition.face_locations(imgS)
#     encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

#     for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
#         matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
#         faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
#         print(faceDis)
#         matchIndex = np.argmin(faceDis)

#         if matches[matchIndex]:
#             name = classNames[matchIndex].upper()
#             org_img=ImageNames[matchIndex]
# # print(name)
#             y1, x2, y2, x1 = faceLoc
#             y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#             cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
#             cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
#         # print(org_img)
#         # print(retrieve(org_img))
#             print(retrieve(classNames[matchIndex]))
#             time.sleep(2)
#             exit(1)
#         else:
#             # insert_record()
#             print("Record Not Found !")
#             val=int(input("Press '1' to Insert your record In Database  \n Press '2' to Exit:\t"))
#             if(val==1):
#                 name=input("Enter the name:\t")
#                 id=str(uuid.uuid4())
#                 adhar_no=int(input("Enter the adhar no:\t"))
#                 mobile_no=int(input("Enter your mobile no:\t"))
#                 address=input("Enter your address:\t")
#                 ptype=input("Person type:\t")
#                 threat=input("Threat YES | NO:\t")

#                 # ----------Manual Upload ------------------
#                 # imgfile=input("Enter the image file path:\t")
#                 # imgfile=imgfile.replace(imgfile.split('.')[0],id)
#                 # ----------------------------------------------
#                 imgfile = im.fromarray(img)
#                 # print(imgfile)
#                 store_path='uploads/'+id+".png"
#                 cv2.imwrite(store_path, img)
#                 imgfile=store_path
#                 per=Person(name, id, adhar_no, imgfile, address, mobile_no, ptype, threat)
#                 insertData(per.name, per.id, per.adhar_no, per.imgfile, per.address, per.mobile_no, per.ptype, per.threat)
#                 exit(1)
#             else:
#                 exit(1)

#     cv2.imshow('Webcam', img)
#     cv2.waitKey(1)

###################################################################################################


def verify(all_img):
    # all_img= crop_face()
    cnt=0
    for img in all_img:
        cnt+=1
        img = cv2.imread(img)

        #------show Image--------------
        show_img = im.open(all_img[cnt-1]) 
        show_img.show()
        # time.sleep(4)
        

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                org_img=ImageNames[matchIndex]
        # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                # cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            # print(org_img)
            # print(retrieve(org_img))
                print(retrieve(classNames[matchIndex]))
                # return retrieve(classNames[matchIndex])
                # img = cv2.imread(img)
                # cv2.imshow('show_img', show_img)
                # time.sleep(2)
                # exit(1)
            else:
                    # ------show Image--------------
                # show_img = im.open(all_img[cnt-1]) 
                # show_img.show()
                # show_img = cv2.imread(all_img[cnt-1])
                # cv2.imshow('show_img', show_img) 
                
                # time.sleep(3)

                print("Record Not Found !")
                val=int(input("Press '1' to Insert your record In Database \nPress '2' to Skip  \nPress '3' to Exit:\t"))
                if(val==1):
                    name=input("Enter the name:\t")
                    id=str(uuid.uuid4())

                    adhar_no=int(input("Enter the adhar no:\t"))
                    mobile_no=int(input("Enter your mobile no:\t"))
                    address=input("Enter your address:\t")
                    ptype=input("Person type:\t")
                    threat=input("Threat YES | NO:\t")
                    show_resp={'Id':id,'Name':name,'Mobile No':mobile_no,'Adhar No':adhar_no,'Address':address, 'Person Type':ptype, 'Threat':threat}
                    print('Your Record :{} inserted successfully '.format(show_resp))
                    # ----------Manual Upload ------------------
                    # imgfile=input("Enter the image file path:\t")
                    # imgfile=imgfile.replace(imgfile.split('.')[0],id)
                    # ----------------------------------------------

                    imgfile= all_img[cnt-1]
                    imgfile=imgfile.replace(imgfile.split('.')[0],'uploads/'+id)
                    cv2.imwrite(imgfile, img)

                    per=Person(name, id, adhar_no, imgfile, address, mobile_no, ptype, threat)
                    insertData(per.name, per.id, per.adhar_no, per.imgfile, per.address, per.mobile_no, per.ptype, per.threat)
                elif(val==2):
                    continue
                else:
                    exit(1)
