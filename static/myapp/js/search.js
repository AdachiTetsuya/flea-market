'use strict';

/**
 * 現在のURLからGETパラメータを削除したものを返します
 */
function getNowUrl(){
    var url = new URL(window.location.href);
    // URLSearchParamsオブジェクトを取得
    var params = url.searchParams;
    // URLからGETパラメータを削除
    params.delete('keyword');
    params.delete('category');
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
    var checks = document.getElementsByClassName('cattegory_checkbox');
    for (let i = 0; i < checks.length; i++) {
        if ( checks[i].checked === true ) {
            url.searchParams.append("category",checks[i].value);
        }
    }
    location.replace(url);
}


//checkboxの値を保持する
var targets = document.querySelectorAll('.cattegory_checkbox');
var checkboxClick = function(){
    var self = this;
    sessionStorage.setItem(self.getAttribute('id'), self.checked);
};
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
        if(session.getItem(key).toLowerCase() === 'true'){
            document.querySelector(`input#${key}`).checked = true;
        }else{
            document.querySelector(`input#${key}`).checked = false;
        }
    }
}

// windowをloadしたタイミングで実行
window.addEventListener('load', addSessionStorage);

