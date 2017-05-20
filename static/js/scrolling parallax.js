$(document).ready(function() {
	var ori_scroll_top = $(document).scrollTop()
  $(document).scroll(function() {
    $("body").css("background-position", 'center ' + (-50 + (Math.abs($(document).scrollTop() - ori_scroll_top) * 0.07) + 'px'));
    $(".slide-2").css("background-position", 'center ' + (-200 + (Math.abs($(document).scrollTop() - ori_scroll_top) * 0.1) + 'px'));
    console.log($(document).scrollTop())
  });
  // $(".jumbotron").css("height", $(window).height())
});
