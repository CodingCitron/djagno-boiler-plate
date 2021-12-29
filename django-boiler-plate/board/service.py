from datetime import datetime
from django.db import connection
from board.util import changeToObject

class BoardControl:
    def __init__(self) : pass
    def insert(self, request):
        user_id = request.session['user_id']
        category = '기본 게시판'
        title = request.POST.get('title', '')
        about = request.POST.get('about', '')

        query = 'insert into "board"(category, title, contents, writer, register_date) values(%s, %s, %s, %s, now())'
        with connection.cursor() as cursor:
            cursor.execute(query, [category, title, about, user_id])
            connection.commit()

    def list(self, option):
        if 'start' in option: start = option['start']
        if 'length' in option: length = option['length']
        piece = [
            '"post_id", "title", "writer", "register_date"', 
            '', 
            'order by register_date desc, post_id desc limit {0} offset {1}'
            ]
            
        category = ''

        cursor = connection.cursor()
        if 'category' in option:
            piece[1] = "where category = '{2}'"
            category = option['category']

        if 'count' in option:
            piece[0] = 'count(post_id)' 
            piece[2] = ''
            start = ''
            length = ''
    
        query = 'select ' + piece[0] + 'from "board" ' + piece[1] + piece[2]
        print(query)
        cursor.execute(query.format(length, start, category))
        list = cursor.fetchall()
        object = changeToObject(list, cursor)
        return object

    def writerCheck(self, post_id, user_id):
        query = 'select writer from "board" where post_id = {0}'
        cursor = connection.cursor()
        cursor.execute(query.format(post_id))
        list = cursor.fetchone()
        if list is not None:
            if list[0] == user_id:
                return True
        return False

    def read(self, post_id):
        query = 'select * from "board" where post_id = {0}'
        cursor = connection.cursor()
        cursor.execute(query.format(post_id))
        list = cursor.fetchone()
        object = changeToObject([list], cursor)
        object[0]['register_date'] = object[0]['register_date'].strftime('%Y.%m.%d, %H:%M:%S')
        return object[0]

    def update(self, request, post_id):
        title = request.POST.get('title', '')
        about = request.POST.get('about', '')

        query = "update board set title = '{1}', contents = '{2}' where post_id = '{0}'"
        cursor = connection.cursor()
        cursor.execute(query.format(post_id, title, about))
        connection.commit()

    def delete(self, post_id):
        query = "delete from board where post_id = {0}"
        cursor = connection.cursor()
        cursor.execute(query.format(post_id))
        connection.commit()

    def __del__(self):
        connection.close()