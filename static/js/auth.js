$(document).ready(function () {
    $("#btn-login-intro").prop('disabled', true)

    $("#auth-input").on('focusout keyup', function () {
        if ($("#auth-input").val().length <= 0) {
            $("#login-form-error").html('لطفا این قسمت را خالی نگذارید')
            $("#auth-input").css('border-color', 'red')
        } else {
            $("#login-form-error").html('')
            $("#auth-input").css('border-color', '')
        }
    });


    $("#auth-input").on('keyup', function () {
        var entered_info = $("#auth-input").val()
        var phoneregex = new RegExp('^(\\+|0)?9\\d{9}$');
        var emailregex = /^[a-z0-9]+@[a-z]+\.com$/
        var phoneresult = phoneregex.test(entered_info);
        var emailresult = emailregex.test(entered_info.toLowerCase());
        if (emailresult || phoneresult) {
            $("#btn-login-intro").prop('disabled', false)
            $("#btn-login-intro").css('box-shadow', '0px 0px 10px 5px rgb(92 241 160 / 40%)')

        } else {
            $("#btn-login-intro").prop('disabled', true)
            $("#btn-login-intro").css('box-shadow', '')
        }

    });
    $("#btn-login-intro").click(function () {
        $("#loading-icon").append('<span class="spinner-border spinner-border-sm"\n' +
            '                                              role="status"\n' +
            '                                              aria-hidden="true"></span>')

        $("#btn-login-intro").prop('disabled', true)
        $("#btn-login-intro").css('box-shadow', '')
        $("#btn-login-intro").css('background', '#999999');
        const info = $("#auth-input").val()
        $.get('auth?info=' + info).then(res => {
            $("#btn-login-intro").css('background', '');
            $("#btn-login-intro").css('box-shadow', '')
            $("#loading-icon").html("")

            if (res.status === 'empty') {


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
            if (res.status === 'login_by_password') {
                $("#login-form-section").html(res.body)

            }
            if (res.status === 'auth_by_phone_otp') {
                $("#login-form-section").html(res.body);
                submitPoll()
                countdown(2, 00);

                toastr.success('کد تایید به شماره ' + res.phone_number + ' ارسال شد', '', {
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
            if (res.status === 'auth_by_email_otp') {
                $("#login-form-section").html(res.body);
                submitPoll()
                countdown(2, 00);

                toastr.success('کد تایید به ایمیل ' + res.email_address + ' ارسال شد', '', {
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
    })


});
/*password login section*/
var lbp_section_input_check = function () {
    if ($("#lbp-section-password-input").val().length <= 0) {
        $("#lbp-section-btn").prop('disabled', true)
        $("#lbp-section-password-input").css('border-color', 'red')
        $("#lbp-section-btn").css('box-shadow', '')


    } else {
        $("#lbp-section-btn").prop('disabled', false)
        $("#lbp-section-password-input").css('border-color', '')
        $("#lbp-section-btn").css('box-shadow', '0px 0px 10px 5px rgb(92 241 160 / 40%)')


    }

}

var lbp_section_btn = function () {
    $("#loading-icon").append('<span class="spinner-border spinner-border-sm"\n' +
        '                                              role="status"\n' +
        '                                              aria-hidden="true"></span>')
    $("#lbp-section-btn").prop('disabled', true)
    $("#lbp-section-btn").css('box-shadow', '')
    $("#lbp-section-btn").css('background', '#999999')

    const password = $("#lbp-section-password-input").val()
    $.get('auth/password?password=' + password).then(res => {
        $("#lbp-section-btn").css('background', '')
        $("#loading-icon").html("")
        if (res.status === 'success') {
            window.location.href = "/";
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
                "timeOut": "10000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            });


        }
        if (res.status === 'wrong') {
            $("#lbp-section-btn").prop('disabled', false)
            $("#lbp-section-btn").css('box-shadow', '0px 0px 10px 5px rgb(92 241 160 / 40%)')

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
            $("#lbp-section-btn").prop('disabled', false)
            $("#lbp-section-btn").css('box-shadow', '0px 0px 10px 5px rgb(92 241 160 / 40%)')

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
        if (res.status === 'home') {

            window.location.href = "/";

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

/* otp login section*/

var lbotp_section_input_check = function () {
    if ($("#lbotp-section-input").val().length == 5) {
        lbotp_section_btn()
        $("#lbotp-section-input").blur()


    }
    if ($("#lbotp-section-input").val().length <= 0) {
        $("#lbotp-section-btn").prop('disabled', true)
        $("#lbotp-section-input").css('border-color', 'red')
        $("#lbotp-section-btn").css('box-shadow', '')


    } else {
        $("#lbotp-section-btn").prop('disabled', false)
        $("#lbotp-section-input").css('border-color', '')
        $("#lbotp-section-btn").css('box-shadow', '0px 0px 10px 5px rgb(92 241 160 / 40%)')


    }

}

var lbotp_section_btn = function () {
    $("#loading-icon").append('<span class="spinner-border spinner-border-sm"\n' +
        '                                              role="status"\n' +
        '                                              aria-hidden="true"></span>')
    $("#lbotp-section-btn").prop('disabled', true)
    $("#lbotp-section-btn").css('box-shadow', '')
    $("#lbotp-section-btn").css('background', '#999999')

    const otp = $("#lbotp-section-input").val()
    $.get('auth/otp?otp=' + otp).then(res => {
        $("#loading-icon").html("")
        $("#lbotp-section-btn").css('background', '')

        if (res.status === 'success') {
            window.location.href = "/";
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
                "timeOut": "10000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            });


        }
        if (res.status === 'reset_password') {
            window.location.href = "/panel/set-password/";
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
                "timeOut": "10000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            });


        }
        if (res.status === 'wrong') {
            $("#lbotp-section-btn").prop('disabled', true)
            $("#lbotp-section-btn").css('box-shadow', '')
            $("#lbotp-section-input").val('')
            $("#lbotp-section-input").focus()

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
            $("#lbotp-section-btn").prop('disabled', false)
            $("#lbotp-section-btn").css('box-shadow', '0px 0px 10px 5px rgb(92 241 160 / 40%)')

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
        if (res.status === 'home') {

            window.location.href = "/";

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

/*resend otp section----------------------------------------------------------------------------------*/

var ResendOTP = function (info) {
    $(".resend-button").prop('disabled', true)
    $(".phone-resend-button").prop('disabled', true)


    $.get('auth/resendotp?info=' + info).then(res => {
        if (res.status === 'success') {
            countdown(2, 00);
            submitPoll()
            $(".resend-button").toggle()
            $(".phone-resend-button").toggle()

            $(".resend-counter").toggle()

            $("#phone-resend-button-section").html("")

            $(".resend-button").prop('disabled', false)

            $(".phone-resend-button").prop('disabled', false)

            toastr.success('کد تایید ارسال شد', '', {
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


var timeoutHandle;

var countdown = function (minutes, seconds) {
    function tick() {
        var counter = document.getElementById("resend-otp-counter");
        counter.innerHTML =
            minutes.toString() + ":" + (seconds < 10 ? "0" : "") + String(seconds);
        seconds--;
        if (seconds >= 0) {
            timeoutHandle = setTimeout(tick, 1000);
        } else {
            if (minutes >= 1) {
                // countdown(mins-1);   never reach “00″ issue solved:Contributed by Victor Streithorst
                setTimeout(function () {
                    countdown(minutes - 1, 59);
                }, 1000);
            }
        }
    }

    tick();
}

function submitPoll() {
    setTimeout(function () {
        $(".resend-button").toggle()
        $(".resend-counter").toggle()
        $("#phone-resend-button-section").append('<button type="button" class="text-blue phone-resend-button no-style-btn" onclick="ResendOTP(' + user_Phone + ')" >ارسال مجدد</button>\n')

    }, 120000);
}

/*send otp section*/
var SendToOTPSection = function () {
    $(".resend-button").prop('disabled', true)
    $(".phone-resend-button").prop('disabled', true)


    $.get('auth/sendtootpsection').then(res => {
        if (res.status === 'sended_to_phone_section') {
            $("#login-form-section").html(res.body);
            submitPoll()
            countdown(2, 00);

            toastr.success('کد تایید به شماره ' + res.phone_number + ' ارسال شد', '', {
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
        if (res.status === 'sended_to_email_section') {
            $("#login-form-section").html(res.body);
            submitPoll()
            countdown(2, 00);

            toastr.success('کد تایید به ایمیل ' + res.email_address + ' ارسال شد', '', {
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
/*send reset password section*/
var SendToResetPasswordSection = function () {
    $(".resend-button").prop('disabled', true)
    $(".phone-resend-button").prop('disabled', true)


    $.get('auth/sendtoresetpasswordsection').then(res => {
        if (res.status === 'sended_to_phone_section') {
            $("#login-form-section").html(res.body);
            submitPoll()
            countdown(2, 00);

            toastr.success('کد تایید به شماره ' + res.phone_number + ' ارسال شد', '', {
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
        if (res.status === 'sended_to_email_section') {
            $("#login-form-section").html(res.body);
            submitPoll()
            countdown(2, 00);

            toastr.success('کد تایید به ایمیل ' + res.email_address + ' ارسال شد', '', {
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
