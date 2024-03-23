import cv2
import os
import customtkinter as ck
import threading
import PIL.Image, PIL.ImageTk

ck.set_appearance_mode("System")  # Modes: system (default), light, dark
ck.set_default_color_theme("blue")

root = ck.CTk()
root.geometry('800x600')

frame = ck.CTkFrame(master=root, fg_color="white")
frame.pack(expand=True, fill="both")

# Create a Label widget to display the camera feed
camera_label = ck.CTkLabel(master=frame, text=None)
camera_label.place(x=600,y=300)

start_button = ck.CTkButton(
    master=frame, text="Start Camera", command=lambda: start_camera(start_button))
start_button.pack()

def camera():
    from deepface import DeepFace
    face_classifier = cv2.CascadeClassifier()
    face_classifier.load(cv2.samples.findFile(
        "/home/fameless/my_venv/lib/python3.11/site-packages/cv2/data/haarcascade_frontalface_default.xml"))
    cap = cv2.VideoCapture(0)
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
            new_frame = cv2.rectangle(frame, (x, y),
                                       (x+w, y+h), color=(255, 0, 0), thickness=2)
        # Convert the frame to RGB format
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convert the frame to a Tkinter-compatible photo image
        img = PIL.Image.fromarray(rgb_frame)
        imgtk = PIL.ImageTk.PhotoImage(image=img)
        # Update the camera label with the new image
        camera_label.imgtk = imgtk
        camera_label.configure(image=imgtk)
        camera_label.update()
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


def start_camera(button):
    button.pack_forget()  # Hide the start button
    thread = threading.Thread(target=camera)
    thread.start()

root.mainloop()
