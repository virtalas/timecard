// Used to concatenate a starting time to the link to start a timer for that particular project

$(document).ready(function(){
  update_project_links();

  $('#work_start_time').bind('input propertychange', function() {
    update_project_links();
  });
})

function update_project_links() {
  var hour = $('#work_start_time').val().split(":")[0];
  var minute = $('#work_start_time').val().split(":")[1];

  $("a.project").each(function() {
    var $this = $(this);
    var _href = $this.attr("href");

    if (_href.indexOf('?') !== -1) {
      _href = _href.substring(0, _href.indexOf('?')) // Remove previous parameters
    }

    $this.attr("href", _href + '?start_hour=' + hour + "&start_minute=" + minute);
  });
}
