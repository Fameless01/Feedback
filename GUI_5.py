import customtkinter as ctk
import pygame
import os.path
import threading
import speech_recognition as sr
import spacy
import time
import re
import csv

pygame.init()
nlp = spacy.load("en_core_web_sm")


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")



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
    pygame.mixer.music.load(thankuFilePath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)
    
    print(feedback)
    os.abort()

def thank():
    clearScreen()
    label2 = ctk.CTkLabel(root, text="Thank you !", font=('default', 25, 'bold'), text_color="Lime")
    label2.pack(anchor='center', pady=(centerTextWidth, centerTextWidth))
    threading.Thread(target=speakthanku).start()

def speakquestion5():
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
    elif response_type == "negative":
        print("User response: Negative")
        feedback.append(response_type)
    else:
        print("Unable to determine user response. default response: ",spoken_response)
        feedback.append(spoken_response)
        

    thank()

def question5():
    clearScreen()
    label2 = ctk.CTkLabel(root, text="Would you recommend today's meal to others? ", font=('default', 25, 'bold'), text_color="Lime")
    label2.pack(anchor='center', pady=(centerTextWidth, centerTextWidth))
    threading.Thread(target=speakquestion5).start()

def speakquestion4():
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
    else:
        print("Unable to determine user satisfaction level.")
        threading.Thread(target=sorrySpeak, args='4',).start()

    question5()

def question4():
    clearScreen()
    label2 = ctk.CTkLabel(root, text="On a scale from 1 to 10, how would you rate the taste and flavor of the meal? ", font=('default', 25, 'bold'), text_color="Lime")
    label2.pack(anchor='center', pady=(centerTextWidth, centerTextWidth))
    threading.Thread(target=speakquestion4).start()

def speakquestion3():
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

        elif response_type == "negative":
            print("User response: Negative")
            feedback.append(response_type)
            
        else:
            print("Unable to determine user response getting default result: ",spoken_response)
            feedback.append(spoken_response)

        question4()

def question3():
    clearScreen()
    label2 = ctk.CTkLabel(root, text="Are you satisfied with the quantity of food provided? ", font=('default', 25, 'bold'), text_color="Lime")
    label2.pack(anchor='center', pady=(centerTextWidth, centerTextWidth))
    threading.Thread(target=speakquestion3).start()

def speakquestion2():
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
    
    else:
        print("No food mentioned.")

    
    question3()

def question2():
    clearScreen()
    label2 = ctk.CTkLabel(root, text="What did you enjoy the most about today's meal?  ", font=('default', 25, 'bold'), text_color="Lime")
    label2.pack(anchor='center', pady=(centerTextWidth, centerTextWidth))
    threading.Thread(target=speakquestion2).start()
 
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
    food_keywords = ["pizza", "burger", "sushi", "pasta", "salad", "steak", "sandwich", "soup", "taco", "burrito","rice","roti","chapati","bread","samosa","momos","momo","noddles","chiken","potato","dal","daal"]
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
        positive_keywords = ["yes","indeed", "yup", "yeah", "sure", "absolutely", "definitely", "affirmative"]
        negative_keywords = ["no", "nope", "nah", "negative", "not at all"]
        
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

question1()

root.mainloop()

