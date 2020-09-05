$(document).ready(function () {
    $(".account-item").click(function() {
        if ($(this).val() == "/login/") {
            $.removeCookie("token", { path: "/" });
        }

        window.location.href = $(this).val();
    });
})
