window.onload = function() {
  var place_data = []
  $.ajax({
    url: '/load_attrations_data/',
    type: "GET",
    dataType: "json",
    success: function(json) {
      console.log(json)
      console.log("asds")
    },
    error: function() {
      console.log("ERROR");
    }
  });
}
