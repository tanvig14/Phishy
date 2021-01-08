$(document).ready(function() {

  $("#scroll").click(function() {
    console.log('here');
    $('html,body').animate({
        scrollTop: $("#home").offset().top},
        'slow');
  });

  $("#submiturl").click(function () {
    var url = $("#url").val();
    document.getElementById('result').src = "images/processing.gif";

    var request = $.ajax({
      url: "http://127.0.0.1:5000/adv_results/",
      method: "GET",
      dataType: "json",
      data: {
        url: url
      }
    });

    request.done (function (msg) {
      console.log(msg);
      document.getElementById('result').src = "images/loading (1).gif";
      $('#report').html("Incorrectly Reported?<br><input type=\"submit\" id=\"submiturl\" value=\"Report a problem\"/>");
    });

    request.fail (function (jqXHR, testStatus) {
      alert("Data transfer failed!");
    });

  });

 });