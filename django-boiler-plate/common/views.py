from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from common.service import Authentication
from board.service import BoardControl

# Create your views here.

def loggedIn(function):
    def wrapper(request):
        if 'user_id' in request.session:
            return function(request)
        redirect('/')
    return wrapper

def notLoggedIn(function):
    def wrapper(request):
        if 'user_id' in request.session:
            return redirect('/')
        return function(request)
    return wrapper

def home(request):
    context = {}
    board = BoardControl()
    context['list'] = board.list({ 'start': 0, 'length': 10 })
    return render(request, 'main.html', context)

@notLoggedIn
def login(request):
    context = {}
    if request.method == 'POST' :
        auth = Authentication(request)
        result = auth.login()
        context = { 'message': result['message'] }

        if result['pass']:
            request.session['user_id'] = result['user_id']
            request.session['user_name'] = result['user_name']
            return redirect('/')
    return render(request, 'common/login.html', context)

@notLoggedIn
def register(request):
    context = {}
    if request.method == 'POST' :
        auth = Authentication(request)
        result = auth.register()

        context = { 'message': result['message'] }
        if result['pass']:
            return redirect('/user/login/')
    return render(request, 'common/register.html', context)

@loggedIn
def logout(request):
    request.session.flush()
    return redirect('/')

@loggedIn
def mypage(request):
    context = {}
    auth = Authentication(request)
    context['result'] = auth.getMemberInfo(request.session['user_id'])
    return render(request, 'common/mypage.html', context)

@loggedIn
def editProfile(request):
    context = {}
    auth = Authentication(request)
    context['result'] = auth.getMemberInfo(request.session['user_id'])

    if request.method == 'POST':
        auth = Authentication(request)
        auth.updateProfile(request.session['user_id'])
        return redirect('/user/mypage/')

    return render(request, 'common/editProfile.html', context)

@loggedIn
def deleteMember(request):
    auth = Authentication(request)
    auth.deleteMember(request.session['user_id'])
    request.session.flush()
    return redirect('/')

@notLoggedIn
def findIdPwd(request):
    context = {}
    
    if request.method == 'POST':
        auth = Authentication(request)
        result = auth.temporaryPassword()
        return JsonResponse({ 'result': result })

    return render(request, 'common/findIdPwd.html', context)
