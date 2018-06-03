from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth  import authenticate, login
import datetime
import pyrebase

# Create your views here.
def index(request):

    return render(request, 'Messages/index.html')



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
    #print('The database is below')
   # print(db.get())
    #print(db.child('Chat').get())
   # messages = db.child('Chat').get()
   # key = messages.key()
    #print('Message: ', messages[key])
    #send message to firebase.
    context = {
        'Message':'You entered a message!'
    }
    context = {}
    print('Begin to check post')
    if request.method == 'POST':
        print('User message is: ', request.POST.get('enteredMessage'))
        message_sent = request.POST.get('enteredMessage')
        #Format message
        if message_sent != '' and message_sent.strip() != '':
            current_time = str(datetime.datetime.now())
            print('time: ', current_time)
            user = request.user.username
            data = {
                'User': request.user.username,
                'Time': current_time,
                'Text': message_sent
            }
            #print('Data to be pushed is: ', data)
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
            #print("database",db.child('Chat').get())
            #n_data = { datetime.datetime.now().microsecond : data}
            #print(n_data)
            #db.child('Chat').push(data)'''
            #print(messages.val())
            #key = messages.key()
            # print('Message: ', messages[key])
            # send message to firebase.
            retrieved_data = db.child('Chat')
            save_keys = []
            for j in retrieved_data.get().val():
                print('safe', j)
                save_keys.append(j)
            print('-------------')
            collectionOfData = []
            for key in save_keys:
                past_message = db.child('Chat').child(key).get()

                msgKey = past_message.key()
                msgDetails = dict(past_message.val())
                print('Sent by', msgDetails)

                userSent = msgDetails['User']
                mesText = msgDetails['Text']
                print(userSent, mesText)
                msgForm = userSent+':'+mesText+"\n"
                print('Message Key', msgKey)
                print('past', msgDetails)
                collectionOfData.append(msgForm)

            collectionOfData.append(data['User']+":"+data['Text'])

            context = {
                'TextRetrieved': collectionOfData,
            }
    return render(request, 'Messages/index.html', context)

def login(request):
    pass

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
    return render(request, 'registration/login.html')