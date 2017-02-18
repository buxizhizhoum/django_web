# coding: utf-8
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import datetime
import Queue
import time
from blog import forms
import json
from blog.models import Notes, NotesType, User, UserType, Reply, ChatContent
from django.views.decorators.cache import cache_page  # 缓存
# Create your views here.
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
# used to json serializable datetime

GLOBAL_GROUP_CHAT_DICT = {}
GLOBAL_SIZE = {}

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
            # 在User寻找用户名和密码匹配的对象个数。
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
    # print request.FILES.get("Portrait", None)
    if request.method == "POST":
        try:
            username = request.POST.get("username", None)
            password = request.POST.get("password", None)
            email = request.POST.get("email", None)
            portrait = request.FILES.get("Portrait", None)  # 获取portrait对象
            # 将头像文件上传到指定目录
            if portrait:
                portrait_name = "blog/static/portrait/%s" % portrait.name  # 获取对象名字
                print "portrait name:", portrait_name
                with open(portrait_name, 'wb') as f:
                    for chunk in portrait.chunks():
                        f.write(chunk)
            else:
                portrait_name = None
            print portrait_name
            # user_type = request.POST.get("user_type")
            # here chages the sign in logic, so all are sign in as guest
            user_type = "Guest"
            user_type_obj = UserType.objects.get(user_type=user_type)
            # 新建一个User对象
            user_obj = User.objects.create(username=username,password=password,
                                           email=email,portrait=portrait_name,
                                           user_type=user_type_obj)
            data["statues"] = 1  # 提供了这个变量，但是这里还没有用到。
            request.session["login_info"] = {"username": username, "password": password}
            return redirect("/blog/signinsuccess/")
        except Exception, e:
            print e.message
            data["message"] = e.message
            return redirect("/blog/signin/")
    else:
        return render_to_response("signin.html")

@cache_page(60*5)
def index(request):
    print request.user
    # 这里如果使用Django自带用户登录验证框架，若登录应当显示登录用户，
    # 目前由于没使用Django自带用户验证框架，所以无论登录与否都显示匿名用户。
    return render_to_response("index.html")

def notes(request):
    # get the data form database and send them to template
    # add notes whose type is Python to section Python.
    NotesType.objects.filter(notes_type="Python")
    notes_Python = Notes.objects.filter(notes_type = 1 )
    python_portrait = {}
    # 先这样写，后续优化代码。
    # 在一个类型的notes, username_id 相同的头像，可以覆盖其他的。
    # 找到每个用户对应的头像，后续尝试用两层for循环代替这样的循环。
    for note_Python in notes_Python:
        print note_Python
        username_id = note_Python.username_id
        python_portrait[username_id] = User.objects.get(id=username_id).portrait.name
        # 需要文件对象的name
    notes_Django = Notes.objects.filter(notes_type = 2)
    django_portrait = {}
    # 在一个类型的notes, username_id 相同的头像，可以覆盖其他的。
    for note_Django in notes_Django:
        print note_Django
        username_id = note_Django.username_id
        django_portrait[username_id] = User.objects.get(id=username_id).portrait.name
    notes_HTML = Notes.objects.filter(notes_type = 3)
    html_portrait = {}
    # 在一个类型的notes, username_id 相同的头像，可以覆盖其他的。
    for note_HTML in notes_HTML:
        print note_HTML
        username_id = note_HTML.username_id
        html_portrait[username_id] = User.objects.get(id=username_id).portrait.name
    notes_Javascript = Notes.objects.filter(notes_type = 4)
    javascript_portrait = {}
    # 在一个类型的notes, username_id 相同的头像，可以覆盖其他的。
    for note_Javascript in notes_Javascript:
        print note_Javascript
        username_id = note_Javascript.username_id
        javascript_portrait[username_id] = User.objects.get(id=username_id).portrait.name
    notes_jQuery = Notes.objects.filter(notes_type = 5)
    jquery_portrait = {}
    # 在一个类型的notes, username_id 相同的头像，可以覆盖其他的。
    for note_jQuery in notes_jQuery:
        print note_jQuery
        username_id = note_jQuery.username_id
        jquery_portrait[username_id] = User.objects.get(id=username_id).portrait.name
    return render_to_response("notes.html",{"notes_Python": notes_Python,
                                            "notes_Django": notes_Django,
                                            "notes_HTML": notes_HTML,
                                            "notes_Javascript": notes_Javascript,
                                            "notes_jQuery": notes_jQuery,
                                            "python_portrait": python_portrait,
                                            "django_portrait": django_portrait,
                                            "html_portrait": html_portrait,
                                            "jquery_portrait": jquery_portrait,
                                            "javascript_portrait": javascript_portrait,
                                            })
    # 对于图片对象，不能直接传数据库取到的对象，需要传名字。

def addfavor(request):
    login_statues = request.session.get("login_info", None)
    data = {"statues": 0, "favor_count": "", "message": ""}
    if login_statues:
        print login_statues
        #print login_statues['username']
        if request.method == "POST":
            try:
                # 根据id找到对应的Note，favor count 加一。
                id = request.POST.get("id")
                temp_obj = Notes.objects.get(id = id)
                temp_favor = temp_obj.favor_count + 1 # add favor count
                temp_obj.favor_count = temp_favor # update database
                temp_obj.save()
                data["favor_count"] = temp_favor # update data will be sent to ajax
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
                # 根据ajax发送的数据去查回复
                id = request.POST.get("id")
                # 每个Note对应多条回复，所以需要用filter
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
                replies = request.POST.get("replies", None)  # POST not post
                id = request.POST.get("id", None)
                # store data
                notes_obj = Notes.objects.get(id = id)
                # about the User, need to add cookies and session
                user_obj = User.objects.get(id = 1)  # 这里写死了，实际上应该获取当前用户的id
                Reply.objects.create(content = replies, notes = notes_obj, user = user_obj)
                notes_obj.reply_count += 1
                # reply能不能直接通过查询数据库获取？可以避免出错后count和数据库实际内容不一致
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
                title = request.POST.get("InputTitle", None)
                content = request.POST.get("InputNoteContent", None)
                username = request.POST.get("InputUsername", None)
                # 此处硬编码了用户
                user_obj = User.objects.get(username = "BinshanMa")
                notes_type = request.POST.get("NoteType", None)
                notes_type_obj = NotesType.objects.get(notes_type = notes_type)
                print title, content, username, notes_type
                notes_obj = Notes.objects.create(title = title, content=content,
                                                username = user_obj, notes_type = notes_type_obj)
                notes_obj.save()  # 用create是不是不用用save()? 是不用用。
                '''
                另一种方法是note_obj = Notes(title = title, content=content,username = user_obj, notes_type = notes_type_obj)
                note_obj.save()
                '''
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

# @login_required()
def chat(request):
    login_statues = request.session.get("login_info", None)
    # 此处应当完善判断，未登录应该重定向至登录页面.先略过
    username = login_statues['username']
    user_obj = User.objects.get(username = username)
    # print "user:", user_obj.friends.all()
    return render_to_response("webchat.html", {'user_obj': user_obj})


# @login_required
def sendchat(request):
    data = {"statues":0, "content": "", "user": "", "message": "","time":'', "username_to": ''}
    login_statues = request.session.get("login_info", None)
    username_from = login_statues['username']
    username_to = request.POST.get('username_to')
    print 'the request in send chat js:', request.POST
    print 'the username_to in send chat js:', username_to
    if username_from not in GLOBAL_GROUP_CHAT_DICT:
        # if there is no queue for user, create a queue.
        GLOBAL_GROUP_CHAT_DICT[username_from] = Queue.Queue()# create a queue for every user
    if username_to not in GLOBAL_GROUP_CHAT_DICT:
        GLOBAL_GROUP_CHAT_DICT[username_to] = Queue.Queue()  # create a queue for every user
    if request.method == "POST":
        try:
            content = request.POST.get('content')
            print content
            user_obj = User.objects.get(username = username_from)
            chat_obj = ChatContent.objects.create(content=content, user = user_obj)
            data["statues"] = 1
            data["content"] = content
            data['time'] = datetime.datetime.now()
            data["user"] = login_statues['username']
            data['username_to'] = username_to
            GLOBAL_GROUP_CHAT_DICT[username_to].put(data) # put chatting data to queue
        except Exception, e:
            data["statues"] = 0
            data["message"] = e.message
            return HttpResponse(e.message)
        else:
            chat_list = []
            chat_list.append(data)
            return HttpResponse(json.dumps(chat_list, cls=CJsonEncoder))
    else:
        return HttpResponse("fail")

# add judgement, get the msg of active user. something is need to distinguish where the msg comes from
def get_new_messages(request):
    if request.POST.get("username_from", None):
        # test whether there is usename in request, test one is enough
        username_from = request.POST.get("username_from")
        username_to = request.POST.get("username_to")
        print "username:", username_from, username_to
        # if username_from not in GLOBAL_GROUP_CHAT_DICT:
        #     # if there is no queue for user, create a queue.
        #     GLOBAL_GROUP_CHAT_DICT[username_from][username_to] = Queue.Queue()  # create a queue for every user
        # if username_to not in GLOBAL_GROUP_CHAT_DICT:
        #     GLOBAL_GROUP_CHAT_DICT[username_to][username_from] = Queue.Queue()  # create a queue for every user
        chat_list = []
        # have a judge if this is the first time and username_from is not in the GLOBAL_dict
        if username_from in GLOBAL_GROUP_CHAT_DICT: # from or to?
            messages_count = GLOBAL_GROUP_CHAT_DICT[username_from].qsize() # get message from queue
            print "username_from in dict", GLOBAL_GROUP_CHAT_DICT[username_from]
            # something need here, username_from will get all the messages that send to username_from
            # regard less of who send it.
        else:
            messages_count = 0
        # there is need to judge the value of messages_count, because if is 0, the program
        # will not go into the loop, and the get method of Queue will not block, the program
        # will out of control, since there is javascript function recursion(递归).
        if messages_count:
            for i in range(messages_count):
                print "message count not = 0"
                try:
                    chat_list.append(GLOBAL_GROUP_CHAT_DICT[username_from].get(timeout=60))
                except Exception, e:
                    print e.message
        else:
            print "message count = 0"
            try:
                chat_list.append(GLOBAL_GROUP_CHAT_DICT[username_from].get(timeout=60))
            except Exception, e:
                print "error"
                print e.message
        print "chat list in get new message.", chat_list
        return HttpResponse(json.dumps(chat_list, cls=CJsonEncoder))
    else:
        print "username_dict is missing..."
        return HttpResponse("username_dict is missing...")

def upload_file(request):
    # print request.POST
    # print request.FILES
    # where to get filename
    file_obj = request.FILES.get("file", None)
    if file_obj:
        # 获取文件，在前端formdata用file做名字，此时同名获取。
        file_name = "blog/static/files/%s" % file_obj.name
        receive_size = 0
        with open(file_name,"wb") as file:
            # 分块写文件
            for chunk in file_obj.chunks():
                file.write(chunk)
                receive_size += len(chunk)
                GLOBAL_SIZE = {file_obj.name, receive_size }
        print "File: %s ---uploaded successfully!" % file_obj.name
        return HttpResponse("/".join(file_name.split("/")[1:]))
    else:
        return HttpResponse("file in request is None, may be it is because it is TemporaryFile.")


# def upload_progress(request):
#     # get filename from request, look for dict and get the size of file, then send to backend
#     filename = request.GET.get("filename")
#     progress = GLOBAL_SIZE[filename]
#     print "uploading progress %s" % progress
#     return HttpResponse(progress)
