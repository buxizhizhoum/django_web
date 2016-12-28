# coding: utf-8
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from blog import forms
import json
from blog.models import Notes, NotesType, User, UserType, Reply, ChatContent
# Create your views here.
def login_0(request):
    if request.method == 'POST':
        form = forms.UserInfo(request.POST)
        if form.is_valid():
            form_clean_data = form.cleaned_data
            # get username and password form database and verification,
            # just think that username
            # in the database is Jerry and password is sb
            username = 'jerry'
            password = 'sb'
            if form_clean_data['username'] == username and \
                            form_clean_data['password'] == password:
                return render_to_response('index.html')
        else:
            return redirect('/blog/login/')
    else:
        return render_to_response('login_v1.html', {'form': forms.UserInfo()})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        if remember_me:
            # something could be done here according to the value of remember_me.
            print 'remember asked!'
        if User.objects.filter(username=username, password=password).count() == 1:
            request.session["login_info"] = {"username": username, "password": password}
            return render_to_response('index.html')
        else:
            return redirect('/blog/login/')
    else:
        return render_to_response('login.html', {'error': 'Wrong!'})

def logout(request):
    del request.session["login_info"]
    return HttpResponse("Logged out.")

def signin(request):
    data = {"statues": 0, "message": ""}
    if request.method == "POST":
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            email = request.POST.get("email")
            # user_type = request.POST.get("user_type")
            # here chages the sign in logic, so all are sign in as guest
            user_type = "Guest"
            user_type_obj = UserType.objects.get(user_type=user_type)
            user_obj = User.objects.create(username=username,password=password,
                                           email=email,user_type=user_type_obj)
            data["statues"] = 1
            request.session["login_info"] = {"username": username, "password": password}
            return redirect("/blog/signinsuccess/")
        except Exception, e:
            print e.message
            data["message"] = e.message
            return redirect("/blog/signin/")
    else:
        return render_to_response("signin.html")

def index(request):
        return render_to_response("index.html")

def notes(request):
    # get the data form database and send them to template
    # add notes whose type is Python to section Python.
    NotesType.objects.filter(notes_type="Python")
    notes_Python = Notes.objects.filter(notes_type = 1 )
    notes_Django = Notes.objects.filter(notes_type = 2)
    notes_HTML = Notes.objects.filter(notes_type = 3)
    notes_Javascript = Notes.objects.filter(notes_type = 4)
    notes_jQuery = Notes.objects.filter(notes_type = 5)
    return render_to_response("notes.html",{"notes_Python": notes_Python,
                                            "notes_Django": notes_Django,
                                            "notes_HTML": notes_HTML,
                                            "notes_Javascript": notes_Javascript,
                                            "notes_jQuery": notes_jQuery})

def addfavor(request):
    login_statues = request.session.get("login_info", None)
    data = {"statues": 0, "favor_count": "", "message": ""}
    if login_statues:
        print login_statues
        #print login_statues['username']
        if request.method == "POST":
            try:
                id = request.POST.get("id")
                temp_obj = Notes.objects.get(id = id)
                temp_favor = temp_obj.favor_count + 1 # add favor count
                temp_obj.favor_count = temp_favor # update database
                temp_obj.save()
                data["favor_count"] = temp_favor # update data send to ajax
                data["statues"] = 1 # update statues to 1
            except Exception, e:
                data["message"] = e.message
        else:
            data["message"] = "error request method"
        return HttpResponse(json.dumps(data))
    else:
        return redirect("/blog/login/")

def getreply(request):
    login_statues = request.session.get("login_info", None)
    data = {"statues":0, "reply_count":'', "replies": '', "message": ''}
    if login_statues:
        if request.method == "POST":
            try:
                id = request.POST.get("id")
                temp_reply_obj = Reply.objects.filter(notes_id = id).order_by("-id").values("content","user__username")
                temp_notes_obj = Notes.objects.get(id = id)
                replies = list(temp_reply_obj)
                reply_count = temp_notes_obj.reply_count
                data["replies"] = replies
                data["reply_count"] = reply_count
                data["statues"] = 1
            except Exception, e:
                data["message"] = e.message
        return HttpResponse(json.dumps(data))
    else:
        return redirect("/blog/login/")

def submitreply(request):
    login_statues = request.session.get("login_info", None)
    if login_statues:
        data = {"statues": 0, "message":"", "replies": "", "username": ""}
        if request.method == "POST":
            try:
                # data from javascript
                replies = request.POST.get("replies")  # POST not post
                id = request.POST.get("id")
                # store data
                notes_obj = Notes.objects.get(id = id)
                # about the User, need to add cookies and session
                user_obj = User.objects.get(id = 1)
                Reply.objects.create(content = replies, notes = notes_obj, user = user_obj)
                notes_obj.reply_count += 1
                notes_obj.save()
                # change the value of data dict
                data["statues"] = 1
                data["replies"] = replies
                data["username"] = user_obj.username
            except Exception , e:
                data["message"] = e.message
        return HttpResponse(json.dumps(data))
    else:
        return redirect("/blog/login/")

def addnote(request):
    login_statues = request.session.get("login_info", None)
    data = {"statues":0, "message":""}
    if login_statues:
        if request.method == "POST":
            # deal with the data and redirect to success pages
            try:
                title = request.POST.get("InputTitle")
                content = request.POST.get("InputNoteContent")
                username = request.POST.get("InputUsername")
                user_obj = User.objects.get(username = "BinshanMa")
                notes_type = request.POST.get("NoteType")
                notes_type_obj = NotesType.objects.get(notes_type = notes_type)
                print title, content, username, notes_type
                notes_obj = Notes.objects.create(title = title, content=content,
                                                username = user_obj, notes_type = notes_type_obj)
                notes_obj.save()
                data["statues"] = 1
                # if there is no mistake, redirect to a new page
                return redirect("/blog/addnotesuccess/")
            except Exception, e:
                data["message"] = e.message
                print e.message
                # if there is error, redirect to addnote ,
                # here might need changes to keep the content that user input
                return redirect("/blog/addnote/")
        else:
            return render_to_response("addnote.html")
    else:
        return redirect("/blog/login/")

def addnotesuccess(request):
    # add interval and redirect the pages to notes after a certain time
    return render_to_response("addnotesuccess.html")

def signinsuccess(request):
    return render_to_response("signinsuccess.html")

def chat(request):
    return render_to_response("webchat.html")

def sendchat(request):
    data = {"statues":0, "content": "", "user": "", "message": ""}
    login_statues = request.session.get("login_info", None)
    if request.method == "POST":
        try:
            content = request.POST.get("content")
            user_obj = User.objects.get(id=1)
            chat_obj = ChatContent.objects.create(content=content, user = user_obj)
            data["statues"] = 1
            data["content"] = content
            data["user"] = login_statues['username']
        except Exception, e:
            data["message"] = e.message
            return HttpResponse("error")
        else:
            return HttpResponse(json.dumps(data))
    else:
        return HttpResponse("fail")

