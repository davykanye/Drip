function totalIt() {
    var input = document.getElementsByName("product");
    var total = 0;
    for (var i = 0; i < input.length; i++) {
      if (input[i].checked) {
        total += parseFloat(input[i].value);
      }
    }
    
    document.getElementById("total").value = "$" + total.toFixed(2);
  }

$(function () {
        $("#p1").click(function () {
            if ($(this).is(":checked")) {
                $(".productOne").hide();
            }
        });
          $("#p2").click(function () {
            if ($(this).is(":checked")) {
                $(".productTwo").hide();
            }
        });
          $("#p3").click(function () {
            if ($(this).is(":checked")) {
                $(".productThree").hide();
            }
        });
});