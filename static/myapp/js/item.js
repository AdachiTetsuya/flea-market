'use strict';


const item_button = document.getElementById('item_button')
const is_purchased = JSON.parse(document.getElementById('is_purchased').textContent)
if(is_purchased){
  item_button.classList.add('purchased')
}