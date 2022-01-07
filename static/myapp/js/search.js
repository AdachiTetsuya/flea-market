'use strict';

const category_array = ['novel','society','culture','travel','economy','health','IT','hobby','life','art','foreign','picture','study','other'];
const quality_array = ['new','no_damaged','little_damaged','damaged','bad']
const sort_array = ['a_created_time','a_price','d_created_time','d_price']

/**
 * 現在のURLからGETパラメータを削除したものを返します
 */
function getNowUrl(){
    var url = new URL(window.location.href);
    // URLSearchParamsオブジェクトを取得
    var params = url.searchParams;
    // URLからGETパラメータを削除
    
    params.delete('csrfmiddlewaretoken');
    params.delete('keyword');
    params.delete('category');
    params.delete('status');
    params.delete('quality');
    params.delete('sort');

    return url
}

/**
 * 入力されたkeywordとcheckboxの値をクエリパラメータに設定しロードします
 */
function SearchButtonClick(){
    var keyword = document.getElementById("input-button").value;
    let url = getNowUrl();
    if(keyword){
        //入力されたkeywordをクエリパラメータに設定
        url.searchParams.append("keyword",keyword);
    }
    //checkboxの入力状況を確認し、クエリパラメータに設定する
    var checks = document.getElementsByClassName('search_checkbox');
    for (let i = 0; i < checks.length; i++) {
        if (checks[i].checked === true) {
            // カテゴリー
            if(category_array.includes(checks[i].value)){
                url.searchParams.append("category",checks[i].value);
                //販売状況
            }else if(checks[i].value === "on_sale"){
                url.searchParams.append("status","on_sale");
                //商品の状態
            }else if(quality_array.includes(checks[i].value)){
                url.searchParams.append("quality",checks[i].value);
            }
        }
    }
    location.replace(url);
}


//checkboxの値を保持する
var targets = document.querySelectorAll('.search_checkbox');
var checkboxClick = function(){
    var self = this;
    sessionStorage.setItem(self.getAttribute('id'), self.checked);
};
//checkboxの値がユーザによって変化させられたら作動
targets.forEach(function(e){
    e.addEventListener("change",checkboxClick)
    e.addEventListener("change",SearchButtonClick)
})

/**
 * ページ読み込み時にセッションを確認して、'true'の場合、checkedをtrueにする
 */
var addSessionStorage = function() {
    var session = sessionStorage;
    for(let i=0; i<session.length; i++){
        let key = session.key(i);
        if(category_array.includes(key) || quality_array.includes(key)){
            if(session.getItem(key).toLowerCase() === 'true'){
                document.querySelector(`input#${key}`).checked = true;
            }else{
                document.querySelector(`input#${key}`).checked = false;
            }
        }
    }
}

// windowをloadしたタイミングで実行
window.addEventListener('load', addSessionStorage);




let select = document.querySelector('[id="sort"]');
select.onchange = event => { 
    for (var i=0; i<4; i++) {
        sessionStorage.setItem(i, select.options[i].selected);
    }
}
