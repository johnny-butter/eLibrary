$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        let lang = $.cookie("django_language") || "zh-tw";

        settings.url = "/" + lang + settings.url;
    }
});

function appRegister(username, pwd, email,
    oauth_type = null, oauth_response = null) {
    if (oauth_type != null && oauth_response != null) {
        var data = JSON.stringify({
            'email': oauth_response.email,
            'oauth_record': {
                'provider': oauth_type,
                'uid': oauth_response.id,
            },
        })
    } else {
        var data = JSON.stringify({
            'username': username,
            'password': pwd,
            'email': email,
        })
    }

    $.blockUI({
        message: "<img src='/static/loading.gif'/>",
        css: { borderWidth: '0px', backgroundColor: 'transparent' }
    });

    $.ajax({
        type: "POST",
        url: '/api/v2/user/',
        contentType: 'application/json; charset=UTF-8',
        data: data,
        success: function (msg) {
            $.unblockUI();

            if (oauth_type != null && oauth_response != null) {
                appLogin(null, null, oauth_type, oauth_response);
            };

            $('#status-msg-g').text("Register Success");
            $('#status-msg-g').slideDown();
            $('#status-msg-g').delay(1500).slideUp("slow", "swing", function() {
                data = $.parseJSON(data);
                appLogin(data.username, data.password);
            });
        },
        error: function (error) {
            $.unblockUI();

            $('#status-msg-r').text("Fail:" + error.responseText);
            $('#status-msg-r').slideDown();
            $('#status-msg-r').delay(3000).slideUp();
        }
    });
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

            $('#status-msg-g').text("Login Success");
            $('#status-msg-g').slideDown();
            $('#status-msg-g').delay(1500).slideUp("slow", "swing", function () {
                let lang = $.cookie("django_language") || "zh-tw";
                window.location.href = "/" + lang + "/books/list/?page=1";
            });
        },
        error: function (error) {
            if (oauth_type != null && oauth_response != null) {
                appRegister(null, null, null, oauth_type, oauth_response);
            } else {
                $.unblockUI();

                $('#status-msg-r').text("Fail:" + error.responseText);
                $('#status-msg-r').slideDown();
                $('#status-msg-r').delay(3000).slideUp();
            };
        }
    });
};

function fbOauthLogin(fb_response) {
    var url = "https://graph.facebook.com/" + fb_response.authResponse.userID +
        "?access_token=" + fb_response.authResponse.accessToken + "&fields=name,email"

    $.ajax({
        type: "GET",
        url: url,
        success: function (response) {
            appLogin(null, null, "fb", response);
        },
        error: function (error) {
            $.unblockUI();

            $('#status-msg-r').text("Fail:" + error.responseText);
            $('#status-msg-r').slideDown();
            $('#status-msg-r').delay(3000).slideUp();
        }
    });

};

function googleOauthLogin(google_response) {
    appLogin(null, null, "google", google_response)
}

$(document).ready(function () {
    $("#pills-home input").keypress(function (event) {
        if (event.keyCode == 13) {
            $('#login-submit').click();
        }
    });

    $("#login-submit").click(function () {
        var username = $("#login-account").val();
        var password = $("#login-password").val();

        appLogin(username, password);
    });

    $('#register-submit').click(function () {
        var username = $("#register-username").val();
        var password = $("#register-pwd").val();
        var email = $("#register-email").val();

        if (email == "") { email = null };

        appRegister(username, password, email);
    });
});
