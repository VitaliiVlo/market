function showinfo(id) {
    $("#info_order" + id).toggle();
    $("#span" + id).toggleClass("dropup");

    var order = $("#order" + id);

    if (order.css('background-color') === 'rgb(255, 204, 153)') {
        order.css('background-color', 'white');
    }
    else {
        order.css('background-color', '#FFCC99');
    }
}

function cancel_order(id) {
    var csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url: '/order/cancel/',
        type: 'post',
        data: {
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            id:id,
        },
        success: function (data) {
            $("#status"+id).text(data.status);
        }
    })
}