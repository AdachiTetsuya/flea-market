'use strict';

$(function(){
    $('#textarea')
    .on('input', function(){
      if ($(this).outerHeight() > this.scrollHeight){
        $(this).height(1)
      }
      while ($(this).outerHeight() < this.scrollHeight){
        $(this).height($(this).height() + 1)
      }
    });
});