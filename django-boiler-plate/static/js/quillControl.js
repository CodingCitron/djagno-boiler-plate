(function(){
    var quill = new Quill('#editor', {
        modules: {
            toolbar: [
                [{ header: [1, 2, false] }],
                ['bold', 'italic', 'underline'],
                ['image', 'code-block']
            ]
        },
        placeholder: '안녕하세요',
        theme: 'snow'
    })

    var form = document.querySelector('#quillForm')
    if(form){
        (function(){
            form.onsubmit = function(e) {
                e.preventDefault()
                var about = document.querySelector('input[name=about]')
                about.value = JSON.stringify(quill.getContents())
                
                console.log("Submitted", $(form).serialize(), $(form).serializeArray())
                form.submit()
            }

           var cancelButton = document.getElementById('updateCancel')
           var postCancel = document.getElementById('postCancel')

           if(cancelButton){
                cancelButton.addEventListener('click', function(e){
                    location.href = '/board/read/' + e.currentTarget.value + '/'
                })
            }

            if(postCancel){
                postCancel.addEventListener('click', function(e){
                    location.href = '/board/'
                })
            }
        })();
    }

    var contentsEl= document.getElementById('contentsValue')

    if(contentsEl){
        (function(){
            var quillWrapper = document.querySelector('.quill-wrapper')
            var view = document.querySelector('#contents')
    
            quill.setContents(JSON.parse(contentsEl.value))
            var html = quill.root.innerHTML
            view.innerHTML = html

            quillWrapper.remove()
            contentsEl.remove()
        })();
    }

    var updatePage = document.getElementById('update')

    if(updatePage){
        quill.setContents(JSON.parse(updatePage.value))
        updatePage.remove()
    }

    /* delete */
    var confirmDelete = document.getElementById('confirmDelete')
    if(confirmDelete){
        (function(){
            confirmDelete.addEventListener('click', function(e){
                e.preventDefault()
                if(!confirm('정말 삭제하시겠습니까?')) return
                location.href = e.currentTarget.href
            })
        })();
    }
})();