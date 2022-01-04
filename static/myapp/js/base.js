'use strict';

const category_content = document.getElementById('category_content');

document.addEventListener('click', (e) => {
    if(!e.target.closest('#input-button')) {
      //ここに外側をクリックしたときの処理
      category_content.style.display = "none";
      
    } else {
      //ここに内側をクリックしたときの処理
      category_content.style.display = "block";
    }
})
const account_content = document.getElementById('account_content');

document.addEventListener('click', (e) => {
    if(!e.target.closest('#account_button')) {
      //ここに外側をクリックしたときの処理
      account_content.style.display = "none";
      
    } else {
      //ここに内側をクリックしたときの処理
      if(window.getComputedStyle(account_content).getPropertyValue("display")==="block"){
        account_content.style.display = "none";
      }else{
        account_content.style.display = "block";
      }
      
    }
})
