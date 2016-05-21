var hours = 0;
var minutes = 0;
var seconds = 0;

$(document).ready(function(){
  hours = parseInt($('#hours').text());
  minutes = parseInt($('#minutes').text());
  seconds = parseInt($('#seconds').text());

  var timer = setInterval(update_timer, 1000);
})

function update_timer() {
  seconds++;
  $('#seconds').text(seconds);
}
