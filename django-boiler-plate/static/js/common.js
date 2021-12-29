/* 회원 탈퇴 */
(function(){
    var deleteMember = document.getElementById('deleteMember')
    if(deleteMember){

        deleteMember.addEventListener('click', function(e){
            var form = document.getElementById('deleteMemberForm')
            e.preventDefault()
            if(!confirm('정말 탈퇴하실건가요?')) return
            form.submit()
        })
    }

    var findIdPwd = document.getElementById('findIdPwd')

    if(findIdPwd){
        findIdPwd.addEventListener('click', function(e){
            e.preventDefault()
            temporaryPassword()
        })
    }

    function temporaryPassword(){
        var form = document.forms.findIdPwd
        var user_name = form['1'].value
        var user_email = form['2'].value

        if(user_name == '' || user_email == '') return alert('값을 입력하세요.') 

        $.ajax({
            url: '/user/findIdPwd/',
            method: 'post',
            data: { user_name: user_name, user_email: user_email },
            success: function(data){
                data = data.result
                data.pass? (alert(data.message + '\n' + '비밀번호:' + data.pwd), console.log(data.pwd)) : alert(data.message)
            },
            error: function(data){

            }
        })
    }   

})();

