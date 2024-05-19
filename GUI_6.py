import customtkinter as ctk
import pygame
import os.path
import threading
import speech_recognition as sr
import spacy
import time
import re
import csv
import subprocess
import sys

import cv2
from mtcnn import MTCNN
from deepface import DeepFace
from collections import Counter
import os

import keyboard

import queue

pygame.init()
nlp = spacy.load("en_core_web_sm")


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


totalSatisfactionScore=0

root = ctk.CTk()
root.configure(bg="black")
centerTextHeight = (root.winfo_screenheight()*20//100)
centerTextWidth = (root.winfo_screenwidth()*20//100)
root.geometry('800x600')

# Audio files...
script_dir = os.path.dirname(__file__)
filename = "hello.mp3"
helloFilePath = os.path.join(script_dir+'\\voiceData', filename)

filename = "question2.mp3"
question2FilePath = os.path.join(script_dir+'\\voiceData', filename)

filename = "question3.mp3"
question3FilePath = os.path.join(script_dir+'\\voiceData', filename)

filename = "question4.mp3"
question4FilePath = os.path.join(script_dir+'\\voiceData', filename)

filename = "question5.mp3"
question5FilePath = os.path.join(script_dir+'\\voiceData', filename)

filename = "question6.mp3"
question6FilePath = os.path.join(script_dir+'\\voiceData', filename)

filename = "thanku.mp3"
thankuFilePath = os.path.join(script_dir+'\\voiceData', filename)

filename = "sorry.mp3"
sorryFilePath = os.path.join(script_dir+'\\voiceData', filename)

feedback=[]

global dominant_emotion


def mainCamera(): 
    global dominant_emotion
    print("\nCamera started !")
    face_detector = MTCNN()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    emotions = []

    frame_skip = 5
    frame_count = 0

    while True:
        
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        faces = face_detector.detect_faces(frame)

        for face in faces:
            x, y, w, h = face['box']
            face_region = frame[y:y+h, x:x+w]
            try:
                response = DeepFace.analyze(face_region, actions=('emotion',), enforce_detection=False)
                emotion = response[0].get('dominant_emotion')
                emotions.append(emotion)
                print(emotion)
                
            except Exception as e:
                print(f"Error in analyzing face: {e}")
        
        cv2.imshow("cam",frame)
                

    
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("\n\nCamera closed")

    emotion_counts = Counter(emotions)
    if emotion_counts:
        dominant_emotion = emotion_counts.most_common(1)[0][0]
        print("most dominant emotion:",dominant_emotion)
    else:
        dominant_emotion= 'neutrall'
    

def recognize_speech(timeout=5):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout)
            print("Recognizing...")
            spoken_text = recognizer.recognize_google(audio)
            print("You said:", spoken_text)
            return spoken_text
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return None
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            return None
        except sr.RequestError as e:
            print("Error occurred; {0}".format(e))
            return None

def clearScreen():
    for widget in root.winfo_children():
            widget.destroy()

def speakthanku():
    global totalSatisfactionScore
    pygame.mixer.music.load(thankuFilePath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)
    
    print(feedback)
    print("\n\nSatisfaction: ",str((totalSatisfactionScore*100)/10)+"%")
    os.abort()

def thank():
    clearScreen()
    label2 = ctk.CTkLabel(root, text="Thank you !", font=('default', 25, 'bold'), text_color="Lime")
    label2.pack(anchor='center', pady=(centerTextWidth, centerTextWidth))
    threading.Thread(target=speakthanku).start()

def speakquestion5():
    # global dominant_emotion
    global totalSatisfactionScore
    pygame.mixer.music.load(question6FilePath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)
    
    spoken_response = recognize_speech()
    print("Recognised text: ",spoken_response)

    response_type = extract_sentiment(spoken_response,'5')
    if response_type == "positive":
        print("User response: Positive")
        feedback.append(response_type)
        totalSatisfactionScore+=3
    elif response_type == "negative":
        print("User response: Negative")
        feedback.append(response_type)
        totalSatisfactionScore-=2
    else:
        print("Unable to determine user response. default response: ",spoken_response)
        feedback.append(spoken_response)
        

    keyboard.press_and_release('q')
    thank()

def question5():
    clearScreen()
    print("Would you recommend today's meal to others? ")
    label2 = ctk.CTkLabel(root, text="Would you recommend today's meal to others? ", font=('default', 25, 'bold'), text_color="Lime")
    label2.pack(anchor='center', pady=(centerTextWidth, centerTextWidth))
    threading.Thread(target=speakquestion5).start()

def speakquestion4():
    global totalSatisfactionScore
    pygame.mixer.music.load(question4FilePath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)
    
    spoken_response = recognize_speech()

    print("Recognized text: ",spoken_response)

    if spoken_response is None:
        threading.Thread(target=sorrySpeak, args='4',).start()

    print("Recognised Text:", spoken_response)
    satisfaction_level = extract_satisfaction_level(spoken_response)
    if satisfaction_level:
        print("User satisfaction level:", satisfaction_level)
        feedback.append(satisfaction_level)
        totalSatisfactionScore+=(satisfaction_level/2)
    else:
        print("Unable to determine user satisfaction level.")
        threading.Thread(target=sorrySpeak, args='4',).start()

    question5()

def question4():
    clearScreen()
    print("On a scale from 1 to 10, how would you rate the taste and flavor of the meal?")
    label2 = ctk.CTkLabel(root, text="On a scale from 1 to 10, how would you rate the taste and flavor of the meal? ", font=('default', 25, 'bold'), text_color="Lime")
    label2.pack(anchor='center', pady=(centerTextWidth, centerTextWidth))
    threading.Thread(target=speakquestion4).start()

def speakquestion3():
    global totalSatisfactionScore
    pygame.mixer.music.load(question3FilePath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)
    
    spoken_response = recognize_speech()

    print("Recognized Text: ",spoken_response)

    if spoken_response==None:
        threading.Thread(target=sorrySpeak, args='3',).start()

    else:

        response_type = extract_sentiment(spoken_response,'3')

        if response_type == "positive":
            print("User response: Positive")
            feedback.append(response_type)
            totalSatisfactionScore+=1

        elif response_type == "negative":
            print("User response: Negative")
            feedback.append(response_type)
            totalSatisfactionScore-=1
            
        else:
            print("Unable to determine user response getting default result: ",spoken_response)
            feedback.append(spoken_response)

        question4()

def question3():
    clearScreen()
    print("Are you satisfied with the quantity of food provided? ")
    label2 = ctk.CTkLabel(root, text="Are you satisfied with the quantity of food provided? ", font=('default', 25, 'bold'), text_color="Lime")
    label2.pack(anchor='center', pady=(centerTextWidth, centerTextWidth))
    threading.Thread(target=speakquestion3).start()

def speakquestion2():
    global totalSatisfactionScore
    pygame.mixer.music.load(question2FilePath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)
    
    spoken_response = recognize_speech()

    if spoken_response is None:
        threading.Thread(target=sorrySpeak, args='2',).start()

    print("Recognized text: ",spoken_response)

    food_names = extract_food_names(spoken_response)

    if food_names:
        enjoyedFood= ", ".join(food_names)
        feedback.append(enjoyedFood)
        totalSatisfactionScore+=1
    
    else:
        print("No food mentioned.")
        totalSatisfactionScore-=1

    
    question3()

def question2():
    clearScreen()

    

    print("What did you enjoy the most about today's meal?  ")
    label2 = ctk.CTkLabel(root, text="What did you enjoy the most about today's meal?  ", font=('default', 25, 'bold'), text_color="Lime")
    label2.pack(anchor='center', pady=(centerTextWidth, centerTextWidth))
    threading.Thread(target=speakquestion2).start()
 
def getEmotion():
    recognized_emotion = subprocess.check_output([sys.executable, 'main_4.py']).decode().strip()
    print("Emotion:",recognized_emotion)
    if recognized_emotion=="happy":
        facial_satisfaction=1
    
    elif recognized_emotion=="neutral":
        facial_satisfaction=0.5
    
    else:
        facial_satisfaction=0
    
    print("\nFacial satisfaction: ",str(facial_satisfaction*100/1)+"%")
    return str(facial_satisfaction)+"%"

def speakquestion1():

    pygame.mixer.music.load(helloFilePath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)

    spoken_response = recognize_speech()

    if spoken_response is None:
        threading.Thread(target=sorrySpeak, args='1',).start()

    doc = nlp(spoken_response)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            userName=ent.text
            break

    print("User name: ",userName)
    feedback.append(userName)
    
    question2()

def question1():
    clearScreen()
    
    print("Hello sir, What is your name? ")
    
    label2 = ctk.CTkLabel(root, text="Hello sir, What is your name? ", font=('default', 25, 'bold'), text_color="Lime")
    label2.pack(anchor='center', pady=(centerTextWidth, centerTextWidth))
    threading.Thread(target=speakquestion1).start()

def sorrySpeak(callFun):
    pygame.mixer.music.load(sorryFilePath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)
    
    time.sleep(5)

    if callFun=='1':
        return question1()

    elif callFun=='2':
        return question2()

    elif callFun=='3':
        return question3()

    elif callFun=='4':
        return question4()

    elif callFun=='5':
        return question5()

def extract_food_names(text):
    food_keywords = [
    "pizza", "burger", "sushi", "pasta", "salad", "steak", "sandwich", "soup", "taco", "burrito",
    "rice", "roti", "chapati", "bread", "samosa", "momos", "momo", "noodles", "chicken", "potato",
    "dal", "daal", "spaghetti", "lasagna", "fried chicken", "fish and chips", "hot dog", "grilled cheese",
    "quesadilla", "nachos", "pad thai", "pho", "spring rolls", "dumplings", "curry", "kebabs", "biryani",
    "shawarma", "falafel", "hummus", "pita bread", "tabbouleh", "goulash", "paella", "risotto", "polenta",
    "bruschetta", "tiramisu", "cheesecake", "ice cream", "brownies", "cupcakes", "donuts", "waffles",
    "pancakes", "crepes", "muffins", "bagels", "croissants", "biscuits", "granola", "oatmeal", "cereal",
    "smoothie", "yogurt", "fruit salad", "caesar salad", "greek salad", "coleslaw", "mashed potatoes",
    "french fries", "hash browns", "baked beans", "chili", "meatloaf", "lamb chops", "roast beef",
    "barbecue ribs", "pork chops", "meatballs", "sushi roll", "sashimi", "tempura", "miso soup",
    "teriyaki chicken", "fried rice", "stir fry", "egg roll", "beef stroganoff", "shepherd's pie",
    "chicken tikka masala", "paneer butter masala", "chole bhature", "aloo gobi", "palak paneer",
    "gulab jamun", "jalebi", "pecan pie", "apple pie", "chocolate cake"
]
    text = text.lower()
    found_food = [food for food in food_keywords if food in text]
    return found_food

def extract_sentiment(text,funNo):

    if text==None and funNo=='3':
        threading.Thread(target=sorrySpeak, args='3',).start()
    
    elif text==None and funNo=='5':
        threading.Thread(target=sorrySpeak, args='5',).start()
    
    else:
        text = text.lower()
        positive_keywords = [
    "yes", "indeed", "yup", "yeah", "sure", "absolutely", "definitely", "affirmative",
    "certainly", "of course", "right", "positively", "naturally", "sure thing", "you bet",
    "undoubtedly", "without a doubt", "for sure", "exactly", "true", "correct", "yep",
    "roger that", "got it", "sounds good", "all right", "fine", "okay", "ok", "alright",
    "agreed", "indeed", "totally", "aye", "very well", "gladly", "with pleasure", "by all means",
    "good", "I agree", "I concur", "that's right", "affirmed", "that's correct", "you got it",
    "affirmatively", "amen", "precisely", "right on", "so true", "just so", "amen to that",
    "right you are", "that's so", "verily", "def", "surely", "indubitably", "unquestionably",
    "decidedly", "beyond a doubt", "beyond question", "no doubt", "indeedy", "roger", "aye aye",
    "yessir", "yes ma'am", "yup yup", "abso-freaking-lutely", "hell yes", "heck yeah", "you know it",
    "all day", "affirmatory", "why not", "without question", "right away", "on it", "as you say",
    "sure as shootin'", "damn straight", "betcha", "no problem", "for a fact", "for real",
    "straight up", "righto", "you know", "uh-huh", "thumbs up", "yis", "yeppers", "yo",
    "positive", "most definitely", "for certain", "agreed"
]
        negative_keywords = [
    "no", "nope", "nah", "negative", "not at all", "never", "absolutely not", "definitely not",
    "no way", "not really", "I don't think so", "not in a million years", "by no means", 
    "certainly not", "under no circumstances", "no chance", "no way in hell", "nuh-uh", 
    "nay", "nope nope", "not happening", "forget it", "nothing doing", "no sir", "no ma'am",
    "not on your life", "out of the question", "no dice", "no thanks", "not gonna happen", 
    "no can do", "not a chance", "never ever", "no siree", "nope never", "not ever", 
    "not in this lifetime", "nope nope nope", "nope not at all", "hell no", "heck no", 
    "not by a long shot", "no shot", "fat chance", "nope not really", "not by any means",
    "nope not today", "nah not really", "nope not now", "definitely no", "absolutely no",
    "never in a million years", "not under any circumstances", "not even close", "nope never ever",
    "no way José", "nope no way", "nope not ever", "nope no how", "nope nuh-uh", "not a bit",
    "nope not at all"
]
        
        for keyword in positive_keywords:
            if keyword in text:
                return "positive"
        
        for keyword in negative_keywords:
            if keyword in text:
                return "negative"
        return text

def extract_satisfaction_level(text):
    pattern = r'\b(?:10|[1-9])\b'
    match = re.search(pattern, text)
    
    if match:
        return int(match.group())
    else:
        return None



thread= threading.Thread(target=mainCamera).start()




print("\n\nLoading modules and process !\n\n")
time.sleep(8)

question1()

root.mainloop()

