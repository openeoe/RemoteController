document.addEventListener('DOMContentLoaded', function() {
});





(function($) {
  $(function() {

    var data


    $( document ).ready(function() {
      $('select').formSelect();

      $.ajaxSettings.async = false;


      $.ajax({
          type: "GET",
          url: 'http://129.254.165.43:8000/combine',

      }).done(function (jqXHR) {

          console.log( "success" );
          console.log(jqXHR);

    /*
          var html = '<select name="select" id="select">';
          html = html + '  <option value="" disabled selected>테스트할 조합을 선택해주세요.</option>';
          for (var oper in jqXHR.operList) {
            if (object.hasOwnProperty(variable)) {
              html = html + '  <option value="' + port + '">' +  opername + '</option>';
            }
          }
          html = html + '</select>';*/

          var html = '';
          for (var ops in jqXHR.opsList) {
              html = html + '  <option value="' + port + '">' +  opsname + '</option>';
          }

          $('select').append(html);


          $('#select').change(function () {
              var port = $(this).val();
              var text = $("#speech").text()

              $.ajax({
                  type: "POST",
                  url: window.location + "",
                  data: {'port': port, 'text': text}

              }).done(function (msg) {

                  $("#result").text(msg)
              });
          });
      });

    /*
      data.forEach(function(_url){
        $.get(_url, {
        },function(jqXHR) {
          console.log( "success" );
          current_url = _url;
          current_name = jqXHR.name;
          $(".hide-on-med-and-down").append('<li><a href="#" onclick="change(\'' + _url + '\', \'' + jqXHR.name + '\')">' + jqXHR.name + '</a></li>');
        },'json')
        //.done(function(jqXHR) {
        //  console.log( "success done" );
        //})
        .fail(function(jqXHR) {
          console.log( "error" );
        })
        .always(function(jqXHR) {
          console.log( "finished" );
        });
      })*/

      //change(current_url, current_name);
    });

    function init(url, name) {
      $("#speech").text("")
    }

    /*function change(url, name) {
      $("#speech").text("")
    }*/

    $('#download-button').click( function() {
      action();
    });

    $("#speech").keypress(function(e) {
      if (e.keyCode == 13){
        action();
      }
    });

    function action() {
      var speech = $("#speech").val();
      $.post('', {
        content: speech
      },function(jqXHR) {
        console.log( "success" );
      },'json' /* xml, text, script, html */)
      //.done(function(jqXHR) {
      //  alert("second success" );
      //})
      .fail(function(jqXHR) {
        console.log( "error" );
      })
      .always(function(jqXHR) {
        console.log( "finished" );
        $("#speech").val("");
      });
    }

  }); // end of document ready
})(jQuery); // end of jQuery name space
