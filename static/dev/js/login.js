function auth() {
    var login = $("#inputName").val();
    var password = $("#inputPassword").val();
    var csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url: "/login/userin/",
        type: "post",
        data: {
            "password": password,
            "login": login,
            "csrfmiddlewaretoken": csrfmiddlewaretoken
        },
        success: function (data) {
            if (data.check === true) {
                window.location.href = '/';
            } else {
                $("#auth-error").show();
            }
        }
    })

}


function reg() {

    $("#reg-ok").hide();

    var login = $("#RegInputName").val();
    var password = $("#RegInputPassword").val();
    var password_rep = $("#RegInputPasswordConfirm").val();
    var csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: "/login/adduser/",
        type: "post",
        data: {
            "login": login,
            "password": password,
            "password_rep": password_rep,
            "csrfmiddlewaretoken": csrfmiddlewaretoken
        },
        success: function (data) {
            if (data.fails === true) {
                $("#RegInputName").val("");
                $("#RegInputPassword").val("");
                $("#RegInputPasswordConfirm").val("");
                $("#reg-ok").html("Регистрация прошла успешно").css("color", "green").show();
            } else {
                $("#reg-ok").html(data.fails).css("color", "red").show();
            }
        }
    })

}