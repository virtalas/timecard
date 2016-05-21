var hours = 0;
var minutes = 0;
var seconds = 0;

$(document).ready(function(){
  hours = parseInt($('hours'));
  minutes = parseInt($('minutes'));
  seconds = parseInt($('seconds'));

  var timer = setInterval(update_timer, 1000);
}

function update_timer() {
  seconds++;

}
