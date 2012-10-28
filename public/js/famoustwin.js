var FAMOUSTWIN = (function () {

  var my = {};
  var day = null;
  var month = null;
  var year = null;

  my.init = function () {
    $(".dobday").change(my.changeDay);
    $(".dobmonth").change(my.changeMonth);
    $(".dobyear").change(my.changeYear);
  };

  my.changeDay = function () {
    day = $(".dobday").val();
    my.checkDob();
  };

  my.changeMonth = function () {
    month = $(".dobmonth").val();
    my.checkDob();
  };

  my.changeYear = function () {
    year = $(".dobyear").val();
    my.checkDob();
  };

  my.checkDob = function () {
    if (day && month && year) {
      my.submitDob();
    }
  };

  my.submitDob = function () {
    // load loading image
    $.ajax({
      type: "POST",
      url: "http://localhost:8888/lookup",
      dataType: "jsonp",
      cache: false,
      timeout: 5000,
      data: {
        "day": day,
        "month": month,
        "year": year
        },
      jsonpCallback: "_testcb",
      success: function(data) {
          $("#results").html(data);
      },
      error: function(jqXHR, textStatus, errorThrown) {
          alert('error ' + textStatus + " " + errorThrown);
      }
//      complete: function (jqXHR, textStatus) {
//        alert(textStatus);
//      }
    });
 



//    }).fail(function( html ) {
//      $("#results").append(html);
//    }).always(function (){
//      alert("always");
//    });
    // remove loading image
  }

  return my;
}());

$(document).ready(function() {
    // put all your jQuery goodness in here.
  FAMOUSTWIN.init();
});

function FamousTwinViewModel() {
    var self = this;
    self.twins = ko.observableArray([]);
}

function FamousTwin(person) {
    this.person = person;
}

ko.applyBindings(new FamousTwinViewModel());
