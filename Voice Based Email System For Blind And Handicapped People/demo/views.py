from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render, redirect,reverse
from django.http import JsonResponse
import imaplib,email
import re
import os
import difflib
import speech_recognition as sr
import smtplib
import pyttsx3
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView # FOR CLASS BAESD VIEW WE NEED
from playsound import playsound
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
###########

#######


passwrd = ""
addr = ""

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
imap_url = 'imap.gmail.com'
conn = imaplib.IMAP4_SSL(imap_url)


def TextToSpeech(cmd,speech_rate):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate',speech_rate)
    engine.say(cmd)
    engine.runAndWait()

def speechtotext(duration1,action):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        TextToSpeech("speak",180)
        print("listening.."+ action)
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source, phrase_time_limit=duration1)
    try:
        response=r.recognize_google(audio)
        #command1=command1.lower()

            #if "sophie" in command1:
             #   return command1
    except:
        response='None'
    return response

def convert_special_char(text):
    temp=text
    special_chars = ['dot','underscore','dollar','hashh','star','plus','minus','space','dash','attherate','add','incom']
    for character in special_chars:
        while(True):
            pos=temp.find(character)
            if pos == -1:
                break
            else :
                if character == 'dot':
                    temp=temp.replace('dot','.')
                elif character == 'underscore':
                    temp=temp.replace('underscore','_')
                elif character == 'dollar':
                    temp=temp.replace('dollar','$')
                elif character == 'hashh':
                    temp=temp.replace('hashh','#')
                elif character == 'star':
                    temp=temp.replace('star','*')
                elif character == 'plus':
                    temp=temp.replace('plus','+')
                elif character == 'minus':
                    temp=temp.replace('minus','-')
                elif character == 'space':
                    temp = temp.replace('space', '')
                elif character == 'dash':
                    temp=temp.replace('dash','-')
                elif character == 'attherate':
                    temp=temp.replace('attherate','@')
                elif character == 'add':
                    temp = temp.replace('add', '@')
                elif character == 'incom':
                    temp = temp.replace('incom', 'com')

    return temp


strings=['khizarbagwan86@gmaiL.com','devidas.jaybhay@.net','aniketbali7@gmail.com','projectblind3@gmail.com','savita.adhav@.net','akashshendge2@gmail.com']

"""
def emails(strings,substring):
	for string in strings:
		if substring in string:
			name = string
			return name

	return substring"""
#_________________________________READMAIL PART____________________________________________


def home(request):
    if request.method == 'POST':
       """say= speechtotext(5,"start")
       print(say)
       if say=='start' or say=='yes' or say=='search':
           return JsonResponse({'result' : 'success'})
"""
    return render(request,'home.html')


def login(request):
    global i, addr, passwrd
    if request.method == 'POST':
        text1 = "Welcome to our Voice Based Email Portal. Login with your email account to continue. "
        TextToSpeech(text1, 180)
        flag = True
        while (flag):
            TextToSpeech("Enter your Email", 180)
            addr =speechtotext(8,'email. bhai.')
            #addr = 'projectblind123@gmail.com'
            """
            addr = difflib.get_close_matches(addr, strings)
            addr=str(addr[0])
            """
            pas=difflib.get_close_matches(addr, strings)
            try:
                addr=str(pas[0])
            except:
                addr = addr
            addr = addr.strip()
            addr = addr.replace(' ', '')
            addr = addr.lower()
            addr = convert_special_char(addr)
            print(addr)
            if addr != 'N':
                TextToSpeech("You meant " + addr + " say yes to confirm or no to enter again", 180)
                #say='yes'
                say = speechtotext(3, "yes or no")
                if say == 'yes' or say == 'Yes':
                    flag = False
            else:
                TextToSpeech("could not understand what you meant:", 180)

        flag = True
        while (flag):
            TextToSpeech("Enter your password", 180)
            passwrd = speechtotext(10, "enter password")


            if addr != 'N':
                TextToSpeech("You meant " + passwrd + " say yes to confirm or no to enter again", 180)
                #say = 'yes'
                say = speechtotext(3, 'yes r no')
                if say == 'yes' or say == 'Yes':
                    flag = False
            else:
                TextToSpeech("could not understand what you meant:", 180)

        passwrd = passwrd.strip()
        passwrd = passwrd.replace(' ', '')
        passwrd = passwrd.lower()
        passwrd = convert_special_char(passwrd)
        print(passwrd)
        imap_url = 'imap.gmail.com'
        conn = imaplib.IMAP4_SSL(imap_url)
        try:
            conn.login(addr, passwrd)
            s.login(addr, passwrd)
            TextToSpeech("Congratulations. You have logged in successfully. You will now be redirected to options page.", 180)
            return JsonResponse({'result': 'success'})
        except:
            TextToSpeech("Invalid Login Details. Please try again.", 180)
            return JsonResponse({'result': 'failure'})

    return render(request,'login.html', context={})


def menu(request):#1>>options
    global i, addr, passwrd
    if request.method == 'POST':
        flag = True
        TextToSpeech("You are logged into your account. What would you like to do ?", 180)
        while (flag):
            TextToSpeech("To compose an email say compose.\
                         To open Inbox folder say Inbox. \
                         To open Sent folder say Sent.\
                          To open Trash folder say Trash.\
                          To Logout say Logout.Do you want me to repeat?",180)
            #say ='no'
            say=   speechtotext(3, "option choose")
            if say == 'No' or say == 'no':
	            flag = False
	            print(say)

        TextToSpeech("Enter your desired action", 180)
        act = speechtotext(5, "action")
        #act='compose'
        act = act.lower()
        print(act)
        if act == 'compose':
            TextToSpeech(" You will now be redirected to the compose page.", 180)
            return JsonResponse({'result': 'compose'})
        elif act == 'inbox':
            TextToSpeech(" You will now be redirected to the inbox page.", 180)
            return JsonResponse({'result': 'inbox'})
        elif act == 'sent' or act == 'send':
            TextToSpeech(" You will now be redirected to the sent page.", 180)
            return JsonResponse({'result': 'sent'})
        elif act == 'trash':
            TextToSpeech(" You will now be redirected to the trash page.", 180)
            return JsonResponse({'result': 'trash'})
        elif act == 'logout':
            addr = ""
            passwrd = ""
            TextToSpeech("You have been logged out of your account and now will be redirected back to the login page",180)
            return JsonResponse({'result': 'logout'})
        else:
            TextToSpeech("Invalid action. Please try again.", 180)
            return JsonResponse({'result': 'failure'})

    return render(request, 'menu.html')



###########################################3

def compose(request):
    global i, addr, passwrd, s
    if request.method == "POST":
        text1 = "You have reached the page where you can compose and send an email. "
        TextToSpeech(text1, 130)
        flag = True
        flag1 = True

        fromaddr = addr
        toaddr = list()
        while flag1:
            while flag:
                TextToSpeech("enter receiver's email address:", 180)
                to = speechtotext(12, 'recepient emaail.')
                to = to.strip()
                to = to.replace(' ', '')
                to = to.lower()
                to = convert_special_char(to)
                """
                to = difflib.get_close_matches(to, strings)
                to = str(to[0])
                """
                recepient_email = difflib.get_close_matches(to, strings)
                try:
                    to = str(recepient_email[0])
                except:
                    to = to
                if to != 'None':
                    print(to)
                    TextToSpeech("You meant " + to + " say yes to confirm or no to enter again", 180)
                    say=speechtotext(5,"yes or no")
                    #say='yes'
                    if say == 'yes' or say == 'Yes':
                        toaddr.append(to)
                        flag = False
                else:
                    TextToSpeech("could not understand what you meant", 180)

            TextToSpeech("Do you want to enter more recipients ?  Say yes or no.", 180)

            say1 = speechtotext(3, "no or yes")
            #say1='no'
            if say1 == 'No' or say1 == 'no':
                flag1 = False
            flag = True

        newtoaddr = list()
        for item in toaddr:
            item = item.strip()
            item = item.replace(' ', '')
            item = item.lower()
            item = convert_special_char(item)
            newtoaddr.append(item)

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ",".join(newtoaddr)
        flag = True
        while (flag):
            TextToSpeech("Enter subject", 180)

            subject = speechtotext(10, "subject")
            if subject == 'None':
                TextToSpeech("could not understand what you meant", 180)

            else:
                flag = False
        msg['Subject'] = subject
        flag = True
        while flag:
            TextToSpeech("enter body of the mail", 180)
            body = speechtotext(30, "body of the mail")
            print(body)
            if body == 'None':
                TextToSpeech("could not understand what you meant", 180)
            else:
                flag = False

        msg.attach(MIMEText(body, 'plain'))
        TextToSpeech("any attachment? say yes or no", 180)
        x = speechtotext(4, "yes or no ")
        x = x.lower()
        if x == 'yes':
            TextToSpeech("Do you want to record an audio and send as an attachment?", 180)
            say = speechtotext(4, "record say yes or no")
            say = say.lower()
            if say == 'yes' or say == 'YES':
                TextToSpeech("Enter filename.", 180)
                filename = speechtotext(5, "filenae")
                filename = filename.lower()
                filename = filename + '.mp3'
                filename = filename.replace(' ', '')
                print(filename)
                TextToSpeech("Enter your audio message.", 180)
                audio_msg = speechtotext(10, "audio to record")
                flagconf = True
                while flagconf:
                    try:
                        tts = gTTS(text=audio_msg, lang='en', slow=False)
                        tts.save(filename)
                        flagconf = False
                    except:
                        print('Trying again')
                attachment = open(filename, "rb")
                p = MIMEBase('application', 'octet-stream')
                p.set_payload((attachment).read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                msg.attach(p)
            elif say == 'no':
                TextToSpeech("Enter filename with extension", 180)
                filename = speechtotext(5, "filename ")
                attachment = open(filename, "rb")
                p = MIMEBase('application', 'octet-stream')
                p.set_payload((attachment).read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                msg.attach(p)
        try:
            s.sendmail(fromaddr, newtoaddr, msg.as_string())
            TextToSpeech("Your email has been sent successfully. You will now be redirected to the options page.", 180)

        except:
            TextToSpeech("Sorry, your email failed to send. please try again. You will now be redirected to the the compose page again.",180)
            return JsonResponse({'result': 'failure'})
        s.quit()
        return JsonResponse({'result': 'success'})
    return render(request, 'compose.html')


######################################
'''def compose(request):
    if request.method == 'POST':
        TextToSpeech("say back to back to manu",180)
        say=speechtotext(3,"say back")
        if say=='back' or say == 'BACK':
            print(say)
            return JsonResponse({'result': 'back'})
    return render(request,'compose.html')


'''
######################

def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)
#########################

def get_attachment(msg):
    global i
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        if bool(filename):
            filepath = os.path.join(attachment_dir, filename)
            with open(filepath, "wb") as f:
                f.write(part.get_payload(decode=True))
                TextToSpeech("Attachment has been downloaded",180)
                path = 'C:/Users/Shaibaz/Desktop/khizar dont delete very important/recorder'
                files = os.listdir(path)
                paths = [os.path.join(path, basename) for basename in files]
                file_name = max(paths, key=os.path.getctime)
            with open(file_name, "rb") as f:
                if file_name.find('.jpg') != -1:
                    TextToSpeech("attachment is an image.",180)
                if file_name.find('.png') != -1:
                    TextToSpeech("attachment is an image.",180)
                if file_name.find('.mp3') != -1:
                    TextToSpeech("Playing the downloaded audio file.",180)
                    playsound(file_name)
#####################

def reply_mail(msg_id, message):
    global i, s
    TO_ADDRESS = message['From']
    FROM_ADDRESS = addr
    msg = email.mime.multipart.MIMEMultipart()
    msg['to'] = TO_ADDRESS
    msg['from'] = FROM_ADDRESS
    msg['subject'] = message['Subject']
    msg.add_header('In-Reply-To', msg_id)
    flag = True
    while (flag):

        TextToSpeech("enter body of mail", 180)
        body = speechtotext(20, 'body')
        print(body)
        try:
            msg.attach(MIMEText(body, 'plain'))
            s.sendmail(msg['from'], msg['to'], msg.as_string())
            TextToSpeech("Your reply has been sent successfully.", 180)
            flag = False
        except:
            TextToSpeech("Your reply could not be sent. Do you want to try again? Say yes or no.", 180)
            act = speechtotext(3)
            act = act.lower()
            if act != 'yes':
                flag = False
#############################

def frwd_mail(item, message):
    global i,s
    flag1 = True
    flag = True
    global i
    newtoaddr = list()
    while flag:
        while flag1:
            while True:
                TextToSpeech("Enter receiver's email address",180)
                to = speechtotext(12, 'recepient emaail.')
                to = to.strip()
                to = to.replace(' ', '')
                to = to.lower()
                to = convert_special_char(to)

                """
                to = difflib.get_close_matches(to, strings)
                to = str(to[0])
                """
                pas = difflib.get_close_matches(to, strings)
                try:
                    to = str(pas[0])
                except:
                    to = to
                TextToSpeech("You meant " + to + " say yes to confirm or no to enter again",180)
                yn = speechtotext(3,"yes")
                yn = yn.lower()
                if yn == 'yes':
                    to = to.strip()
                    to = to.replace(' ', '')
                    to = to.lower()
                    to = convert_special_char(to)
                    print(to)
                    newtoaddr.append(to)
                    break
            TextToSpeech("Do you want to add more recepients?",180)
            ans1 = speechtotext(3,'yes or no')
            ans1 = ans1.lower()
            print(ans1)
            if ans1 == "no" :
                flag1 = False

        message['From'] = addr
        message['To'] = ",".join(newtoaddr)
        try:
            s.sendmail(addr, newtoaddr, message.as_string())
            TextToSpeech("Your mail has been forwarded successfully.",180)
            flag = False
        except:
            TextToSpeech("Your mail could not be forwarded. Do you want to try again? Say yes or no.",180)
            act = speechtotext(3,'yes or no')
            act = act.lower()
            if act != 'yes':
                flag = False
###############################
#read_mails()
def read_mails(mail_list,folder):
    global s, i
    mail_list.reverse()
    mail_count = 0
    to_read_list = list()
    for item in mail_list:
        result, email_data = conn.fetch(item, '(RFC822)')
        raw_email = email_data[0][1].decode()
        message = email.message_from_string(raw_email)
        To = message['To']
        From = message['From']
        Subject = message['Subject']
        Msg_id = message['Message-ID']
        TextToSpeech("Email number " + str(mail_count + 1) + "    .The mail is from you to " + str(To) + "  . The subject of the mail is " + str(Subject),180)
        print('message id= ', Msg_id)
        print('From :', From)
        print('To :', To)
        print('Subject :', Subject)
        print("\n")
        to_read_list.append(Msg_id)
        mail_count = mail_count + 1

    flag = True
    while flag :
        n = 0
        flag1 = True
        while flag1:
            TextToSpeech("Enter the email number of mail you want to read.",180)
            n = speechtotext(3,'yes or no')
            print(n)
            TextToSpeech("You meant " + str(n) + ". Say yes or no.",180)
            say = speechtotext(3,'yes or no')
            say = say.lower()
            if say == 'yes':
                flag1 = False
        n = int(n)
        msgid = to_read_list[n - 1]
        print("message id is =", msgid)
        typ, data = conn.search(None, '(HEADER Message-ID "%s")' % msgid)
        data = data[0]
        result, email_data = conn.fetch(data, '(RFC822)')
        raw_email = email_data[0][1].decode()
        message = email.message_from_string(raw_email)
        To = message['To']
        From = message['From']
        Subject = message['Subject']
        Msg_id = message['Message-ID']
        print('From :', From)
        print('To :', To)
        print('Subject :', Subject)
        TextToSpeech("The mail is from " + From + " to " + To + "  . The subject of the mail is " + Subject,180)
        Body = get_body(message)
        Body = Body.decode()
        Body = re.sub('<.*?>', '', Body)
        Body = os.linesep.join([s for s in Body.splitlines() if s])
        if Body != '':
            TextToSpeech(Body,180)
        else:
            TextToSpeech("body is Empty sir",180)
        get_attachment(message)

        if folder == 'inbox':
            TextToSpeech("Do you want to reply to this mail? Say yes or no. ",180)
            ans = speechtotext(3,'yes or no')
            ans = ans.lower()
            print(ans)
            if ans == "yes":
                reply_mail(Msg_id, message)

        if folder == 'inbox' or folder == 'sent':
            TextToSpeech("Do you want to forward this mail to anyone? Say yes or no. ",180)
            ans = speechtotext(3,'yes or no')
            ans = ans.lower()
            print(ans)
            if ans == "yes":
                frwd_mail(Msg_id, message)

        if folder == 'inbox' or folder == 'sent':
            TextToSpeech("Do you want to delete this mail? Say yes or no. ",180)
            ans = speechtotext(3,'yes or no')
            ans = ans.lower()
            print(ans)
            if ans == "yes":
                try:
                    conn.store(data, '+X-GM-LABELS', '\\Trash')
                    conn.expunge()
                    TextToSpeech("The mail has been deleted successfully.",180)
                    print("mail deleted")
                except:
                    TextToSpeech("Sorry, could not delete this mail. Please try again later.",180)

        if folder == 'trash':
            TextToSpeech("Do you want to delete this mail? Say yes or no. ",180)
            ans = speechtotext(3,'yes or no')
            ans = ans.lower()
            print(ans)
            if ans == "yes":
                try:
                    conn.store(data, '+FLAGS', '\\Deleted')
                    conn.expunge()
                    TextToSpeech("The mail has been deleted permanently.",180)
                    print("mail deleted")
                except:
                    TextToSpeech("Sorry, could not delete this mail. Please try again later.",180)

        TextToSpeech("Email ends here",180)

        TextToSpeech("Do you want to read more mails?",180)
        ans = speechtotext(3,'yes or no')
        ans = ans.lower()
        if ans == "no":
            flag = False

###SEARCH SPECIFIC Mail
def search_specific_mail(folder,key,value,foldername):
    global i, conn
    conn.select(folder)
    result, data = conn.search(None,key,'"{}"'.format(value))
    mail_list=data[0].split()
    if len(mail_list) != 0:
        TextToSpeech("There are " + str(len(mail_list)) + " emails with this email ID.",180)
    if len(mail_list) == 0:
        TextToSpeech("There are no emails with this email ID.",180)
    else:
        read_mails(mail_list,foldername)

#################################
def inbox(request):
    global i, addr, passwrd, conn
    if request.method =='POST':

        imap_url = 'imap.gmail.com'
        conn = imaplib.IMAP4_SSL(imap_url)
        conn.login(addr, passwrd)
        conn.select('"INBOX"')
        result, data = conn.search(None, '(UNSEEN)')
        unread_list = data[0].split()
        no = len(unread_list)
        result1, data1 = conn.search(None, "ALL")
        mail_list = data1[0].split()
        text = "You have reached your inbox. There are " + str(len(mail_list)) + " total mails in your inbox. You have " + str(no) + " unread emails" + ". To read the unread emails say unread. To search a specific email say search. To go back to the options page say back. To logout say logout."
        TextToSpeech(text, 180)
        flag = True
        while (flag):
            act = speechtotext(5, "unread")
            act = act.lower()
            print(act)
            if act == 'unread':
                flag = False
                if no != 0:
                    read_mails(unread_list, 'inbox')
                else:
                    TextToSpeech("You have no unread emails.", 180)

            elif act == 'search':
                flag = False
                emailid = ""
                while True:
                    TextToSpeech("Enter email ID of the person who's email you want to search.", 180)
                    to = speechtotext(12, 'emaail id .')
                    to = to.strip()
                    to = to.replace(' ', '')
                    to = to.lower()
                    to = convert_special_char(to)
                    """
                    to = difflib.get_close_matches(to, strings)
                    to = str(to[0])
                    """
                    pas = difflib.get_close_matches(to, strings)
                    try:
                        to = str(pas[0])
                    except:
                        to = to

                    emailid = to
                    TextToSpeech("You meant " + emailid + " say yes to confirm or no to enter again", 180)

                    yn = speechtotext(5, "yes or no")
                    yn = yn.lower()
                    if yn == 'yes':
                        break
                search_specific_mail('INBOX', 'FROM', emailid,'inbox')

            elif act == 'back':
                TextToSpeech("You will now be redirected to the options page.", 180)
                conn.logout()
                return JsonResponse({'result': 'success'})

            elif act == 'logout' or act =='log out':
                addr = ""
                passwrd = ""
                TextToSpeech("You have been logged out of your account and now will be redirected back to the login page.", 180)
                return JsonResponse({'result': 'logout'})

            else:
                TextToSpeech("Invalid action. Please try again.", 180)

            TextToSpeech("If you wish to do anything else in the inbox or logout of your mail say yes or else say no.",180)

            ans = speechtotext(3, "hai")
            ans = ans.lower()
            if ans == 'yes':
                flag = True
                TextToSpeech("Enter your desired action. Say unread, search, back or logout. ", 180)

        TextToSpeech("You will now be redirected to the options page.", 180)
        conn.logout()
        return JsonResponse({'result': 'success'})

    return render(request,'Inbox.html')



###################################

def sent(request):
    global i, addr, passwrd, conn
    if request.method == 'POST':
        imap_url = 'imap.gmail.com'
        conn = imaplib.IMAP4_SSL(imap_url)

        conn.login(addr, passwrd)
        conn.select('"[Gmail]/Sent Mail"')
        result1, data1 = conn.search(None, "ALL")
        mail_list = data1[0].split()
        text = "You have reached your sent mails folder. You have " + str(len(mail_list)) + " mails in your sent mails folder. To search a specific email say search. To go back to the options page say back. To logout say logout."
        TextToSpeech(text,180)
        flag = True
        while (flag):
            act = speechtotext(5,'search,read')
            act = act.lower()
            print(act)
            if act == 'search':
                flag = False
                emailid = ""
                while True:
                    TextToSpeech("Enter email ID of receiver.",180)
                    to = speechtotext(12, 'recepient emaail.')
                    to = to.strip()
                    to = to.replace(' ', '')
                    to = to.lower()
                    to = convert_special_char(to)

                    """
                    to = difflib.get_close_matches(to, strings)
                    to = str(to[0])
                    """
                    pas = difflib.get_close_matches(to, strings)
                    try:
                        to = str(pas[0])
                    except:
                        to = to

                    emailid = to
                    TextToSpeech("You meant " + emailid + " say yes to confirm or no to enter again",180)
                    yn = speechtotext(5,'yes or no')
                    yn = yn.lower()
                    if yn == 'yes':
                        break
                search_specific_mail('"[Gmail]/Sent Mail"', 'TO', emailid,'sent')

            elif act == 'back':
                TextToSpeech("You will now be redirected to the options page.",180)
                conn.logout()
                return JsonResponse({'result': 'success'})

            elif act == 'logout':
                addr = ""
                passwrd = ""
                TextToSpeech("You have been logged out of your account and now will be redirected back to the login page.",180)
                return JsonResponse({'result': 'logout'})

            else:
                TextToSpeech("Invalid action. Please try again.",180)

            TextToSpeech("If you wish to do anything else in the sent mails folder or logout of your mail say yes or else say no.",180)
            ans = speechtotext(3,'yes or no')
            ans = ans.lower()
            if ans == 'yes':
                flag = True
                TextToSpeech("Enter your desired action. Say search, back or logout. ",180)
        TextToSpeech("You will now be redirected to the options page.",180)
        conn.logout()
        return JsonResponse({'result': 'success'})

    elif request.method == 'GET':
        return render(request, 'sent.html')
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def trash(request):
    global i, addr, passwrd, conn
    if request.method == 'POST':
        imap_url = 'imap.gmail.com'
        conn = imaplib.IMAP4_SSL(imap_url)


        conn.login(addr, passwrd)
        conn.select('"[Gmail]/Bin"')
        result1, data1 = conn.search(None, "ALL")
        mail_list = data1[0].split()
        text = "You have reached your trash folder. You have " + str(len(mail_list)) + " mails in your trash folder. To search a specific email say search. To go back to the options page say back. To logout say logout."
        TextToSpeech(text,180)
        flag = True
        while (flag):
            act = speechtotext(5,'yes or no')
            act = act.lower()
            print(act)
            if act == 'search':
                flag = False
                emailid = ""
                while True:
                    TextToSpeech("Enter email ID of sender.",180)
                    to = speechtotext(12, 'recepient emaail.')
                    to = to.strip()
                    to = to.replace(' ', '')
                    to = to.lower()
                    to = convert_special_char(to)
                    """
                    to = difflib.get_close_matches(to, strings)
                    to = str(to[0])
                    """
                    pas = difflib.get_close_matches(to, strings)
                    try:
                        to = str(pas[0])
                    except:
                        to = to

                    emailid = to
                    print(emailid)
                    TextToSpeech("You meant " + emailid + " say yes to confirm or no to enter again",180)
                    yn = speechtotext(5,'yes or no')
                    yn = yn.lower()
                    if yn == 'yes':
                        break

                search_specific_mail('"[Gmail]/Bin"', 'FROM', emailid, 'trash')

            elif act == 'back':
                TextToSpeech("You will now be redirected to the options page.",180)
                conn.logout()
                return JsonResponse({'result': 'success'})

            elif act == 'logout':
                addr = ""
                passwrd = ""
                TextToSpeech("You have been logged out of your account and now will be redirected back to the login page.",180)
                return JsonResponse({'result': 'logout'})

            else:
                TextToSpeech("Invalid action. Please try again.",180)

            TextToSpeech("If you wish to do anything else in the trash folder or logout of your mail say Yes or else say No.",180)
            ans = speechtotext(3,'yes or no')
            ans = ans.lower()
            print(ans)
            if ans == 'yes':
                flag = True
                TextToSpeech("Enter your desired action. Say search, back or logout. ",180)

        TextToSpeech("You will now be redirected to the options page.",180)
        conn.logout()
        return JsonResponse({'result': 'success'})
    elif request.method == 'GET':
        return render(request, 'trash.html')



def instructions(request):
	return render(request,'Instructions.html')

def sample(request):
    bet = {}
    if request.method =='POST':
        TextToSpeech("say your username",180)
        username=speechtotext(5,'username')
        print(username)

        TextToSpeech("say your password",180)
        password=speechtotext(5,'email')
        print(password)
        bet.update({'username':username})

        bet.update({'eamil':email})

    return render(request,'sample.html',context=bet)