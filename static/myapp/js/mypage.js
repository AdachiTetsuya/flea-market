'use strict';


function changeBackColor(){
    var url = location.href;
    var ary = url.split('/');
    var firststr = ary[ary.length - 2];
    var secondstr = ary[ary.length - 1];
    var lefttargets = document.getElementsByClassName('left_item');
    var righttargets = document.getElementsByClassName('option_text');

    if(firststr === 'listings'){
        lefttargets[0].classList.add('background');
        lefttargets[1].classList.remove('background');

        if(secondstr === 'listing'){
            righttargets[0].classList.add('textcolor');
            righttargets[1].classList.remove('textcolor');
            righttargets[2].classList.remove('textcolor');
        }else if(secondstr === 'in_progress'){
            righttargets[0].classList.remove('textcolor');
            righttargets[1].classList.add('textcolor');
            righttargets[2].classList.remove('textcolor');
        }else if(secondstr === 'completed'){
            righttargets[0].classList.remove('textcolor');
            righttargets[1].classList.remove('textcolor');
            righttargets[2].classList.add('textcolor');
        }

    }else if(firststr === 'purchases'){
        lefttargets[0].classList.remove('background');
        lefttargets[1].classList.add('background');

        if(secondstr === 'in_progress'){
            righttargets[0].classList.add('textcolor');
            righttargets[1].classList.remove('textcolor');
            
        }else if(secondstr === 'completed'){
            righttargets[0].classList.remove('textcolor');
            righttargets[1].classList.add('textcolor');
        }
            
    }
}


// windowをloadしたタイミングで実行
window.addEventListener('load', changeBackColor);
