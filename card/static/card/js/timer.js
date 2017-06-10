var seconds_left = 0;
var negative = false;
var use_negative_sign = false; // used when timer turns negative on screen
var startTime;

$(document).ready(function(){
  startTime = Date.parse($('#start_time').text());
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

  // Update length
  var length = Date.now() - startTime;
  $('#length').text(msToTime(length));
}

function msToTime(s) {
  var ms = s % 1000;
  s = (s - ms) / 1000;
  var secs = s % 60;
  s = (s - secs) / 60;
  var mins = s % 60;
  var hrs = (s - mins) / 60;

  var length = "";

  if (hrs) length += hrs + " hours, ";
  length += mins + " minutes, ";
  length += secs + " seconds";

  return length;
}
