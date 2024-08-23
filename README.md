Face Recognition and Attendance System
This project is a simple face recognition-based attendance system that captures and recognizes faces from a live webcam feed. When a recognized face is detected, the system logs the name and time of detection into a CSV file. This project uses the face_recognition library for face detection and encoding, OpenCV for image processing, and numpy for numerical operations.

Features
Face Registration: Automatically loads and encodes faces from a predefined folder of images (registeredImages).
Real-Time Face Recognition: Captures video from the webcam, detects faces, and matches them with registered faces.
Attendance Logging: Logs the attendance (name and time) into a CSV file (attendanceList.csv) when a face is recognized.
Prerequisites
Before running the code, ensure you have the following installed:

Python 3.x
OpenCV: pip install opencv-python
face_recognition: pip install face-recognition
numpy: pip install numpy
Project Structure
bash
Copy code
.
├── registeredImages/          # Directory containing images of registered members
├── attendanceList.csv         # CSV file where attendance records are logged
└── main.py                    # Main script to run the face recognition and attendance system
registeredImages/: This directory should contain images of all the members whose faces need to be recognized. Each image should be named with the corresponding member's name (e.g., JohnDoe.jpg).

attendanceList.csv: This file is used to store the attendance records in the format: Name,Time.

How to Run
Prepare the Environment:

Place the images of the members in the registeredImages directory. Ensure the filenames correspond to the member's name.
Run the Script:

Execute the main.py script. The script will:
Load and encode all images in the registeredImages directory.
Start capturing video from the webcam.
Detect and recognize faces in real-time.
Log attendance in the attendanceList.csv file.
bash
Copy code
python main.py
Viewing Attendance:

Open the attendanceList.csv file to see the logged attendance, which includes the name of the recognized person and the time they were detected.
Code Overview
Face Encoding
The script reads images from the registeredImages directory and encodes them using the face_recognition.face_encodings method. These encodings are stored for later comparison.

python
Copy code
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
Real-Time Face Recognition
The script captures frames from the webcam, detects faces, and compares them with the stored encodings. If a match is found, the face is labeled and attendance is marked.

python
Copy code
while True:
    success, img = cap.read()
    imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    faceInCurrentFrame = face_recognition.face_locations(imgSmall)
    encodeInCurrentFrame = face_recognition.face_encodings(imgSmall, faceInCurrentFrame)

    for encodeFace, faceloc in zip(encodeInCurrentFrame, faceInCurrentFrame):
        matches = face_recognition.compare_faces(encodeMemberFaces, encodeFace)
        faceDist = face_recognition.face_distance(encodeMemberFaces, encodeFace)

        matchIndex = np.argmin(faceDist)
        if matches[matchIndex]:
            name = members[matchIndex].upper()
            markAttendance(name)
Attendance Logging
When a face is recognized, the script checks if the person has already been logged. If not, it logs the person's name and the current time.

python
Copy code
def markAttendance(name):
    with open('attendanceList.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
Future Enhancements
Multi-Camera Support: Add support for multiple camera inputs.
GUI Implementation: Implement a graphical user interface for easier interaction.
Face Registration via Webcam: Allow new members to register their faces directly from the webcam.
