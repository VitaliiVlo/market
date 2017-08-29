function show_form() {
    $("#show_form").hide();
    $("#form").show();
}

function send_order() {

    var email = $('#email').val();
    var name = $('#name').val();
    var address = $('#address').val();
    var phone = $('#phone').val();
    var comment = $('#comment').val();
    var csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url: "/order/add/",
        type: "post",
        data: {
            email: email,
            name: name,
            address: address,
            phone: phone,
            comment: comment,
            csrfmiddlewaretoken: csrfmiddlewaretoken
        },
        success: function (data) {
            if (data.check === true) {
                window.location.href = "/order/all/";
            }
            else {
                $("#fails").html(data.check).show();
            }
        }
    })
}

function delete_from_basket(id) {
    var csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url: "/basket/remove/",
        type: 'post',
        data: {
            id: id,
            csrfmiddlewaretoken: csrfmiddlewaretoken
        },
        success: function () {
            $("#product" + id).hide();
            var total = $("#total_price");
            total.html(total.html() - $("#price" + id).html());
        }
    })

}

function change_number(event) {
    var key = event.keyCode;

    if (key < 48 || key > 57) {
        event.preventDefault();
    }
}

function calculate(event, id) {
    var nmb = event.currentTarget.value;
    if (!isNaN(nmb) && nmb >= 1) {
        var csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: '/basket/number/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrfmiddlewaretoken,
                id: id,
                nmb: nmb
            },
            success: function (data) {

                if (data.fails !== "true") {

                    var total_price = $("#price" + id);
                    var product_price = total_price.data('price');
                    var sum = $("#total_price");

                    var new_price = nmb * product_price;

                    sum.text(Number(sum.text() - total_price.text()) + new_price);
                    total_price.text(nmb * product_price);
                }

            }
        })

    }
}

