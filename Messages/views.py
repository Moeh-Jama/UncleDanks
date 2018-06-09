from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth  import authenticate, login
from django.contrib.auth.models import User

from django.http import HttpResponse



import datetime
import pyrebase
full_user = ""
iterations = -10

# Create your views here.
def index(request):
    config = {
        "apiKey": "AIzaSyCLKnXHfD4mqCifYwA9Fm8PCiXaNZqDtkA",
        "authDomain": "moehsmessagingapp.firebaseapp.com",
        "databaseURL": "https://moehsmessagingapp.firebaseio.com",
        "projectId": "moehsmessagingapp",
        "storageBucket": "moehsmessagingapp.appspot.com",
        "messagingSenderId": "529929215823"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    # print('The database is below')
    # print(db.get())
    # print("database",db.child('Chat').get())
    # n_data = { datetime.datetime.now().microsecond : data}
    retrieved_data = db.child('Chat')
    save_keys = []
    for j in retrieved_data.get().val():
        save_keys.append(j)
    collectionOfData = {}
    i = 0
    for key in save_keys[iterations:]:
        past_message = db.child('Chat').child(key).get()

        msgKey = past_message.key()
        msgDetails = dict(past_message.val())
        print('Sent by', msgDetails)

        userSent = msgDetails['User']
        mesText = msgDetails['Text']
        print(userSent, mesText)
        msgForm = userSent + ':' + mesText + "\n"
        print('Message Key', msgKey)
        print('past', msgDetails)
        collectionOfData[i] = {userSent: mesText}
        i += 1
    users = User.objects.all()
    context = {
        "TextRetrieved": collectionOfData,
        "UserList": users,
    }
    return render(request, 'Messages/index.html', context)



def sendMessage(request):
    config = {
        "apiKey": "AIzaSyCLKnXHfD4mqCifYwA9Fm8PCiXaNZqDtkA",
        "authDomain": "moehsmessagingapp.firebaseapp.com",
        "databaseURL": "https://moehsmessagingapp.firebaseio.com",
        "projectId": "moehsmessagingapp",
        "storageBucket": "moehsmessagingapp.appspot.com",
        "messagingSenderId": "529929215823"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    context = {
        'Message':'You entered a message!'
    }
    context = {}
    print('Begin to check post')
    if request.method == 'POST':
        message_sent = request.POST.get('enteredMessage')
        #Format message
        if message_sent != '' and message_sent.strip() != '':
            #current time
            current_time = str(datetime.datetime.now())
            #print('time: ', current_time)
            user = request.user.username
            data = {
                'User': request.user.username,
                'Time': current_time,
                'Text': message_sent
            }
            db.child('Chat').push(data)
            retrieved_data = db.child("Chat")
            save_keys = []
            count =0
            for j in retrieved_data.get().val():
                save_keys.append(j)
                count+=1
            collectionOfData = {}
            i = 0
            #get the last 10 messages
            for key in save_keys[iterations:]:
                past_message = db.child('Chat').child(key).get()

                msgKey = past_message.key()
                msgDetails = dict(past_message.val())
                #print('Sent by', msgDetails)

                userSent = msgDetails['User']
                mesText = msgDetails['Text']
                msgForm = userSent+':'+mesText+"\n"
                collectionOfData[i]= {userSent : mesText}
                i+=1

            context = {
                "TextRetrieved": collectionOfData,
            }
            redirect('index')
    return render(request, 'Messages/index.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            password
            user = authenticate(username=username, password=password)
            login(request, user)
            redirect('index')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)

def login(request):
    iterations = -10
    return render(request, 'registration/login.html')

def view_detail(request):
    if request.method == "POST":
        search_word = request.POST['data']
        iterations -=10

def directMessaging(request):
    name = None
    
    if request.method == 'GET':
        name = request.GET['UserEntry']
    print('USERNAME IS ', str(name))
    full_user = name
    context = {
        "other_user": full_user,
    }
    config = {
        "apiKey": "AIzaSyCLKnXHfD4mqCifYwA9Fm8PCiXaNZqDtkA",
        "authDomain": "moehsmessagingapp.firebaseapp.com",
        "databaseURL": "https://moehsmessagingapp.firebaseio.com",
        "projectId": "moehsmessagingapp",
        "storageBucket": "moehsmessagingapp.appspot.com",
        "messagingSenderId": "529929215823"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    ifContains = False
    chatName = ""
    for j in  db.child('private_Messages').get().val():
        if j == request.user.username+"_"+name:
            ifContains = True
        elif j == name+ "_"+request.user.username:
            ifContains = True
    if not ifContains:
        chatName = request.user.username+"_"+name
    else:
        # print('The database is below')
        # print(db.get())
        # print("database",db.child('Chat').get())
        # n_data = { datetime.datetime.now().microsecond : data}
        retrieved_data = db.child('private_Messages').child(chatName)
        save_keys = []

        s = 0
        for j in retrieved_data.get().val():
            save_keys.append(j)
            s+=1
        collectionOfData = {}
        i = 0

        if s>0:
            for key in save_keys:
                past_message = db.child('private_Messages').child(chatName).child(key).get()

                msgKey = past_message.key()
                msgDetails = dict(past_message.val())
                print('Sent by', msgDetails)
                print(msgDetails)
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                print(chatName)
                userSent = ''
                if 'User' in msgDetails:
                    userSent = msgDetails['User']
                mesText = ''
                if 'Text' in msgDetails:
                    mesText = msgDetails['Text']
                print(userSent, mesText)
                msgForm = userSent + ':' + mesText + "\n"
                print('Message Key', msgKey)
                print('past', msgDetails)
                collectionOfData[i] = {userSent: mesText}
                i += 1
            users = User.objects.all()
            print(collectionOfData)
            context = {
                "TextRetrieved": collectionOfData,
                "UserList": users,
                "other_user": name,
                "afterGuy": "Mark Whalburg",
            }
    
    #return HttpResponse('<p>Hello World</p>')
    return render(request, 'Messages/directMessaging.html', context)

def sendDirect(request):
    current_user = request.user.username
    config = {
        "apiKey": "AIzaSyCLKnXHfD4mqCifYwA9Fm8PCiXaNZqDtkA",
        "authDomain": "moehsmessagingapp.firebaseapp.com",
        "databaseURL": "https://moehsmessagingapp.firebaseio.com",
        "projectId": "moehsmessagingapp",
        "storageBucket": "moehsmessagingapp.appspot.com",
        "messagingSenderId": "529929215823"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    context = {
        'Message':'You entered a message!'
    }
    context = {}
    print('Begin to check post')
    if request.method == 'POST':
        message_sent = request.POST.get('enteredMessage')
        print('01')
        print('Other guy: ', request.POST.get('other_user'))
        other_user  = request.POST.get('other_user')
        context = {
            'other_user': other_user
        }
        #Format message
        if message_sent != '' and message_sent.strip() != '':
            #current time
            current_time = str(datetime.datetime.now())
            #print('time: ', current_time)
            user = request.user.username
            data = {
                'User': request.user.username,
                'Time': current_time,
                'Text': message_sent
            }
            new_Contact = True
            chatName = ''
            for j in db.child('private_Messages').get().val():
                print('USERS: ', current_user+"_"+other_user)
                if j == current_user+"_"+other_user:
                    new_Contact = False
                    chatName = current_user+"_"+other_user
                elif j == other_user+"_"+current_user:
                    new_Contact = False
                    chatName = other_user+"_"+current_user

            if new_Contact:
                #make the new chat here.
                chatName = current_user+"_"+other_user
                new_Chat = {
                            'User': current_user,
                            'Time': current_time,
                            'Text': message_sent
                        }
                db.child('private_Messages').child(chatName).push(data)
            else:
                collectionOfData = {} 
                save_keys = []
                for j in db.child('private_Messages').child(chatName).get().val():
                    save_keys.append(j)
                i = 0
                for key in save_keys:
                    past_message = db.child('private_Messages').child(chatName).child(key).get()
                    msgKey = past_message.key()
                    msgDetails = dict(past_message.val())
                    #print('Sent by', msgDetails)

                    userSent = msgDetails['User']
                    mesText = msgDetails['Text']
                    msgForm = userSent+':'+mesText+"\n"
                    collectionOfData[i]= {userSent : mesText}
                    i+=1
                collections[i] = {current_user: message_sent}
                context = {
                    "TextRetrieved": collectionOfData,
                    "other_user": other_user
                }
                db.child('private_Messages').child(chatName).push(data)
    return render(request, 'Messages/directMessaging.html', context)

