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
    $(".fav").click(function () {
        $(this).parent().block({
            message: "<img src='/static/fav_load.gif'/>",
            css: { borderWidth: '0px', backgroundColor: 'transparent' }
        });

        var that = $(this);
        $.ajax({
            type: "POST",
            url: "/api/v2/favbook/",
            data: { 'book': $(this).val() },
            success: function (msg) {
                that.parent().unblock();

                if (msg.isFavorite) {
                    that.attr("src", "/static/m_fav.png");
                } else {
                    that.attr("src", "/static/m_unfav.png");
                }
            },
            error: function (error) {
                that.parent().unblock();

                $("#status-msg-r").html(error.responseJSON.detail.message);
                $("#status-msg-r").slideDown();
                $("#status-msg-r").delay(3000).slideUp();
            }
        });
    });

    // Reference: https://stackoverflow.com/a/15579157
    $("a[rel~='keep-params']").click(function (event) {
        event.preventDefault();

        var params = window.location.search.split("&");
        params.splice(0, 1);

        if (params.length > 0) {
            params = "&" + params.join("&");
        } else {
            params = "";
        }

        var dest = $(this).attr('href') + params;

        // A short timeout has helped overcome browser bugs
        window.setTimeout(function () {
            window.location.href = dest;
        }, 100);
    });

    $("#searchEnter").click(function () {
        window.location.href = "/books/list/?search=" + $("#searchText").val();
    })
    $(".shopplus").click(function () {
        var book_id = $(this).val()
        $.ajax({
            type: "POST",
            url: "/api/v2/cart/?action=add",
            data: {'book': book_id},
            success: function (msg) {
                $("#status-msg-g").html(
                    "商品成功加入購物車 <a href=\"/payment/purchase/\" class=\"alert-link\">前往察看</a>"
                );
                $("#status-msg-g").slideDown();
                $("#status-msg-g").delay(3000).slideUp();
            },
            error: function (error) {
                alert(error.responseJSON.detail.message);
            }
        });
    })
});
