$(function () {
    var $li = $('ul.tab_login_title li');
    $($li.eq(0).addClass('active').find('a').attr('href')).siblings('.tab_login_inner').hide();

    $li.click(function () {
        $($(this).find('a').attr('href')).show().siblings('.tab_login_inner').hide();
        $(this).addClass('active').siblings('.active').removeClass('active');
    });
});