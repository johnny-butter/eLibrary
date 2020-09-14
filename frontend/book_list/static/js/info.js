$.ajaxSetup({
    headers: {
        'Authorization': "JWT " + $.cookie("token")
    },
    beforeSend: function(xhr, settings) {
        let lang = $.cookie("django_language") || "zh-tw";

        settings.url = "/" + lang + settings.url;
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
            $('#status-msg-r').text("請確認密碼一致");
            $('#status-msg-r').slideDown();
            $('#status-msg-r').delay(1500).slideUp();
            return;
        }
        console.info($("#username").attr('name'))
        $.ajax({
            type: "PUT",
            url: "/api/v2/user/",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(data),
            success: function (msg) {
                $('#status-msg-g').text("Update Success");
                $('#status-msg-g').slideDown();
                $('#status-msg-g').delay(1500).slideUp("slow", "swing", function() {
                    window.location.reload();
                });
            },
            error: function (error) {
                let errMsg = "";
                if (error.responseJSON.detail == null) {
                    for (var k in error.responseJSON) {
                        errMsg += k + ": " + error.responseJSON[k][0].message;
                    }
                } else {
                    errMsg = error.responseJSON.detail.message;
                }
                $('#status-msg-r').text(errMsg);
                $('#status-msg-r').slideDown();
                $('#status-msg-r').delay(1500).slideUp();
            }
        });
    });
});
