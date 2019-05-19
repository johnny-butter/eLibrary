$(function () {
    var $li = $('ul.tab_login_title li');
    $($li.eq(0).addClass('active').find('a').attr('href')).siblings('.tab_login_inner').hide();

    $li.click(function () {
        $($(this).find('a').attr('href')).show().siblings('.tab_login_inner').hide();
        $(this).addClass('active').siblings('.active').removeClass('active');
    });
});

function app_register(id, name, email) {
    $.ajax({
        type: "POST",
        url: '/api/cbv/user/',
        data: {
            'username': "fb_" + id,
            'password': id,
            'email': email
        },

        success: function (msg) {
            $.unblockUI();
            $('#status_msg').text("Success");
            $('#status_msg').css({ "background-color": "#99CC66" });
            $('#status_msg').slideDown();
            $('#status_msg').delay(1500).slideUp("slow", "swing",
                app_login('fb_' + id, id)
            );
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

function fb_oauth_register(fb_response) {
    var url = "https://graph.facebook.com/" + fb_response.authResponse.userID +
        "?access_token=" + fb_response.authResponse.accessToken + "&fields=name,email"
    $.ajax({
        type: "GET",
        url: url,
        success: function (response) {
            app_login("fb_" + response.id, response.id, response = response);
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

function app_login(user, pass, response = null) {
    $.ajax({
        type: "POST",
        url: "/api/token/",
        data: {
            'username': user,
            'password': pass
        },
        success: function (msg) {
            $.cookie("token", msg.access, { path: "/" });
            $.cookie("token_r", msg.refresh, { path: "/" });
            window.location.href = "/elibrary/booklist/?page=1";
        },
        error: function (error) {
            if (response != null) {
                app_register(response.id, response.name, response.email);
            };
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
        $.blockUI({
            message: "<img src='/static/loading.gif'/>",
            //no border and no background color
            css: { borderWidth: '0px', backgroundColor: 'transparent' }
        });
        $.ajax({
            type: "POST",
            url: "/api/token/",
            // dataType: "json",
            // contentType: "application/json; charset=utf-8",
            data: {
                'username': $("#login_account").val(),
                'password': $("#login_password").val()
            },
            success: function (msg) {
                $.cookie("token", msg.access, { path: "/" });
                $.cookie("token_r", msg.refresh, { path: "/" });
                $.unblockUI();
                $('#status_msg').text("Success");
                $('#status_msg').css({ "background-color": "#99CC66" });
                $('#status_msg').slideDown();
                $('#status_msg').delay(1500).slideUp("slow", "swing",
                    function () {
                        window.location.href = "/elibrary/booklist/?page=1";
                    });

            },
            error: function (error) {
                $.unblockUI();
                $('#status_msg').text("Fail:" + error.responseText);
                $('#status_msg').css({ "background-color": "#FF6666" });
                $('#status_msg').slideDown();
                $('#status_msg').delay(3000).slideUp();
            }
        });
    });

    $('#register_form').submit(function (event) {
        $.blockUI({
            message: "<img src='/static/loading.gif'/>",
            //no border and no background color
            css: { borderWidth: '0px', backgroundColor: 'transparent' }
        });
        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: $(this).serialize(),
            // timeout: 100,
            success: function (msg) {
                $.unblockUI();
                $('#status_msg').text("Success");
                $('#status_msg').css({ "background-color": "#99CC66" });
                $('#status_msg').slideDown();
                $('#status_msg').delay(1500).slideUp("slow", "swing",
                    function () {
                        location.reload();
                    });
            },
            error: function (error) {
                $.unblockUI();
                $('#status_msg').text("Fail:" + error.responseText);
                $('#status_msg').css({ "background-color": "#FF6666" });
                $('#status_msg').slideDown();
                $('#status_msg').delay(3000).slideUp();
            }
        });
        // Notice "preventDefault" from the submit event,
        // otherwise the form will be posted also.
        event.preventDefault();
    });

});
