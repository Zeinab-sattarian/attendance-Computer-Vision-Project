import numpy as np
import cv2
import face_recognition
import os
from datetime import datetime

path = 'registeredImages'
images = []
members = []
myList = os.listdir(path)
#print(myList)
for member in myList:
    currentImg = cv2.imread(f'{path}/{member}')
    images.append(currentImg)
    members.append(os.path.splitext(member)[0])

print(members)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('attendanceList.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0]) # Will be name
        if name not in nameList: # will ony set a record if face is not repeated
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S') # Time format
            f.writelines(f'\n{name},{dtString}')




encodeMemberFaces = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read(())
    # reduce the size od the real time image
    imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # 1/4 of the original size
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    faceInCurrentFrame = face_recognition.face_locations(imgSmall)
    encodeInCurrentFrame = face_recognition.face_encodings(imgSmall, faceInCurrentFrame)

    for encodeFace, faceloc in zip(encodeInCurrentFrame,
                                   faceInCurrentFrame):  # we want them in the same loop, so we use zip
        matches = face_recognition.compare_faces(encodeMemberFaces, encodeFace)
        faceDist = face_recognition.face_distance(encodeMemberFaces, encodeFace)
        # print(faceDist)

        matchIndex = np.argmin(faceDist)

        if matches[matchIndex]:
            name = members[matchIndex].upper()
            # print(name)
            up, right, down, left = faceloc
            # because we previously resized our original image to 1/4
            up, right, down, left = up * 4, right * 4, down * 4, left * 4
            cv2.rectangle(img, (left, up), (right, down), (0, 255, 0), 2)
            cv2.rectangle(img, (left, down - 35), (right, down), (0, 255, 0), cv2.FILLED)
            # the method that the author of this library used to display the rectangle
            cv2.putText(img, name, (left + 6, down - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)


