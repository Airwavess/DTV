$(document).ready(function() {
  var ori_scroll_top = $(document).scrollTop()
  var bg_position_jumbotron = parseInt($('.jumbotron').css("background-position").split(" ")[1].split("px")[0])
  var bg_position_slide = parseInt($('.slide-2').css("background-position").split(" ")[1].split("px")[0])
  $(".jumbotron").css("background-position", 'center ' + (bg_position_jumbotron + ($(document).scrollTop() * 0.2) + 'px'));
  $(".slide-2").css("background-position", 'center ' + (bg_position_slide + ($(document).scrollTop() * 0.2) + 'px'));
  // bg_position_jumbotron = parseInt($('.jumbotron').css("background-position").split(" ")[1].split("px")[0])
  // bg_position_slide = parseInt($('.slide-2').css("background-position").split(" ")[1].split("px")[0])
  $(document).scroll(function() {
    $(".jumbotron").css("background-position", 'center ' + (bg_position_jumbotron + ($(document).scrollTop() * 0.2) + 'px'));
    $(".slide-2").css("background-position", 'center ' + (bg_position_slide + ($(document).scrollTop() * 0.2) + 'px'));
  });
});
