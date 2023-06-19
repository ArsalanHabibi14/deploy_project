$(document).ready(function () {
    $(".radio-weight").on('click', function () {
        var _finalprice = $(this).attr('data-final-price');
        var _defaultprice = $(this).attr('data-default-price');
        var _specialprice = $(this).attr('data-special-price');
        const numberFormatter = Intl.NumberFormat('en-US');
        const formattedfinalprice = numberFormatter.format(_finalprice);
        const formatteddefaultprice = numberFormatter.format(_defaultprice);
        $(".product-price-ajax").text(formattedfinalprice + " تومان")

        if (_specialprice == null) {
            $(".product-defualt-price-ajax").text("")
            $(".product-special-price-percent").text("")
            $(".product-special-price-percent-text").text("")

        } else {
            var decreaseValue = _defaultprice - _specialprice;

            var _SpecialPricePercent = (((decreaseValue / _defaultprice) * 100).toLocaleString('fullwide', {maximumFractionDigits: 0}) + "%");
            $(".product-special-price-percent").text(_SpecialPricePercent);
            $(".product-special-price-percent-text").text("تخفیف")

            $(".product-defualt-price-ajax").text(formatteddefaultprice + " تومان");


        }
    })
    $("#coupon-btn").css('background', '#999999');
    $("#coupon-btn").prop('disabled', true);


})

function couponCheck() {
    if ($('#coupon-code').val() != '') {
        $("#coupon-btn").css('background', '');
        $("#coupon-btn").prop('disabled', false);

    } else {
        $("#coupon-btn").css('background', '#999999');
        $("#coupon-btn").prop('disabled', true);
    }
}

$('#coupon-code').keyup(function () {
    if ($('#coupon-code').val() != '') {
        $("#coupon-btn").css('background', '');
        $("#coupon-btn").prop('disabled', false);

    } else {
        $("#coupon-btn").css('background', '#999999');
        $("#coupon-btn").prop('disabled', true);
    }
});

function addProductToBookmarks(productId) {
    $("#loading-icon-bookmark").append('<span class="spinner-border spinner-border-sm"\n' +
        '                                              role="status"\n' +
        '                                              aria-hidden="true"></span>')
    $("#add-to-bookmark-btn").css('background', '#999999')
    $("#add-to-bookmark-btn").prop('disabled', true)
    $('.btn-add-to-wishlist-' + productId).css('background', '#999999');
    $('.btn-add-to-wishlist-' + productId).prop('disabled', true);
    $.get('/panel/bookmarks/add?product_id=' + productId).then(res => {
        $("#loading-icon-bookmark").html("")
        $("#add-to-bookmark-btn").css('background', '')
        $("#add-to-bookmark-btn").prop('disabled', false)


        if (res.status === 'success') {
            $('.btn-add-to-wishlist-' + productId).css('background', '');
            $('.btn-add-to-wishlist-' + productId).prop('disabled', false);
            toastr.success('محصول با موفقیت به علاقه مندی ها اضافه شد', '', {
                "closeButton": false,
                "debug": false,
                "newestOnTop": false,
                "progressBar": true,
                "positionClass": "toast-bottom-left",
                "preventDuplicates": false,
                "onclick": null,
                "showDuration": "300",
                "hideDuration": "1000",
                "timeOut": "5000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            });
        }
        if (res.status === 'removed') {
            $('.bookmarks-ajax').html(res.body);
            $('.bookmarks-dashboard-ajax').html(res.body2);
            $('.btn-add-to-wishlist-' + productId).css('background', '');
            $('.btn-add-to-wishlist-' + productId).prop('disabled', false);
            toastr.info('محصول با موفقیت از علاقه مندی ها حذف شد', '', {
                "closeButton": false,
                "debug": false,
                "newestOnTop": false,
                "progressBar": true,
                "positionClass": "toast-bottom-left",
                "preventDuplicates": false,
                "onclick": null,
                "showDuration": "300",
                "hideDuration": "1000",
                "timeOut": "5000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            });
        }
        if (res.status === 'not_found') {
            $('.btn-add-to-wishlist-' + productId).css('background', '');
            $('.btn-add-to-wishlist-' + productId).prop('disabled', false);
            toastr.error('محصول مورد نظر یافت نشد', '', {
                "closeButton": false,
                "debug": false,
                "newestOnTop": false,
                "progressBar": true,
                "positionClass": "toast-bottom-left",
                "preventDuplicates": false,
                "onclick": null,
                "showDuration": "300",
                "hideDuration": "1000",
                "timeOut": "5000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            });

        }
        if (res.status === 'not_auth') {
            $('.btn-add-to-wishlist-' + productId).css('background', '');
            $('.btn-add-to-wishlist-' + productId).prop('disabled', false);
            toastr.warning('ابتدا وارد حساب کاربری خود شوید', '', {
                "closeButton": false,
                "debug": false,
                "newestOnTop": false,
                "progressBar": true,
                "positionClass": "toast-bottom-left",
                "preventDuplicates": false,
                "onclick": null,
                "showDuration": "300",
                "hideDuration": "1000",
                "timeOut": "5000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            });

        }
    }).fail(function () {
        toastr.error('خطا , لطفا لحظاتی دیگر تلاش کنید', '', {
            "closeButton": false,
            "debug": false,
            "newestOnTop": false,
            "progressBar": true,
            "positionClass": "toast-bottom-left",
            "preventDuplicates": false,
            "onclick": null,
            "showDuration": "300",
            "hideDuration": "1000",
            "timeOut": "5000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
        });

    });
}


function addProductToBasketInDetail(productId) {
    const productCount = $('#product-count').val();
    const productWeight = $('input[name="product-weight"]:checked').val();
    if (productWeight != null) {
        $("#loading-icon-basket").append('<span class="spinner-border spinner-border-sm"\n' +
            '                                              role="status"\n' +
            '                                              aria-hidden="true"></span>')
        $("#add-to-basket-btn").css('background', '#999999')
        $("#add-to-basket-btn").prop('disabled', true)

        $.get('/order/add-to-order?product_id=' + productId + '&count=' + productCount + '&weight=' + productWeight).then(res => {
            $("#loading-icon-basket").html("")
            $("#add-to-basket-btn").css('background', '')
            $("#add-to-basket-btn").prop('disabled', false)
            if (res.status === 'success') {
                toastr.success('محصول با موفقیت به سبد خرید اضافه شد', '', {
                    "closeButton": false,
                    "debug": false,
                    "newestOnTop": false,
                    "progressBar": true,
                    "positionClass": "toast-bottom-left",
                    "preventDuplicates": false,
                    "onclick": null,
                    "showDuration": "300",
                    "hideDuration": "1000",
                    "timeOut": "5000",
                    "extendedTimeOut": "1000",
                    "showEasing": "swing",
                    "hideEasing": "linear",
                    "showMethod": "fadeIn",
                    "hideMethod": "fadeOut"
                });
                $('.basket-content').html(res.body);
                $('.m-basket-content').html(res.body2);
                $('.m-basket-content-count').html(res.body3);

            }
            if (res.status === 'not_found') {
                toastr.error('محصول مورد نظر یافت نشد', '', {
                    "closeButton": false,
                    "debug": false,
                    "newestOnTop": false,
                    "progressBar": true,
                    "positionClass": "toast-bottom-left",
                    "preventDuplicates": false,
                    "onclick": null,
                    "showDuration": "300",
                    "hideDuration": "1000",
                    "timeOut": "5000",
                    "extendedTimeOut": "1000",
                    "showEasing": "swing",
                    "hideEasing": "linear",
                    "showMethod": "fadeIn",
                    "hideMethod": "fadeOut"
                });

            }
            if (res.status === 'not_auth') {
                toastr.warning('برای افزودن محصول به سبد خرید ابتدا وارد شوید', '', {
                    "closeButton": false,
                    "debug": false,
                    "newestOnTop": false,
                    "progressBar": true,
                    "positionClass": "toast-bottom-left",
                    "preventDuplicates": false,
                    "onclick": null,
                    "showDuration": "300",
                    "hideDuration": "1000",
                    "timeOut": "5000",
                    "extendedTimeOut": "1000",
                    "showEasing": "swing",
                    "hideEasing": "linear",
                    "showMethod": "fadeIn",
                    "hideMethod": "fadeOut"
                });

            }
            if (res.status === 'invalid_count') {
                toastr.error('تعداد وارد شده باید بیشتر از 1 باشد', '', {
                    "closeButton": false,
                    "debug": false,
                    "newestOnTop": false,
                    "progressBar": true,
                    "positionClass": "toast-bottom-left",
                    "preventDuplicates": false,
                    "onclick": null,
                    "showDuration": "300",
                    "hideDuration": "1000",
                    "timeOut": "5000",
                    "extendedTimeOut": "1000",
                    "showEasing": "swing",
                    "hideEasing": "linear",
                    "showMethod": "fadeIn",
                    "hideMethod": "fadeOut"
                });

            }
            if (res.status === 'invalid_count_number') {
                toastr.error('تعداد وارد شده در انبار موجود نمیباشد', '', {
                    "closeButton": false,
                    "debug": false,
                    "newestOnTop": false,
                    "progressBar": true,
                    "positionClass": "toast-bottom-left",
                    "preventDuplicates": false,
                    "onclick": null,
                    "showDuration": "300",
                    "hideDuration": "1000",
                    "timeOut": "5000",
                    "extendedTimeOut": "1000",
                    "showEasing": "swing",
                    "hideEasing": "linear",
                    "showMethod": "fadeIn",
                    "hideMethod": "fadeOut"
                });

            }
        }).fail(function () {
            toastr.error('خطا , لطفا لحظاتی دیگر تلاش کنید', '', {
                "closeButton": false,
                "debug": false,
                "newestOnTop": false,
                "progressBar": true,
                "positionClass": "toast-bottom-left",
                "preventDuplicates": false,
                "onclick": null,
                "showDuration": "300",
                "hideDuration": "1000",
                "timeOut": "5000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            });

        });
    } else {
        toastr.error('لطفا گزینه ای را انتخاب کنید', '', {
            "closeButton": false,
            "debug": false,
            "newestOnTop": false,
            "progressBar": true,
            "positionClass": "toast-bottom-left",
            "preventDuplicates": false,
            "onclick": null,
            "showDuration": "300",
            "hideDuration": "1000",
            "timeOut": "5000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
        });

    }

}

function removeOrderDetail(detailId) {
    $.get('/panel/remove-order-detail?detail_id=' + detailId).then(res => {
        if (res.status === 'success') {
            toastr.success('محصول با موفقیت از سبد خرید حذف شد', '', {
                "closeButton": false,
                "debug": false,
                "newestOnTop": false,
                "progressBar": true,
                "positionClass": "toast-bottom-left",
                "preventDuplicates": false,
                "onclick": null,
                "showDuration": "300",
                "hideDuration": "1000",
                "timeOut": "5000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            });
            $('.order-detail-content').html(res.body);
            $('.basket-content').html(res.body2);
            $('.m-basket-content').html(res.body3);
            $('.m-basket-content-count').html(res.body4);


        }
    }).fail(function () {
        toastr.error('خطا , لطفا لحظاتی دیگر تلاش کنید', '', {
            "closeButton": false,
            "debug": false,
            "newestOnTop": false,
            "progressBar": true,
            "positionClass": "toast-bottom-left",
            "preventDuplicates": false,
            "onclick": null,
            "showDuration": "300",
            "hideDuration": "1000",
            "timeOut": "5000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
        });

    });
}

function changeOrderDetailCount(detailId, state) {
    $.get('/panel/change-order-detail?detail_id=' + detailId + '&state=' + state).then(res => {
        if (res.status === 'success') {
            $('.order-detail-content').html(res.body);
            $('.basket-content').html(res.body2);
            $('.m-basket-content').html(res.body3);
            $('.m-basket-content-count').html(res.body4);

        }
    }).fail(function () {
        toastr.error('خطا , لطفا لحظاتی دیگر تلاش کنید', '', {
            "closeButton": false,
            "debug": false,
            "newestOnTop": false,
            "progressBar": true,
            "positionClass": "toast-bottom-left",
            "preventDuplicates": false,
            "onclick": null,
            "showDuration": "300",
            "hideDuration": "1000",
            "timeOut": "5000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
        });

    });
}

$("#userpanelsetaddress").click(function () {
    $(".modal-address-set").fadeIn();

});

function checkUserStatus() {
    $("#loading-icon-status-btn").append('<span class="spinner-border spinner-border-sm"\n' +
        '                                              role="status"\n' +
        '                                              aria-hidden="true"></span>')
    $("#check-user-status-btn").css('background', '#999999');
    $("#check-user-status-btn").css('border-color', '#999999');
    $("#check-user-status-btn").prop('disabled', true);

    $.get('/panel/check-status').then(res => {
        $("#loading-icon-status-btn").html("")
        $("#check-user-status-btn").css('background', '');
        $("#check-user-status-btn").css('border-color', '');

        $("#check-user-status-btn").prop('disabled', false);
        if (res.status === 'done_free') {
            window.location.href = "/panel/orders/";
            $("#check-user-status-btn").prop('disabled', true);

            toastr.success(res.title, '', {
                "closeButton": false,
                "debug": false,
                "newestOnTop": false,
                "progressBar": false,
                "positionClass": "toast-bottom-left",
                "preventDuplicates": false,
                "onclick": null,
                "showDuration": "300",
                "hideDuration": "1000",
                "timeOut": "90000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            });
        }
        if (res.status === 'no_address_set') {
            toastr.error(res.title, '', {
                "closeButton": false,
                "debug": false,
                "newestOnTop": false,
                "progressBar": true,
                "positionClass": "toast-bottom-left",
                "preventDuplicates": false,
                "onclick": null,
                "showDuration": "300",
                "hideDuration": "1000",
                "timeOut": "5000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            });

        }
        if (res.status === 'no_main_address_set') {
            toastr.error(res.title, '', {
                "closeButton": false,
                "debug": false,
                "newestOnTop": false,
                "progressBar": true,
                "positionClass": "toast-bottom-left",
                "preventDuplicates": false,
                "onclick": null,
                "showDuration": "300",
                "hideDuration": "1000",
                "timeOut": "5000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            });
        }
        if (res.status === 'done') {
            window.location.href = "/order/request-payment/";
            toastr.success(res.title, '', {
                "closeButton": false,
                "debug": false,
                "newestOnTop": false,
                "progressBar": false,
                "positionClass": "toast-bottom-left",
                "preventDuplicates": false,
                "onclick": null,
                "showDuration": "300",
                "hideDuration": "1000",
                "timeOut": "90000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            });
        }
        if (res.status === 'no_phone_set') {
            toastr.error(res.title, '', {
                "closeButton": false,
                "debug": false,
                "newestOnTop": false,
                "progressBar": true,
                "positionClass": "toast-bottom-left",
                "preventDuplicates": false,
                "onclick": null,
                "showDuration": "300",
                "hideDuration": "1000",
                "timeOut": "10000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            });
        }


    }).fail(function () {
        toastr.error('خطا , لطفا لحظاتی دیگر تلاش کنید', '', {
            "closeButton": false,
            "debug": false,
            "newestOnTop": false,
            "progressBar": true,
            "positionClass": "toast-bottom-left",
            "preventDuplicates": false,
            "onclick": null,
            "showDuration": "300",
            "hideDuration": "1000",
            "timeOut": "5000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
        });

    });
}

function useCoupon() {
    const couponCode = $('#coupon-code').val();
    $('#coupon-btn').prop('disabled', true)

    $("#loading-icon").append('<span class="spinner-border spinner-border-sm"\n' +
        '                                              role="status"\n' +
        '                                              aria-hidden="true"></span>')

    $('#coupon-btn').css('background-color', '#999999')

    $.get('/panel/use-coupon?coupon_code=' + couponCode).then(res => {
        $("#loading-icon").html("")
        $('#coupon-btn').prop('disabled', false)
        $('#coupon-btn').css('background-color', '')

        if (res.status === 'valid') {
            $('.main-address-in-basket').html(res.body);

            toastr.success(res.title, '', {
                "closeButton": false,
                "debug": false,
                "newestOnTop": false,
                "progressBar": true,
                "positionClass": "toast-bottom-left",
                "preventDuplicates": false,
                "onclick": null,
                "showDuration": "300",
                "hideDuration": "1000",
                "timeOut": "5000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            });

        }
        if (res.status === 'not_valid') {
            toastr.error(res.title, '', {
                "closeButton": false,
                "debug": false,
                "newestOnTop": false,
                "progressBar": true,
                "positionClass": "toast-bottom-left",
                "preventDuplicates": false,
                "onclick": null,
                "showDuration": "300",
                "hideDuration": "1000",
                "timeOut": "5000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            });

        }
        if (res.status === 'empty') {
            toastr.info(res.title, '', {
                "closeButton": false,
                "debug": false,
                "newestOnTop": false,
                "progressBar": true,
                "positionClass": "toast-bottom-left",
                "preventDuplicates": false,
                "onclick": null,
                "showDuration": "300",
                "hideDuration": "1000",
                "timeOut": "5000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            });

        }


    }).fail(function () {
        toastr.error('خطا , لطفا لحظاتی دیگر تلاش کنید', '', {
            "closeButton": false,
            "debug": false,
            "newestOnTop": false,
            "progressBar": true,
            "positionClass": "toast-bottom-left",
            "preventDuplicates": false,
            "onclick": null,
            "showDuration": "300",
            "hideDuration": "1000",
            "timeOut": "5000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
        });

    });
}


function removeCoupon() {
    $("#loading-icon").append('<span class="spinner-border spinner-border-sm"\n' +
        '                                              role="status"\n' +
        '                                              aria-hidden="true"></span>')

    $.get('/panel/remove-coupon').then(res => {
        $("#loading-icon").html("")

        if (res.status === 'success') {
            $('.main-address-in-basket').html(res.body);
            $("#coupon-btn").css('background', '#999999');
            $("#coupon-btn").prop('disabled', true);
            toastr.success(res.title, '', {
                "closeButton": false,
                "debug": false,
                "newestOnTop": false,
                "progressBar": true,
                "positionClass": "toast-bottom-left",
                "preventDuplicates": false,
                "onclick": null,
                "showDuration": "300",
                "hideDuration": "1000",
                "timeOut": "5000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            });

        }
        if (res.status === 'error') {
            window.location.reload();
            toastr.error(res.title, '', {
                "closeButton": false,
                "debug": false,
                "newestOnTop": false,
                "progressBar": true,
                "positionClass": "toast-bottom-left",
                "preventDuplicates": false,
                "onclick": null,
                "showDuration": "300",
                "hideDuration": "1000",
                "timeOut": "5000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut",

            });

        }


    }).fail(function () {
        toastr.error('خطا , لطفا لحظاتی دیگر تلاش کنید', '', {
            "closeButton": false,
            "debug": false,
            "newestOnTop": false,
            "progressBar": true,
            "positionClass": "toast-bottom-left",
            "preventDuplicates": false,
            "onclick": null,
            "showDuration": "300",
            "hideDuration": "1000",
            "timeOut": "5000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
        });

    });
}
