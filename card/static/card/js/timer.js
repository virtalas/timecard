var seconds_left = 0;

$(document).ready(function(){
  var hours = parseInt($('#hours').text());
  var minutes = parseInt($('#minutes').text());

  seconds_left = hours * 60 * 60 + minutes * 60;

  if ($('#timer_active').text()) {
    var timer = setInterval(update_timer, 1000);
  }
})

function update_timer() {
  seconds_left--;

  var hours = Math.floor(seconds_left / 60 / 60);
  var minutes = Math.floor((seconds_left - hours * 60 * 60) / 60);
  var seconds = seconds_left - hours * 60 * 60 - minutes * 60;

  $('#hours').text(hours);
  $('#minutes').text(minutes);
  $('#seconds').text(seconds);
}
