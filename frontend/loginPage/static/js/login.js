$(function () {
    var $li = $('ul.tab_login_title li');
    $($li.eq(0).addClass('active').find('a').attr('href')).siblings('.tab_login_inner').hide();

    $li.click(function () {
        $($(this).find('a').attr('href')).show().siblings('.tab_login_inner').hide();
        $(this).addClass('active').siblings('.active').removeClass('active');
    });
});

function app_register(username, pwd, email,
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
                app_login(null, null, oauth_type, oauth_response);
            };

            $('#status_msg').text("Success");
            $('#status_msg').css({ "background-color": "#99CC66" });
            $('#status_msg').slideDown();
            $('#status_msg').delay(1500).slideUp("slow", "swing");
        },
        error: function (error) {
            $.unblockUI();

            $('#status_msg').text("Fail:" + error.responseText);
            $('#status_msg').css({ "background-color": "#FF6666" });
            $('#status_msg').slideDown();
            $('#status_msg').delay(3000).slideUp();
        }
    });
}

function app_login(username, pwd, oauth_type = null, oauth_response = null) {
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

            $('#status_msg').text("Success");
            $('#status_msg').css({ "background-color": "#99CC66" });
            $('#status_msg').slideDown();
            $('#status_msg').delay(1500).slideUp("slow", "swing", function () {
                window.location.href = "/books/list/?page=1";
            });
        },
        error: function (error) {
            if (oauth_type != null && oauth_response != null) {
                app_register(null, null, null, oauth_type, oauth_response);
            } else {
                $.unblockUI();

                $('#status_msg').text("Fail:" + error.responseText);
                $('#status_msg').css({ "background-color": "#FF6666" });
                $('#status_msg').slideDown();
                $('#status_msg').delay(3000).slideUp();
            };
        }
    });
};

function fb_oauth_login(fb_response) {
    var url = "https://graph.facebook.com/" + fb_response.authResponse.userID +
        "?access_token=" + fb_response.authResponse.accessToken + "&fields=name,email"

    $.ajax({
        type: "GET",
        url: url,
        success: function (response) {
            app_login(null, null, "fb", response);
        },
        error: function (error) {
            $.unblockUI();

            $('#status_msg').text("Fail:" + error.responseText);
            $('#status_msg').css({ "background-color": "#FF6666" });
            $('#status_msg').slideDown();
            $('#status_msg').delay(3000).slideUp();
        }
    });

};

$(document).ready(function () {
    $("#login_tab input").keypress(function (event) {
        if (event.keyCode == 13) {
            $('#login_submit').click();
        }
    });

    $("#login_submit").click(function () {
        var username = $("#login_account").val();
        var password = $("#login_password").val();

        app_login(username, password);
    });

    $('#register_submit').click(function (event) {
        var username = $("#register_username").val();
        var password = $("#register_pwd").val();
        var email = $("#register_email").val();

        if (email == "") { email = null };

        app_register(username, password, email);
    });

});
