$.ajaxSetup({
    headers: {
        'Authorization': "JWT " + $.cookie("token")
    }
});
$(document).ready(function () {
    $(".fav").click(function () {
        var that = $(this);
        $.post("/api/favbook/", { 'bookname': $(this).val() }, function (msg) {
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