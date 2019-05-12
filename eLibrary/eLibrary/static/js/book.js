$.ajaxSetup({
    headers: {
        'Authorization': "JWT " + $.cookie("token")
    }
});
$(document).ready(function () {
    $("select").change(function () {
        $.get($(this).val());
        window.location.href = $(this).val();
        $(this).val('account')
    })
    $(".fav").click(function () {
        $(this).parent().block({
            message: "<img src='/static/fav_load.gif'/>",
            css: { borderWidth: '0px', backgroundColor: 'transparent' }
        });
        var that = $(this);
        $.post("/api/favbook/", { 'bookname': $(this).val() }, function (msg) {
            that.parent().unblock();
            if (msg.isFavorite) {
                that.attr("src", "/static/m_fav.png");
            } else {
                that.attr("src", "/static/m_unfav.png");
                // that.text("fav this");
            }
        })
    })

    $(".find").click(function () {
        window.location.href = "/elibrary/booklist/?search=" + $("#bookname").val();
    })
});