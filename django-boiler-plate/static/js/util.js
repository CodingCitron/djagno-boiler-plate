var djagno_wprj_util = {}
djagno_wprj_util.event = {}
djagno_wprj_util.pagination = (function(){
    
    function Pagination(url){
        this.start = 1
        this.now = 1
        this.fullPage = 0
        this.showListLength = 10 
        this.articleLength = 0
        this.url = url
        this.list = []
    }

    Pagination.prototype.Ajax = function(now, callback){
        var obj = this

        $.ajax({
            url: obj.url,
            method: 'get',
            data: { 'now': now? now : obj.now , 'length': obj.showListLength },
            success: function(data){
                obj.now = Number(now? now : obj.now)
                obj.Update(data, callback)
            },
            error: function(error){ }
        })
    }

    Pagination.prototype.Update = function(data, callback){
        this.list = data.list
        this.articleLength = data.count
        this.fullPage = Math.ceil(this.articleLength/this.showListLength)
        // console.log(this)

        if(callback) callback()
    }

    return Pagination

})();

djagno_wprj_util.event.pgEl = (function(){
    var paginationEl = document.querySelector('#pagination > .list')
    if(!paginationEl) return

    var pg = new djagno_wprj_util.pagination('/board/ajaxList')

    pg.init = function(){
        pg.draw()
    }

    pg.draw = function(all){        
        var view = document.getElementById('view')
        var view_li = document.querySelectorAll('#view > li')

        let buttonArray = [...paginationEl.querySelectorAll('li')]

        for(var i = 0; i < buttonArray.length; i++){
            buttonArray[i].remove()
        }
        
        var start = ((Math.ceil(this.now/10) - 1) * 10) + 1
        var length = Math.ceil(this.now/10) * 10
        length = length > this.fullPage ? this.fullPage : length

        for(var i = start; i <= length; i++){
            let li = document.createElement('li')
            let button = document.createElement('button')
            li.appendChild(button)
            button.textContent = i
            button.value = i
            button.type = 'button'
            button.className = 'button'
            paginationEl.appendChild(li)
        }

        if(start > 10){ //prev 버튼 생성
            let li = createElement('li'),
            button = createElement('button', { 'type': 'button', 'className': 'button', 'value': start - 10 }, 'prev')
            li.appendChild(button)
            paginationEl.prepend(li)
        }

        if(start + 9 < this.fullPage){ //next 버튼 생성
            let li = createElement('li'),
            button = createElement('button', { 'type': 'button', 'className': 'button', 'value': start + 10 }, 'next')
            li.appendChild(button)
            paginationEl.append(li)
        }

        if(all){
            let array = [...view_li]
            let count = 0 
            for(let i = 1; i < array.length; i++){
                array[i].remove()
            }

            for(let i = 0; i < this.list.length; i++){
                count++
                let li = createElement('li'),
                post_id = createElement('div', null, this.list[i].post_id),
                title = createElement('div'),
                titleInner = createElement('a', 
                { 'href': '/board/read/' + this.list[i].post_id  }, this.list[i].title),
                writer = createElement('div', null, this.list[i].writer),
                register_date = createElement('div', 
                null, timeFormat(this.list[i].register_date))

                title.appendChild(titleInner)
                li.append(post_id)
                li.append(title)
                li.append(writer)
                li.append(register_date)
                view.append(li)
            }

            if(!count){
                let li = createElement('li', { 'className': 'grid-add' }, '현재 페이지에는 글이 없습니다.')
                view.append(li)
            }
        }

        var btn = paginationEl.querySelector(`button[value='${this.now}']`)
        if(!btn) return 
        btn.classList.add('active')
    }

    function timeFormat(time){
        var date = new Date(time)
        date.setTime(date.getTime() + 9)
        return date.getFullYear() + '.' + date.getMonth() + '.' + date.getDate()
    }
    
    function createElement(el, option, text){
        var element = document.createElement(el) 
        if(option) for(let property in option) element[property] = option[property]
        if(text) element.textContent = text
        return element
    }

    pg.Ajax(null, pg.init.bind(pg))

    paginationEl.addEventListener('click', function(e){
        if(e.target.nodeName != 'BUTTON') return
        pg.Ajax(e.target.value, function(){
            pg.draw.call(pg, 'all')
        })
    })

})();