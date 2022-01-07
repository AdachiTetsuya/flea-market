'use strict';

// is_purchasedがtrueなら購入ボタンを黒くする
let item_button = document.getElementById('item_button')
let is_purchased = JSON.parse(document.getElementById('is_purchased').textContent)
let a = document.getElementById('purchase_link')
if(is_purchased){
  item_button.classList.add('purchased');
  a.removeAttribute('href');
}

