$.ajaxSetup({
    headers: {
        'Authorization': "JWT " + $.cookie("token")
    }
});
$(document).ready(function () {
    $("#updateinfo").click(function () {
        var data = {
            'username': $("#username").val(),
            'email': $("#useremail").val(),
        };
        if ($("#pass1").val() != "" && $("#pass1").val() == $("#pass2").val()) {
            data["password"] = $("#pass1").val();
        } else if ($("#pass1").val() != "") {
            alert("請確認密碼一致");
            return;
        }
        console.info($("#username").attr('name'))
        $.ajax({
            type: "PUT",
            url: "/api/v2/user/detail/",
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
