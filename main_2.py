import cv2
from deepface import DeepFace

face_classifier = cv2.CascadeClassifier()
face_classifier.load(cv2.samples.findFile(
    "C:\\Users\\ayush\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml"))


cap = cv2.VideoCapture(1)



while True:
    ret, frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(frame_gray)
    response = DeepFace.analyze(
        frame, actions=("emotion"), enforce_detection=False)
    for face in faces:
        x, y, w, h = face
        cv2.putText(frame, text=response[0].get('dominant_emotion'), org=(
            x, y), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1.0, color=(0, 255, 0))
        # new_frame = cv2.rectangle(frame, (x, y),
        #                             (x+w, y+h), color=(255, 0, 0), thickness=2)

    # rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow("frame",frame)
    
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()


