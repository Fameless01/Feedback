import cv2
from fer import FER

# Initialize the FER model (optional: set mtcnn=True for MTCNN face detection)
detector = FER(mtcnn=True)

# Load the image or capture video from webcam
# For image:
# img = cv2.imread("path/to/your/image.jpg")  # Replace with your image path

# For webcam:
cap = cv2.VideoCapture(0)

while True:
    # Read image from webcam (for video)
    ret, frame = cap.read()

    # Detect emotions
    emotions = detector.detect_emotions(frame)

    # Draw rectangle around detected face(s) (optional)
    if emotions:
        for emotion in emotions:
            box = emotion["box"]
            cv2.rectangle(frame, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (0, 255, 0), 2)

    # Get the dominant emotion and its score
    if emotions:
        dominant_emotion, score = detector.top_emotion(emotions)
        print("Dominant Emotion:", dominant_emotion, "Score:", score)

    # Display the frame with detected emotions (optional)
    cv2.imshow("Facial Expression Detection", frame)

    # Exit on 'q' press
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources (for webcam)
cap.release()
cv2.destroyAllWindows()



# import cv2
# cap = cv2.VideoCapture(0) 

# while True:
#     ret,frame = cap.read()
#     cv2.imshow("title",frame)

#     if cv2.waitKey(1) == ord('q'):
#       break

# cap.release()
# cv2.destroyAllWindows()