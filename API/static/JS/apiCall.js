$(document).ready(function() {
  $('#result').hide();
  $('#adding_gif').hide();

  $("#scroll").click(function() {
    $('html,body').animate({
        scrollTop: $("#home").offset().top},
        'slow');
  });

  $("#submiturl").click(function () {
    var url = $("#url").val();
    $('#report').html('');
    $('#result_msg').html('')
    $('#result').show();

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
      if(msg['Result'] == 1){
        $('#result').hide();
        $('#report').html("<input type=\"submit\" id=\"report\" value=\"Think we made a mistake? Click Here\"/>");
        $('#result_msg').html("This website appers to be <b style='color:#40e495'>Safe</b>");
      }
      if(msg['Result'] == -1){
        $('#result').hide();
        $('#report').html("<input type=\"submit\" id=\"report\" value=\"Think we made a mistake? Click Here\"/>");
        $('#result_msg').html("This website appers to be a <b style='color:#f53c2f'>Phish</b><br>Do not enter any sensitive data on this website")
      }
      if(msg['Result'] == 0){
        $('#result').hide();
        $('#result_msg').html("Our tests were <b style='color:#ff9900'>Inconclusive</b><br> We would caution against entering any sensitive data on this website")
      }
      
    });

    request.fail (function (jqXHR, testStatus) {
      $('#result_msg').html("Looks like something went wrong!<br>We are working on a fix")
    });

  });

  $("#report").click(function() {
    $('#adding_gif').show();
    $('#report').html("");
    var url = $("#url").val();
    console.log(url)

    var request = $.ajax({
      url: "http://127.0.0.1:5000/report/",
      method: "GET",
      dataType: "json",
      data: {
        url: url
      }
    });

    request.done (function (msg) {
      console.log(msg);
      if(msg['Logged']){
        $('#adding_gif').hide();
        $('#report').html("We have added this instance to our logs! We will use this feedback to improve our models.");
      } else{
        $('#adding_gif').hide();
        $('#report').html("We had trouble adding this page to our logs. Please try again later");
      }
    });


    request.fail (function (jqXHR, testStatus) {
      alert("Server did not respond. We are working on a fix!");
      $('#result_msg').html("Looks like something went wrong!<br>We are working on a fix")
    });


  });

 });