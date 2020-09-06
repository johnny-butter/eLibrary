function isLogin() {
    if ($.cookie('token') == null) {
        return false
    }
    return true
}

function appLogin(username, pwd, oauth_type = null, oauth_response = null) {
    $.blockUI({
        message: "<img src='/static/loading.gif'/>",
        css: { borderWidth: '0px', backgroundColor: 'transparent' }
    });

    if (oauth_response == null) {
        var uid = "";
    } else {
        var uid = oauth_response.id;
    };

    // Set by "ajaxSetup", need remove it first
    delete $.ajaxSettings.headers["Authorization"];

    $.ajax({
        type: "POST",
        url: "/api/v2/login/",
        data: {
            'username': username,
            'password': pwd,
            'provider': oauth_type,
            'uid': uid
        },
        success: function (msg) {
            $.cookie("token", msg.token, { path: "/" });

            $.unblockUI();

            $("#modal-msg-g").html("Login Success");
            $("#modal-msg-g").slideDown();
            $("#modal-msg-g").delay(3000).slideUp("slow", "swing", function() {
                window.location.reload();
            });
        },
        error: function (error) {
            $.unblockUI();

            $("#modal-msg-r").html(error.responseText);
            $("#modal-msg-r").slideDown();
            $("#modal-msg-r").delay(3000).slideUp();
        }
    });
};

$(document).ready(function () {
    $(".el-navbar-item").click(function(event) {
        if (!isLogin()) {
            event.preventDefault();
            $("#popLoginToggle").click();
            return
        }
    });

    $("#pop-login-submit").click(function () {
        var username = $("#pop-login-account").val();
        var password = $("#pop-login-password").val();

        appLogin(username, password);
    });
})
