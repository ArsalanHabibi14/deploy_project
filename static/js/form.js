$(document).ready(function () {
        $("#answer-to-comment").toggle();
    $("#remove-answer-to-comment").click(function (){
            $("#answer-to-comment").toggle();
         $('#parent_id').val("");

    })
     $(function () {
        $("#contactsubmit").css('background','#999999');
        $("#contactsubmit").prop('disabled',true);

        $('#contactformmessage,#contactformemail,#contactformphone,#contactformsubject').keyup(function () {
            if ($('#contactformemail').val() != '' && $('#contactformphone').val() != '' && $('#contactformsubject').val().length >= 5 && $('#contactformmessage').val().length >= 10) {
                 $("#contactsubmit").css('background','');
                $("#contactsubmit").prop('disabled',false);

            } else {
                 $("#contactsubmit").css('background','#999999');
                 $("#contactsubmit").prop('disabled',true);
            }
        });
    });

        $(function () {
        $('#emailsignsubmit').attr('disabled', true);
                        $('#emailsignsubmit').css('background-color', 'gray');

        $('#emailsigninput').change(function () {
            if ($('#emailsigninput').val() == '') {
                $('#emailsignsubmit').attr('disabled', true);
                                        $('#emailsignsubmit').css('background-color', 'gray');

            }
        });
    });
    $("#emailsigninput").keyup(function () {
        if (validateEmail()) {
            $("#emailsigninput").css("border", "1px solid green");
            $('#emailsignsubmit').attr('disabled', false);
                        $('#emailsignsubmit').css('background-color', '');

        } else {
            $("#emailsigninput").css("border", "1px solid red");
            $('#emailsignsubmit').attr('disabled', true);
                        $('#emailsignsubmit').css('background-color', 'gray');

        }

    });
        function validateEmail() {
        var email = $("#emailsigninput").val();
        var reg = /^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/
        if (reg.test(email)) {
            return true;

        } else {
            return false;
        }
    }


});
function SubmitSignEmail() {
    const email = $('#emailsigninput').val();

    $.get('/submit-sign-email?email=' + email).then(res => {
        if (res.status === 'success') {
            $('#emailsigninput').val("");
            $("#emailsignsubmit").attr("disabled", true);
            $("#emailsigninput").attr("disabled", true);
            toastr.success(res.title,'', {
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


var elementOld = null;
var openClass = "Accordion__tab--open";

function toggleAccordion(element) {
    content = element.querySelector(".Accordion__tab__content");

    if(elementOld != null){
        elementOld.classList.remove(openClass);
        contentOld = elementOld.querySelector(".Accordion__tab__content");
        contentOld.style.maxHeight = "0px";
    }

    if(elementOld !== element){
        element.classList.add(openClass);
        content.style.maxHeight = content.scrollHeight + "px";
        elementOld = element;
    }else{
        elementOld = null;
    }
}


function sendBlogComment(blogId){
    var comment = $('#blogComment').val();
    var parentId = $('#parent_id').val();

    $.get('/blog/add-blog-comment',{
        blog_comment: comment,
        blog_id: blogId,
        parent_id: parentId,
    }).then(res => {
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
                "timeOut": "3000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut",
            });

        }else {
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
                "timeOut": "3000",
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

function fillParentid(parentId){
    $('#parent_id').val(parentId);
        $("#answer-to-comment").toggle();

    $('html,body').animate({
        scrollTop: $("#comment-form").offset().top
    },500);
}


function SendProductComment(productId){
        var score = $('#productCommentScore').val();
        var suggest = $('#productCommentSuggest').val();
        var message = $('#productCommentMessage').val();
        $('#sendProductCommentButton').prop('disabled',true)

        $.get('/products/add-product-comment',{
        product_comment: message,
        comment_score: score,
        comment_suggest: suggest,
        product_id: productId,
    }).then(res => {
        if (res.status === 'success') {
            $('#sendProductCommentButton').prop('disabled',true)

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
                "timeOut": "3000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut",
                onHidden: function () {
                    location.reload();
                }
            });

        }else {
                    $('#sendProductCommentButton').prop('disabled',false)

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
