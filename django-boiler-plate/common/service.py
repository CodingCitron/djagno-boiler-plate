from django.db import connection
from django.shortcuts import render
from board.util import changeToObject
from board.util import randomPwd
import bcrypt

class Authentication:
    def __init__(self, request):
        self.request = request
        self.id = request.POST.get('user_id', '')
        self.pwd = request.POST.get('user_pwd', '')
        self.pwd_confirm = request.POST.get('user_pwd_confirm', '')
        self.name = request.POST.get('user_name', '')
        self.email = request.POST.get('user_email', '')
        self.option = ''

    def compareId(self):
        query = 'select count(user_id) from "user" where user_id = %s'
        with connection.cursor() as cursor:
            cursor.execute(query, [self.id])
            num = cursor.fetchone()
            return num[0]

    def verify(self):
        if 'user_id' in self.request.session:
            return render(self.request, 'common/main.html', { 'message': '로그인 상태입니다.' })
        
        result = { 'pass': False, 'message': '값이 입력되지 않았습니다.' }

        if self.option == 'register' :
            if '' in (self.id, self.pwd, self.pwd_confirm, self.name, self.email):
                pass    
            elif self.pwd != self.pwd_confirm:
                result['message'] = '비밀번호가 일치하지 않습니다.'
            elif self.compareId():
                result['message'] = '중복된 아이디입니다.'
            else: 
                result['pass'] = True
            return result
        else:
            if '' in (self.id, self.pwd): pass
            elif not self.checkPwd(): 
                result['message'] = '비밀번호가 일치하지 않습니다.'
            else: 
                result['pass'] = True
            return result

    def register(self):
        self.option = 'register'
        result = self.verify()
        
        if not result['pass']: return result
        else:
            encryption_pwd = self.encryption()
            query = 'insert into "user"(user_id, user_pwd, user_name, user_email, user_register_date, user_auth) values(%s, %s, %s, %s, now(), 0)'
            with connection.cursor() as cursor:
                cursor.execute(query, [self.id, encryption_pwd, self.name, self.email])
                connection.commit()
                result['message'] = '회원 가입되었습니다. 로그인을 해주세요.'
            return result
        
    def encryption(self):            
        hashed_pwd = bcrypt.hashpw(self.pwd.encode('utf-8'), bcrypt.gensalt(10))
        return hashed_pwd.decode('utf-8')

    def checkPwd(self):
        query = 'select user_pwd from "user" where user_id = %s'
        with connection.cursor() as cursor:
            cursor.execute(query, [self.id])
            encryption_pwd = cursor.fetchone()
            if encryption_pwd:
                if encryption_pwd[0] == self.pwd: return True
                else: return bcrypt.checkpw(self.pwd.encode('utf-8'), encryption_pwd[0].encode('utf-8'))
            else: return False

    def login(self):
        self.option = 'login'
        result = self.verify()
        if not result['pass']: return result 
        else: 
            query = 'select user_name from "user" where user_id = %s'
            with connection.cursor() as cursor:
                cursor.execute(query, [self.id])
                name = cursor.fetchone()

            result['user_id'] = self.id
            result['user_name'] = name[0]
            result['message'] = name[0] + '님 환영합니다.'
            return result

    def getMemberInfo(self, id):
        query = "select user_id, user_name, user_email, user_register_date, user_auth from \"user\" where user_id = '{0}'"
        with connection.cursor() as cursor:
                cursor.execute(query.format(id))
                userInfo = cursor.fetchone()
                object = changeToObject([userInfo], cursor)
                object[0]['user_register_date'] = object[0]['user_register_date'].strftime('%Y.%m.%d, %H:%M:%S')
        return object[0]

    def updateProfile(self, id):
        piece = []
        if self.name is not None:
            piece.append(" user_name = '{1}' ")
        if self.pwd is not None and self.pwd is not '':
            piece.append(" user_pwd = '{2}' ")
        if self.email is not None:
            piece.append(" user_email = '{3}' ")

        piece = (',').join(piece)
        query = "update \"user\" set " + piece + " where user_id = '{0}'"
        print(query)
        with connection.cursor() as cursor:
            encryption_pwd = self.encryption()
            cursor.execute(query.format(id, self.name, encryption_pwd, self.email))
            connection.commit()
    
    def deleteMember(self, id):
        query = "delete from \"user\" where user_id = '{0}'"
        with connection.cursor() as cursor:
            cursor.execute(query.format(id))
            connection.commit()

    def temporaryPassword(self):
        result = { 'message': '일치하는 이메일이 없습니다.', 'pass': False, 'pwd': '' }
        query = "select user_id from \"user\" where user_email = '{0}'"
        with connection.cursor() as cursor:
            cursor.execute(query.format(self.email))
            id = cursor.fetchone()
            if id is not None:
                self.pwd = randomPwd()
                result['message'] = '비밀번호를 재설정 했습니다.'
                result['pass'] = True
                result['pwd'] = self.pwd
                hashPWd = self.encryption()
                query = "update \"user\" set user_pwd = '{0}' where user_id = '{1}'"
                cursor.execute(query.format(hashPWd, id[0]))
                connection.commit()
        return result

    def __del__(self):
        connection.close()