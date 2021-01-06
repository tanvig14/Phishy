$(document).ready(function() {
    $("#submiturl").click(function () {
      var url = $("#url").val();


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
      });

      request.fail (function (jqXHR, testStatus) {
        alert("Data transfer failed!");
      });

    });

   });