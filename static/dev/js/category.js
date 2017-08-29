function show_products() {
    var data = $("#filters").serialize();
    var location = window.location.href;
    $.ajax({
        url: location+'product_filters/',
        type: 'post',
        data: data,
        success: function (data) {
            $("#products").html(data.list)
        }
    })
}