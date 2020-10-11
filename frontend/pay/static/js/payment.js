$.ajaxSetup({
    headers: {
        'Authorization': "JWT " + $.cookie("token")
    },
    beforeSend: function(xhr, settings) {
        let lang = $.cookie("django_language") || "zh-tw";

        settings.url = "/" + lang + settings.url;
    }
});

$("#order-create-button").click(function () {
    $.blockUI({
        message: "<img src='/static/loading.gif'/>",
        css: { borderWidth: '0px', backgroundColor: 'transparent' }
    });

    var books_info = [];
    var pay_type = $("#order-type-select").val();
    create_books_info(books_info);

    $.ajax({
        type: "POST",
        url: '/api/v2/pay_order/',
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify({
            'total_price': $("#cart_total_amount").text(),
            'pay_type': pay_type,
            'item_list': books_info,
        }),
        success: function (msg) {
            let pay_order_id = msg.id
            switch (pay_type) {
                case "braintree":
                    $.get("/api/v2/braintree_client_token/", function (msg) {
                        let pay_token = msg.token;
                        create_braintree_pay(pay_token, pay_order_id);

                        $.unblockUI();
                    });
                    break;
                case "manual":
                    alert("訂單已建立(id: " + pay_order_id + ")，付款完成後，請通知客服人員");
                    $.unblockUI();
                    break;
            };
        },
        error: function (error) {
            console.warn(error);

            $.unblockUI();
        }
    });
});

function clear_cart() {
    $.ajax({
        type: "DELETE",
        url: '/api/v2/cart/?del=all',
        success: function (msg) {
            console.log("Success");
            console.log(msg.data.delete_count);
        },
        error: function (error) {
            console.log("Fail");
            console.log(error.responseJSON.detail.message);
        }
    });
}

function create_books_info(books_info) {
    $('#cart-table tbody tr').each(function () {
        var book_info = {};
        book_info["book"] = $(this).find('td.cart_book_name').data('value');
        book_info["quantity"] = $(this).find('td.cart_book_quantity').text();
        book_info["price"] = $(this).find('td.cart_book_price').text();

        if (book_info["book"] != null) books_info.push(book_info);
    });
}

function create_braintree_pay(pay_token, pay_order_id) {
    braintree.dropin.create({
        authorization: pay_token,
        container: '#dropin-container'
    }, function (createErr, instance) {
        $("#order-pay-btn").show();
        $("#order-cancel-btn").show();

        let pay_btn = document.querySelector('#order-pay-btn');
        pay_btn.addEventListener('click', function () {
            instance.requestPaymentMethod(function (err, payload) {
                // Submit payload.nonce to your server
                $.ajax({
                    type: "POST",
                    url: '/api/v2/pay/',
                    contentType: 'application/json; charset=UTF-8',
                    data: JSON.stringify({
                        'pay_order_id': pay_order_id,
                        'extra_data': {
                            'nonce': payload.nonce,
                        },
                    }),
                    success: function (msg) {
                        messageBody = [
                            "交易代碼: ".concat(msg.transaction_id),
                            "金額: ".concat(msg.transaction_total_price, " ", msg.transaction_currency),
                            "日期: ".concat(msg.create_date),
                            "付款方式: ".concat(msg.transaction_pay_type)
                        ]

                        var obj = $(".modal-body").text(messageBody.join("\n"));
                        obj.html(obj.html().replace(/\n/g, '<br/>'));

                        $("#modal-trigger-btn").click();

                        clear_cart();
                    },
                    error: function (error) {
                        $(".modal-title").text("Fail");

                        messageBody = [
                            "error code: ".concat(error.responseJSON.detail.message[0].cade.message),
                            "error message: ".concat(error.responseJSON.detail.message[0].message.message)
                        ]

                        var obj = $(".modal-body").text(messageBody.join("\n"));
                        obj.html(obj.html().replace(/\n/g, '<br/>'));

                        $("#modal-trigger-btn").click();
                    }
                });
            });
        });

        let cancel_btn = document.querySelector('#order-cancel-btn');
        cancel_btn.addEventListener('click', function () {
            $.ajax({
                type: "DELETE",
                url: '/api/v2/pay_order/',
                data: {'pay_order_id': pay_order_id},
                success: function (msg) {
                    $("#status-msg-g").html(
                        "訂單已成功取消"
                    );
                    $("#status-msg-g").slideDown();
                    $("#status-msg-g").delay(3000).slideUp("slow", "swing", function() {
                        window.location.reload();
                    });
                },
                error: function (error) {
                    alert(error.responseJSON.detail.message);
                }
            });
        })
    });
}

$(".shopminus").click(function () {
    var book_id = $(this).val()
    $.ajax({
        type: "POST",
        url: "/api/v2/cart/?action=cut",
        data: {'book': book_id},
        success: function (msg) {
            $("#status-msg-r").html(
                "商品成功移出購物車"
            );
            $("#status-msg-r").slideDown();
            $("#status-msg-r").delay(3000).slideUp("slow", "swing", function() {
                window.location.reload();
            });
        },
        error: function (error) {
            alert(error.responseJSON.detail.message);
        }
    });
})

$(document).ready(function () {
    $.get("/api/v2/pay_order/", function (msg) {
        $.blockUI({
            message: "<img src='/static/loading.gif'/>",
            css: { borderWidth: '0px', backgroundColor: 'transparent' }
        });

        let pay_order_id = msg.data.id
        $("#order-type-select").val(msg.data.pay_type);

        switch (msg.data.pay_type) {
            case "braintree":
                $.get("/api/v2/braintree_client_token/", function (msg) {
                    let pay_token = msg.token;
                    create_braintree_pay(pay_token, pay_order_id);

                    $.unblockUI();
                });
                break;
        };
    });
});
