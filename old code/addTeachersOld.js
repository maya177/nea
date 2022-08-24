console.log("working")

var num = 2; // ads 2 fields at a time

var createInputs = function () {
    $("#form").append("<br>");
  $("#ip_div").append('<form id="form"></form>');
  for (var i = 0; i < num; i++) {
    $("#form").append("<br>");
    $("#form").append("<input></input>");

  }
};

$("#btn").click(function () {
    console.log("pressed")
  createInputs();
  //create unique ID for each input
  $("#form")
    .find("input")
    .each(function (i) {
      $(this).attr("id", "num" + i);
      $(this).attr("placeholder", "num" + i);
    });
});
