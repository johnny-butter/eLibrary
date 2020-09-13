$(document).ready(function () {
    $(".account-item").click(function() {
        if ($(this).val() == "/login/") {
            $.removeCookie("token", { path: "/" });
        }

        window.location.href = $(this).val();
    });

    $(".lang-item").click(function(event) {
        event.preventDefault();

        let csrfToken = $.cookie("csrftoken");
        let newLang =  $(this).attr("name");

        $.ajax({
            url: "/i18n/setlang/",
            type: "POST",
            headers: {
                "X-CSRFToken": csrfToken
            },
            data: {
                "language": newLang
            },
            success: function (data) {
                window.location.replace("/");
            }
        });
   });
})
