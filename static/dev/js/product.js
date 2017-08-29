var csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();

function add_in_basket(id) {
    var added = "Добавлено";
    var disabled = "disabled";

    $.ajax({
        url: '/basket/add/',
        type: 'post',
        data: {
            id: id,
            csrfmiddlewaretoken: csrfmiddlewaretoken
        },
        success: function () {
            var btn = $('#add');
            btn.html(added);
            btn.addClass(disabled);
        }
    })

}

function send_comment(product_id) {
    var text = $("#comment").val();
    var rating = $("#rating").val();

    $.ajax({
        url: '/product/add/comment/',
        type: 'post',
        data: {
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            text: text,
            rating: rating,
            product_id: product_id
        },
        success: function (data) {
            location.reload();
        }
    })
}

