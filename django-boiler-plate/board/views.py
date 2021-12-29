from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from board.service import BoardControl
# Create your views here.

def authCheck(function):
    def wrapper(request, post_id = ''):
        if 'user_id' in request.session: # 로그인 상태
            if post_id == '': # post_id 값이 없을 때는 로그인만 체크
                return function(request)  
            else: # (업데이트, 삭제) 접속한 사람과 작성자 매치
                board = BoardControl()
                result = board.writerCheck(post_id, request.session['user_id'])
                if result: # 글 작성자와 접속한 사람이 같다.
                    return function(request, post_id)
                else: return redirect('/') # 글 작성자와 접속한 사람이 다르다.
        else: # 로그인 상태가 아니다.
            return redirect('/')
    return wrapper

def list(request):
    context = { 'page': 'list' }
    board = BoardControl()
    context['list'] = board.list({ 'start': 0, 'length': 10 })
    return render(request, 'main.html', context)

@authCheck
def post(request):
    context = { 'page': 'post' }

    if request.method == 'POST':
        board = BoardControl()
        board.insert(request)
        return redirect('/')
    return render(request, 'main.html', context)    

def read(request, post_id):
    context = { 'page': 'read' }
    board = BoardControl()
    context['contents'] =  board.read(post_id)
    return render(request, 'main.html', context)

@authCheck
def update(request, post_id):
    context = { 'page': 'update' }
    board = BoardControl()
    context['contents'] =  board.read(post_id)
    if request.method == 'POST':
        board.update(request, post_id)
        print(request.POST)
        return redirect('/board/read/' + str(post_id) + '/')
    return render(request, 'main.html', context)

@authCheck
def delete(request, post_id):
    board = BoardControl()
    board.delete(post_id)
    return redirect('/')

def ajaxList(request):
    board = BoardControl()
    
    start = request.GET.get('now', 0)
    length = request.GET.get('length', 10)

    start = (int(start) - 1) * 10 
    
    context = board.list({ 'start': start, 'length': length }) 
    count = board.list({ 'count': True }) 

    # length = limit
    # start = offset 
    return JsonResponse({ 'list': context, 'count': count[0]['count'] })