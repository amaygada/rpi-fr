from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from rest_framework import status
from .serializers import *
import cv2
import numpy as np
from scipy import stats
import os
import json
import datetime
import pytz

# Create your views here.

haar_classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
try:
    model = cv2.face.LBPHFaceRecognizer_create() #creating the model for LBPH
    model.read('lbph_model_trained.xml')
except:
    model = "None"

class PersonView(APIView):

    #Adds Person in DB, performs HAAR Cascade on image, saves face for recognition
    def post(self, request):  
        name = request.data["name"]
        email = request.data["email"]
        ims = []
        for i in request.data.keys():
            if i=="name" or i=="email":
                pass
            else:
                ims.append(request.data[i])

        faces = []
        for i in range(len(ims)):
            ims[i] = cv2.cvtColor(cv2.imdecode(np.fromstring(ims[i].read(), np.uint8), cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2GRAY)
            ims[i] = detect_face_HAAR(ims[i], 1.05)
            if type(ims[i])==dict:
                faces.append(ims[i]['im'])

        if len(faces)>0:
            try:
                os.mkdir("train/"+email)
            except:
                pass
            
            cnt = 0
            for i in faces:
                cv2.imwrite("train/"+email+"/"+str(cnt)+".jpg", i)
                cnt+=1
            
            person_serializer = PersonSerializer(data={"Name": name, "Email":email, "Label":-1})
            if person_serializer.is_valid():
                person_serializer.save()
                return Response(data={"val": "Success"}, status=status.HTTP_200_OK)
            return Response(data={"val": "error", "error": person_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"val": "Face not found"}, status=status.HTTP_200_OK)

    def get(self, reauest):
        faces = []
        labels = []
        path = "train/"
        label_str = os.listdir(path)
        label_count = 1
        for s in label_str:
            path_new = path + str(s) + "/"
            folders = os.listdir(path_new)
            for folder in folders:
                image = cv2.imread(path_new+folder)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces.append(image)
                labels.append(label_count)
                # print(label_count, s)
            person = Person.objects.filter(Email=s)[0]
            person.Label=label_count
            person.save(update_fields=["Label"])
            label_count+=1
        
        if len(faces)!=0:
            model = cv2.face.LBPHFaceRecognizer_create()
            model.train(np.array(faces),np.array(labels))
            model.write('lbph_model_trained.xml')
            return(Response(data={"val": "Success. Model Training complete."}, status=status.HTTP_200_OK))
        else:
            return(Response(data={"val": "Success. No images found to train."}, status=status.HTTP_400_BAD_REQUEST))


    def put(self, request):
        if model=="None":
            return Response({"val": "Trained model not found"}, status=status.HTTP_400_BAD_REQUEST)
        im = request.data["image"]
        img = cv2.cvtColor(cv2.imdecode(np.fromstring(im.read(), np.uint8), cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2GRAY)
        face = detect_face_HAAR(img, 1.05)

        if type(face)==dict:
            im = face['im'] #extracting face
            pred_list = []
            for i in range(5):
                result = model.predict(im)
                # print(result)
                if result[1]<80:
                    pred_list.append(result[0])
            modeVal = stats.mode(pred_list)[0][0]
            result = Person.objects.filter(Label=modeVal)[0]

            asz = AttendanceSerializer(data={"PersonID": str(modeVal), "Timestamp": datetime.datetime.now(pytz.timezone('Asia/Kolkata'))})
            if asz.is_valid():
                asz.save()
            else:
                return Response({"val": "Error", "error": asz.errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"val": "Success", "result": {"name": result.Name, "email": result.Email}}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"val": "Face Not Found"}, status=status.HTTP_400_BAD_REQUEST)


class AttendanceView(APIView):
    
    def post(self, request):
        query = json.load(request)
        results = Attendance.objects.all()

        date = query["date"]

        if date != "":
            y = int(date[0:4])
            m = date_preprocess(date[5:7])
            d = date_preprocess(date[8:])
            results = results.filter(Timestamp__gte=datetime.datetime(day=d, month=m, year=y, minute=0, hour=0, second=1))
            results = results.filter(Timestamp__lte=datetime.datetime(day=d, month=m, year=y, minute=59, hour=23, second=59))
        
        ll = []
        id_ = 1
        for i in results:
            o = {}
            p = Person.objects.filter(Label=i.PersonID)[0]
            o["id"] = id_
            o["name"] = p.Name
            o["email"] = p.Email
            o["time"] = i.Timestamp.strftime("%H:%M:%S")
            ll.append(o)
            id_+=1
        
        return Response({"val": "Success", "data": ll}, status=status.HTTP_200_OK)


def date_preprocess(x):
    if x[0] == '':
        return int(x[1])
    return int(x)

def detect_face_HAAR(image , scaleFactor):
    face = haar_classifier.detectMultiScale(image, scaleFactor=scaleFactor, minNeighbors=7)
    if len(face)==0:
        return image
    else:
        (x,y,w,h) = face[0]
        dictionary_facedetect = {
            'dim' : face[0],
            'im' : image[y:y+w, x:x+h]
        }
        return dictionary_facedetect