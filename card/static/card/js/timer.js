var seconds_left = 0;
var negative = false;
var use_negative_sign = false; // used when timer turns negative on screen

$(document).ready(function(){
  var hours = parseInt($('#hours').text());
  var minutes = parseInt($('#minutes').text());

  seconds_left = hours * 60 * 60 + minutes * 60;

  if ($('#negative').text() === "True") {
    negative = true;
    seconds_left *= -1;
  }

  if ($('#timer_active').text()) {
    var timer = setInterval(update_timer, 1000);
  }
})

function update_timer() {
  if (seconds_left == 0) {
    negative = true;
    use_negative_sign = true;
  }

  seconds_left--;

  var seconds_left_abs = Math.abs(seconds_left);

  var hours = Math.floor(seconds_left_abs / 60 / 60);
  var minutes = Math.floor((seconds_left_abs - hours * 60 * 60) / 60);
  var seconds = seconds_left_abs - hours * 60 * 60 - minutes * 60;

  $('#hours').text(hours);
  if (use_negative_sign) $('#hours').text("- " + hours); // used when timer turns negative on screen
  $('#minutes').text(minutes);
  $('#seconds').text(seconds);
}
