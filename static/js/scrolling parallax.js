$(document).ready(function() {
	var ori_scroll_top = $(document).scrollTop()
  $(document).scroll(function() {
    $(".jumbotron").css("background-position", 'center ' + (-50 + ($(document).scrollTop() * 0.2) + 'px'));
    $(".slide-2").css("background-position", 'center ' + (-300 + ($(document).scrollTop() * 0.2) + 'px'));
  });
  // $(".jumbotron").css("height", $(window).height())
});
