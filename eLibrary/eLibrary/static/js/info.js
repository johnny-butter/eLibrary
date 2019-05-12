$.ajaxSetup({
    headers: {
        'Authorization': "JWT " + $.cookie("token")
    }
});
$(document).ready(function () {
    $(".divTableCell :button").click(function () {
        var data = {
            'username': $("#username").val(),
            'email': $("#useremail").val(),
        };
        if ($("#pass1").val() != "" && $("#pass1").val() == $("#pass2").val()) {
            data["password"] = $("#pass1").val();
        }
        console.info($("#username").attr('name'))
        $.ajax({
            type: "PUT",
            url: "/api/cbv/user/" + $("#username").attr('name') + '/',
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(data),
            success: function (msg) {
                window.location.reload();
            },
            error: function (error) {
                alert("Fail:" + error.responseText);
            }
        });
    });
});