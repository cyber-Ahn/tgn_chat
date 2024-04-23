import pyttsx3
import speech_recognition as sr
import os
import openai

tgnSettings = "xx"
openai_api_key = "xx"
speakname = "xx"
language = "xx"
error = "xx"
speak = "xx"
over = "xx"
sh_trigger = "xx"
sh_over = "xx"
#-------only tgn_smart_home----------
b1 = ""
b2 = ""
b3 = ""
b4 = ""
b5 = ""
b6 = ""
b7 = ""
b8 = ""
b9 = ""
buttons = []

def ini():
    global tgnSettings
    global openai_api_key
    global speakname
    global language
    global error
    global speak
    global over
    global sh_trigger
    global sh_over
    try:
        f_d = open("/home/pi/tgn_chat/system.config","r")
        for line in f_d:
            if "tgnSettings" in line:
                tgnSettings = line.rstrip().split("_")[1]
            if "openaiApiKey" in line:
                openai_api_key = line.rstrip().split("_")[1]
            if "speakname" in line:
                speakname = line.rstrip().split("_")[1]
            if "language" in line:
                language = line.rstrip().split("_")[1]
            if "error" in line:
                error = line.rstrip().split("_")[1]
            if "speak" in line:
                speak = line.rstrip().split("_")[1]
            if "over" in line:
                over = line.rstrip().split("_")[1]
    except IOError:
        print("File not found !")
    if tgnSettings == "On":
        print("Load from tgn_smart_home")
        import time
        import paho.mqtt.client as mqtt
        from tgnLIB import get_ip
        try:
            f_d = open("/home/pi/tgn_smart_home/config/system.config","r")
            for line in f_d:
                if "XopenaiApiKeyX" in line:
                    openai_api_key = line.rstrip().split("_")[1]
        except IOError:
            print("File not found !")
        client = mqtt.Client("TGN Smart Home")
        client.connect(get_ip())
        client.on_message= on_message
        client.loop_start()
        client.subscribe([("tgn/#",0)])
        time.sleep(1)
        client.loop_stop()
        spr_phat="/home/pi/tgn_smart_home/language/"+language+"/"
        try:
            f_a = open(spr_phat+"voice.lang","r")
            x = 0
            for line in f_a:
                x=x+1
                if x == 27:
                    speakname = line.rstrip()
                if x == 28:
                    error = line.rstrip()
                if x == 29:
                    speak = line.rstrip()
                if x == 30:
                    over = line.rstrip()
                if x == 31:
                    sh_trigger = line.rstrip()
                if x == 32:
                    sh_over = line.rstrip()
        except IOError:
            print("File not found !")
    speakname = speakname.lower()
    openai.api_key = openai_api_key

def on_message(client, userdata, message):
    global language
    global b1
    global b2
    global b3
    global b4
    global b5
    global b6
    global b7
    global b8
    global b9
    if message.topic == "tgn/language":
        language=(message.payload.decode("utf-8"))
    if message.topic == "tgn/buttons/name/1":
        b1=(message.payload.decode("utf-8").split("_")[1].lower())
    if message.topic == "tgn/buttons/name/2":
        b2=(message.payload.decode("utf-8").split("_")[1].lower())
    if message.topic == "tgn/buttons/name/3":
        b3=(message.payload.decode("utf-8").split("_")[1].lower())
    if message.topic == "tgn/buttons/name/4":
        b4=(message.payload.decode("utf-8").split("_")[1].lower())
    if message.topic == "tgn/buttons/name/5":
        b5=(message.payload.decode("utf-8").split("_")[1].lower())
    if message.topic == "tgn/buttons/name/6":
        b6=(message.payload.decode("utf-8").split("_")[1].lower())
    if message.topic == "tgn/buttons/name/7":
        b7=(message.payload.decode("utf-8").split("_")[1].lower())
    if message.topic == "tgn/buttons/name/8":
        b8=(message.payload.decode("utf-8").split("_")[1].lower())
    if message.topic == "tgn/buttons/name/9":
        b9=(message.payload.decode("utf-8").split("_")[1].lower())

def TextToSpeech(tx,ln):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for x in range(len(voices)):
        da = str(voices[x]).split("languages=")[1].split("gender=")[0]
        if ln == "en":
            ln = "en-us"
        if ln in da:
            engine.setProperty('voice', voices[x].id)
            engine.say(tx)
            engine.runAndWait()

ini()
buttons.append(b1); buttons.append(b2); buttons.append(b3); buttons.append(b4); buttons.append(b5); buttons.append(b6); buttons.append(b7); buttons.append(b8); buttons.append(b9)
r = sr.Recognizer()
while True:
    with sr.Microphone() as source:
        print(speak)
        os.system('mpg321 beep.mp3 &')
        audio_text = r.listen(source)
        print(over)
    recognized_text = r.recognize_google(audio_text, language=language)
    if speakname in recognized_text:
        recognized_text = recognized_text.replace(speakname+" ", "")
        if "play" in recognized_text:
            import pywhatkit
            song = recognized_text.replace("play", "")
            pywhatkit.playonyt(song)
        elif sh_trigger in recognized_text and tgnSettings == "On":
            recognized_text = recognized_text.replace(sh_trigger + " ", "")
            print("smart home:" + recognized_text)
            TextToSpeech(sh_over,language)
            cach = recognized_text.split(" ")
            op = "x"
            if cach[1] == "off" or cach[1] == "0":
                op = "0"
            elif cach[1] == "on" or cach[1] == "1":
                op = "1"
            op_num = "0"
            if cach[0] in buttons:
                op_num = str(buttons.index(cach[0])+1)
                client = mqtt.Client("voic_bridge")
                client.connect(get_ip())
                topic = "tgn/buttons/status/"+op_num
                client.publish(topic,op,qos=0,retain=True)
        else:
            print("chatGPT:"+recognized_text)
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=recognized_text,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )
            TextToSpeech(response["choices"][0]["text"],language)

    else:
        TextToSpeech(error,language)
    break                 
