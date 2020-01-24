$.ajaxSetup({
    headers: {
        'Authorization': "JWT " + $.cookie("token")
    }
});
$(document).ready(function () {
    $("select").change(function () {
        $.get($(this).val());
        if ($(this).val() == "/elibrary/login/") {
            $.removeCookie("token", { path: "/" });
            $.removeCookie("token_r", { path: "/" });
        }
        window.location.href = $(this).val();
        $(this).val('account')
    });

    $(".fav").click(function () {
        $(this).parent().block({
            message: "<img src='/static/fav_load.gif'/>",
            css: { borderWidth: '0px', backgroundColor: 'transparent' }
        });
        var that = $(this);
        $.post("/api/v2/favbook/", { 'book': $(this).val() }, function (msg) {
            that.parent().unblock();
            if (msg.isFavorite) {
                that.attr("src", "/static/m_fav.png");
            } else {
                that.attr("src", "/static/m_unfav.png");
                // that.text("fav this");
            }
        })
    });

    $("a[rel~='keep-params']").click(function (event) {
        event.preventDefault();

        var params = window.location.search.split("&");
        params.splice(0, 1);
        // console.info(params)
        if (params.length > 0) {
            params = "&" + params.join("&");
        } else {
            params = "";
        }
        // console.info(params)
        var dest = $(this).attr('href') + params;

        // A short timeout has helped overcome browser bugs
        window.setTimeout(function () {
            window.location.href = dest;
        }, 100);
    });

    $(".find").click(function () {
        window.location.href = "/elibrary/booklist/?search=" + $("#book").val();
    })
    $(".shopplus").click(function () {
        $.post("/api/v2/cart/?action=add", { 'book': $(this).val() }, function (msg) {
            console.log("+1")
        })
    })
    $(".shopminus").click(function () {
        $.post("/api/v2/cart/?action=cut", { 'book': $(this).val() }, function (msg) {
            console.log("-1")
        })
    })
});
