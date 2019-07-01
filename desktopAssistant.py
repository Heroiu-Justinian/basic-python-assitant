from gtts import gTTS
from mpg123 import Mpg123, Out123
import speech_recognition as sr
import os
import re
import webbrowser
import smtplib
import requests
from weather import Weather

def talkToMe(audioString):
    "speaks audio passed as argument"

    # print(audio)
    # for line in audio.splitlines():
    #     os.system(audio)

    # use the system's inbuilt say command instead of mpg123
    # text_to_speech = gTTS(text=audio, lang='en')
    # text_to_speech.save('audio.mp3')
    # os.system('mpg123 audio.mp3')
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    os.system("Mpg123 audio.mp3")


def myCommand():
    "listens for commands"

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Ready...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = myCommand();

    return command


def assistant(command):
    "if statements for executing commands"

    if 'AFIS' in command:
        talkToMe('Hello!My name is AFIS wich stands for Another Fucking Intelligent System and I am a personal voice assistant')
    elif ' open reddit' in command:
        reg_ex = re.search('open reddit(.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        print('Done!')

    elif 'open website' in command:
        talkToMe("opening website right now")
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            print('Done!')
        else:
            pass
    elif 'youtube search ' in command:
        # talkToMe("searching on youtube")
        reg_ex = re.search('youtube search (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.youtube.com/results?search_query=' + domain
            webbrowser.open(url)
            print('Done')
    elif 'facebook search' in command:
        reg_ex = re.search('facebook search (.+)' , command)
        if reg_ex:
            personToSearch = reg_ex.group(1)
            url = 'https://www.facebook.com/search/top/?q=' + personToSearch + '&epa=SEARCH_BOX'
            webbrowser.open(url)
            print("Done!")
    elif 'what\'s up' in command:
        talkToMe('Just doing my thing')
    elif 'joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
        if res.status_code == requests.codes:
            talkToMe(str(res.json()['joke']))
        else:
            talkToMe('oops!I ran out of jokes')
    elif 'get this bread' in command:
        url = 'https://www.youtube.com/watch?v=rY0WxgSXdEE'
        webbrowser.open(url)
    elif 'bodies' in command:
        url = 'https://www.youtube.com/watch?v=04F4xlWSFh0'
        webbrowser.open(url)
    elif 'message' in command:
        url = 'https://web.whatsapp.com/'
        webbrowser.open(url)
    elif 'manage tasks':
        os.system('start taskmgr')
    elif 'email' in command:
        talkToMe('Who is the recipient?')
        recipient = myCommand()

        if 'John' in recipient:
            talkToMe('What should I say?')
            content = myCommand()

            #init gmail SMTP
            mail = smtplib.SMTP('smtp.gmail.com', 587)

            #identify to server
            mail.ehlo()

            #encrypt session
            mail.starttls()

            #login
            mail.login('username', 'password')

            #send message
            mail.sendmail('John Fisher', 'JARVIS2.0@protonmail.com', content)

            #end mail connection
            mail.close()

            talkToMe('Email sent.')
        
        else:
            talkToMe('I don\'t know what you mean!')


talkToMe('I am ready for your command')

#loop to continue executing multiple commands
while True:
    assistant(myCommand())