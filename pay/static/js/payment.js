var pay_order_id = null;
$("#order-create-button").click(function () {
    var books_info = [];
    create_books_info(books_info);

    $.ajax({
        type: "POST",
        url: '/api/v2/pay_order/',
        headers: {
            'Authorization': "JWT " + $.cookie("token")
        },
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify({
            'total_price': $("#cart_total_amount").text(),
            'pay_type': "braintree",
            'item_list': books_info,
        }),
        success: function (msg) {
            pay_order_id = msg.id
            $.get("/api/v2/braintree_client_token/", function (msg) {
                var pay_token = msg.token;
                create_braintree_pay(pay_token);
            });
        },
        error: function (error) {
            console.warn(error);
        }
    });
});

function create_books_info(books_info) {
    $('#cart-table tbody tr').each(function () {
        var book_info = {};
        book_info["book"] = $(this).find('th.cart_book_name').data('value');
        book_info["quantity"] = $(this).find('td.cart_book_quantity').text();
        book_info["price"] = $(this).find('td.cart_book_price').text();

        if (book_info["book"] != null) books_info.push(book_info);
    });
}

var button = document.querySelector('#submit-button');
function create_braintree_pay(pay_token) {
    braintree.dropin.create({
        authorization: pay_token,
        container: '#dropin-container'
    }, function (createErr, instance) {
        $("#submit-button").show();
        button.addEventListener('click', function () {
            instance.requestPaymentMethod(function (err, payload) {
                // Submit payload.nonce to your server
                $.ajax({
                    type: "POST",
                    url: '/api/v2/pay/',
                    headers: {
                        'Authorization': "JWT " + $.cookie("token")
                    },
                    contentType: 'application/json; charset=UTF-8',
                    data: JSON.stringify({
                        'pay_order_id': pay_order_id,
                        'extra_data': {
                            'nonce': payload.nonce,
                        },
                    }),
                    success: function (msg) {
                        var obj = $(".modal-body").text(
                            '交易代碼: ' + msg.data.transaction_id + "\n" +
                            '金額: ' + msg.data.amount + " " + msg.data.currency + "\n" +
                            '日期: ' + msg.data.date + "\n" +
                            '付款方式: ' + msg.data.payment_type
                        );
                        obj.html(obj.html().replace(/\n/g, '<br/>'));
                        $("#success-btn").click();
                        $.ajax({
                            type: "DELETE",
                            url: '/api/v2/cart/?del=all',
                            headers: {
                                'Authorization': "JWT " + $.cookie("token")
                            },
                            success: function (msg) {
                                console.log("Success");
                                console.log(msg.data.delete_count);
                            },
                            error: function (error) {
                                console.log("Fail");
                                console.log(error.responseText);
                            }
                        });
                    },
                    error: function (error) {
                        $(".modal-title").text("Fail");
                        $(".modal-body").text(error.responseText);
                        $("#success-btn").click();
                    }
                });
            });
        });
    });
}
