function refundrequest(detailId, skuid) {

    $.get('/panel/refund-request?detailid=' + detailId + '&skuid=' + skuid).then(res => {
        if (res.status === 'success') {
            $('.refunds-ajax').html(res.body);

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
                "hideMethod": "fadeOut",
            });

        }
        if (res.status === 'error') {
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


function remove_address(addressId) {
    $.get('/panel/addresses/remove-address?address_id=' + addressId).then(res => {
        if (res.status === 'success') {
            $('.address-ajax').html(res.body);
            $('.main-address-in-basket').html(res.body2);

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
                "timeOut": "1000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut",

            });

        } else {
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
                "timeOut": "2000",
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

function set_address_main(addressId) {
    $.get('/panel/addresses/set-address-main?address_id=' + addressId).then(res => {
        if (res.status === 'success') {
            $('.address-ajax').html(res.body);
            $('.main-address-in-basket').html(res.body2);

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
                "timeOut": "1000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut",
            });

        } else {
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
                "timeOut": "2000",
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


function add_address() {
    const receiverName = $('#add-receiver-name-input').val();
    const receiverPhone = $('#add-receiver-phone-input').val();
    const province = $('#add-province-input').val();
    const city = $('#add-city-input').val();
    const postalcode = $('#add-postalcode-input').val();
    const address = $('#add-address-input').val();
    $.get('/panel/addresses/add-new-address?province=' + province + '&city=' + city + '&postalcode=' + postalcode + '&address=' + address + '&receivername=' + receiverName + '&receiverphone=' + receiverPhone).then(res => {
        if (res.status === 'error') {
            toastr.error(res.title, '', {
                "closeButton": false,
                "debug": false,
                "newestOnTop": false,
                "progressBar": true,
                "positionClass": "toast-top-center",
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
        if (res.status === 'full') {

            $("#addAddressModal").toggle();
            $(".modal-backdrop").remove();
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
        if (res.status === 'success') {
            $("#addAddressModal").toggleClass('show');
            $(".modal-backdrop").remove();
            $('.address-ajax').html(res.body);
            $('.main-address-in-basket').html(res.body2);


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
                "timeOut": "2000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut",
            });
        }
    }).fail(function (){
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

function open_edit_address(addressId) {
    $.get('/panel/addresses/edit-address-info?address_id=' + addressId).then(res => {
        if (res.status === 'success') {
            $("#edit-receiver-name-input").val(res.receivername);
            $("#edit-receiver-phone-input").val(res.receiverphone);
            $("#edit-province-input").val(res.province);
            $("#edit-city-input").val(res.city);
            $("#edit-postalcode-input").val(res.postalcode);
            $("#edit-address-input").val(res.address);
            $("#edit-address-id-input").val(addressId);


        }
    }).fail(function (){
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

function edit_address() {
    const address_id = $('#edit-address-id-input').val();
    const receivername = $('#edit-receiver-name-input').val();
    const receiverphone = $('#edit-receiver-phone-input').val();
    const province = $('#edit-province-input').val();
    const city = $('#edit-city-input').val();
    const postalcode = $('#edit-postalcode-input').val();
    const address = $('#edit-address-input').val();

    $.get('/panel/addresses/edit-address?address_id=' + address_id + '&receivername=' + receivername + '&receiverphone=' + receiverphone + '&province=' + province + '&city=' + city + '&postalcode=' + postalcode + '&address=' + address).then(res => {
        if (res.status === 'success') {
            $("#editAddressModal").toggle()
            $(".modal-backdrop").remove();
            $('.address-ajax').html(res.body);
            $('.main-address-in-basket').html(res.body2);

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
                "timeOut": "1000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut",
            });

        } else {
            toastr.error(res.title, '', {
                "closeButton": false,
                "debug": false,
                "newestOnTop": false,
                "progressBar": true,
                "positionClass": "toast-top-center",
                "preventDuplicates": false,
                "onclick": null,
                "showDuration": "300",
                "hideDuration": "1000",
                "timeOut": "2000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut",
            });
        }

    }).fail(function (){
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

$(document).ready(function () {

    $("#userpanel-set-phone-input").keyup(function (e) {
        var key = e.which
        const un_check_keycodes = [9, 13, 16, 17, 18, 19, 20, 27, 33, 34, 35, 36, 37, 38, 39, 40, 45, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 144,]
        if (un_check_keycodes.includes(key)) {

        } else {
            const phone = $("#userpanel-set-phone-input").val();
            var phoneregex = new RegExp('^(\\+|0)?9\\d{9}$');
            var phoneresult = phoneregex.test(phone);
            if (phoneresult) {
                $.get('/panel/verify-phone?phone=' + phone).then(res => {
                    if (res.status === 'exist') {
                        $("#userpanel-set-phone-input").css("border-color", "red");
                        $("#userpanel-set-phone-valid").html(res.title);
                        $('#userpanel-set-phone-button').prop('disabled', true);
                        $("#userpanel-set-phone-button").hide()

                    }
                    if (res.status === 'not_valid') {
                        $("#userpanel-set-phone-input").css("border-color", "red");
                        $("#userpanel-set-phone-valid").html(res.title);
                        $('#userpanel-set-phone-button').prop('disabled', true);
                        $("#userpanel-set-phone-button").hide()

                    }
                    if (res.status === 'same') {
                        $("#userpanel-set-phone-input").css("border-color", "");
                        $("#userpanel-set-phone-valid").html("");
                        $('#userpanel-set-phone-button').prop('disabled', true);
                        $("#userpanel-set-phone-button").hide()

                    }
                    if (res.status === 'success') {
                        $("#userpanel-set-phone-input").css("border-color", "green");
                        $("#userpanel-set-phone-valid").html("");
                        $('#userpanel-set-phone-button').prop('disabled', false);
                        $("#userpanel-set-phone-button").toggle()


                    }

                }).fail(function (){
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
                $("#userpanel-set-phone-input").css("border-color", "red");
                $("#userpanel-set-phone-valid").html('لطفا شماره موبایل معتبر وارد کنید');
                $('#userpanel-set-phone-button').prop('disabled', true);
                $("#userpanel-set-phone-button").hide()
            }
        }


    });
    $("#userpanel-set-phone-button").click(function () {


        const phone = $("#userpanel-set-phone-input").val();
        $("#loading-icon-phone").append('<span class="spinner-border spinner-border-sm"\n' +
            '                                              role="status"\n' +
            '                                              aria-hidden="true"></span>')
        $('#userpanel-set-phone-button').prop('disabled', true);
        $('#userpanel-set-phone-button').css('background', '#999999');

        $.get('/panel/set-phone?phone=' + phone).then(res => {
            $('#userpanel-set-phone-button').css('background', '');
            $("#loading-icon-phone").html("")
            if (res.status === 'success') {
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
                    "hideMethod": "fadeOut",
                });
                $("#set-phone-section").toggle()
                $("#confirm-phone-section").toggle()
            }
        }).fail(function (){
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
    });
    $("#userpanel-confirm-phone-button").click(function () {
        const otp = $("#userpanel-confirm-phone-input").val();
        $("#loading-icon-phone").append('<span class="spinner-border spinner-border-sm"\n' +
            '                                              role="status"\n' +
            '                                              aria-hidden="true"></span>')
        $('#userpanel-confirm-phone-button').prop('disabled', true);
        $('#userpanel-confirm-phone-button').css('background', '#999999');

        $.get('/panel/confirm-phone?otp=' + otp).then(res => {
            $("#loading-icon-phone").html("")
            $('#userpanel-confirm-phone-button').css('background', '');

            if (res.status === 'error') {
                $("#userpanel-confirm-phone-input").css("border-color", "red");
                $("#userpanel-confirm-phone-valid").html(res.title);
                $('#userpanel-confirm-phone-button').prop('disabled', false);


            } else {
                $("#userpanel-confirm-phone-input").css("border-color", "green");
                $("#userpanel-confirm-phone-valid").html("");
                $('#userpanel-confirm-phone-button').prop('disabled', true);

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
                    "timeOut": "1000",
                    "extendedTimeOut": "1000",
                    "showEasing": "swing",
                    "hideEasing": "linear",
                    "showMethod": "fadeIn",
                    "hideMethod": "fadeOut",
                    onHidden: function () {
                        location.reload();
                    }
                });

            }


        }).fail(function (){
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

    });

    $("#userpanel-set-email-input").keyup(function (e) {
        var key = e.which
        const un_check_keycodes = [9, 13, 16, 17, 18, 19, 20, 27, 33, 34, 35, 36, 37, 38, 39, 40, 45, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 144,]
        if (un_check_keycodes.includes(key)) {

        } else {
            const email = $("#userpanel-set-email-input").val();
            var emailregex = /^[a-z0-9]+@[a-z]+\.com$/
            var emailresult = emailregex.test(email.toLowerCase());
            if (emailresult) {
                $.get('/panel/verify-email?email=' + email).then(res => {
                    if (res.status === 'exist') {
                        $("#userpanel-set-email-input").css("border-color", "red");
                        $("#userpanel-set-email-valid").html(res.title);
                        $('#userpanel-set-email-button').prop('disabled', true);
                        $("#userpanel-set-email-button").hide()

                    }
                    if (res.status === 'not_valid') {
                        $("#userpanel-set-email-input-input").css("border-color", "red");
                        $("#userpanel-set-email-valid").html(res.title);
                        $('#userpanel-set-email-button').prop('disabled', true);
                        $("#userpanel-set-email-button").hide()

                    }
                    if (res.status === 'same') {
                        $("#userpanel-set-email-input").css("border-color", "");
                        $("#userpanel-set-email-valid").html("");
                        $('#userpanel-set-email-button').prop('disabled', true);
                        $("#userpanel-set-email-button").hide()

                    }
                    if (res.status === 'success') {
                        $("#userpanel-set-email-input").css("border-color", "green");
                        $("#userpanel-set-email-valid").html("");
                        $('#userpanel-set-email-button').prop('disabled', false);
                        $("#userpanel-set-email-button").toggle()

                    }

                }).fail(function (){
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
                $("#userpanel-set-email-input-input").css("border-color", "red");
                $("#userpanel-set-email-valid").html("لطفا ایمیل معتبر وارد کنید");
                $('#userpanel-set-email-button').prop('disabled', true);
                $("#userpanel-set-email-button").hide()
            }
        }
    });
    $("#userpanel-set-email-button").click(function () {
        const email = $("#userpanel-set-email-input").val();
        $("#loading-icon-email").append('<span class="spinner-border spinner-border-sm"\n' +
            '                                              role="status"\n' +
            '                                              aria-hidden="true"></span>')
        $('#userpanel-set-email-button').prop('disabled', true);
        $('#userpanel-set-email-button').css('background', '#999999');

        $.get('/panel/set-email?email=' + email).then(res => {
            $("#loading-icon-email").html("")
            $('#userpanel-set-email-button').css('background', '');

            if (res.status === 'success') {
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
                    "hideMethod": "fadeOut",
                });
                $("#set-email-section").toggle()
                $("#confirm-email-section").toggle()
            }
        }).fail(function (){
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
    });
    $("#userpanel-confirm-email-button").click(function () {
        const otp = $("#userpanel-confirm-email-input").val();
        $("#loading-icon-email").append('<span class="spinner-border spinner-border-sm"\n' +
            '                                              role="status"\n' +
            '                                              aria-hidden="true"></span>')
        $('#userpanel-confirm-email-button').prop('disabled', true);
        $('#userpanel-confirm-email-button').css('background', '#999999');

        $.get('/panel/confirm-email?emailotp=' + otp).then(res => {
            $("#loading-icon-email").html("")
            $('#userpanel-confirm-email-button').css('background', '');

            if (res.status === 'error') {
                $("#userpanel-confirm-email-input").css("border-color", "red");
                $("#userpanel-confirm-email-valid").html(res.title);
                $('#userpanel-confirm-email-button').prop('disabled', false);


            } else {
                $("#userpanel-confirm-email-input").css("border-color", "green");
                $("#userpanel-confirm-email-valid").html("");
                $('#userpanel-confirm-email-button').prop('disabled', true);

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
                    "timeOut": "1000",
                    "extendedTimeOut": "1000",
                    "showEasing": "swing",
                    "hideEasing": "linear",
                    "showMethod": "fadeIn",
                    "hideMethod": "fadeOut",
                    onHidden: function () {
                        location.reload();
                    }
                });

            }


        }).fail(function (){
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

    });


});