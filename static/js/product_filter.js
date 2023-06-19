$(document).ready(function () {
    $('#loading-section').hide();




});



    const filterProducts = function () {
        var _filterObj = {};
        var _maxPrice = $(".maxPrice").val();
        var _minPrice = $(".minPrice").val();
        var _selectSort = $("#selectSort").val();
        _filterObj.maxPrice = _maxPrice;
        _filterObj.minPrice = _minPrice;
        _filterObj.selectSort = _selectSort;
        $(".filter-checkbox").each(function (index, ele) {
            var _filterVal = $(this).val();
            var _filterKey = $(this).data('filter');
            _filterObj[_filterKey] = Array.from(document.querySelectorAll('input[data-filter=' + _filterKey + ']:checked')).map(function (el) {
                return el.value;
            });
        });
        $.ajax({
            url: '/products/filter-data/',
            data: _filterObj,
            dataType: 'json',
            beforeSend: function () {
                $('#loading-section').show();
                $('#filteredProducts').hide();

            },

            success: function (res) {
                $('#filteredProducts').html(res.data);
                $('#loading-section').hide();
                $('#filteredProducts').show();
                toastr.success('تغییرات با موفقیت اعمال شد', '', {
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
    $(".filter-checkbox,#priceFilterBtn").on('click', filterProducts);
    slider.noUiSlider.on('change', filterProducts);
    $(".js-slider-range-from,.js-slider-range-to").noUiSlider.on('change', filterProducts);
    $("#selectSort").on('change', filterProducts);


slider.noUiSlider.on('change.one', filterProducts);



