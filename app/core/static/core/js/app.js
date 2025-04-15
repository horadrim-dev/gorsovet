(function($) {
    var original_onPageLoad = $.fn.onPageLoad;
    $.fn.onPageLoad = function () {
        original_onPageLoad();

        // ==================TOASTR==========================
        toastr.options = {
            "closeButton": false,
            "debug": false,
            "newestOnTop": false,
            "progressBar": true,
            "positionClass": "toast-bottom-right",
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
        };
        // запускаем событие resize, для перерисовки страницы (в частности для меню схлопывания navbar-collapsing.js)
        // $(window).trigger('resize');

        // COPY-URL-BUTTONS
        $.fn.copyToClipboard = function (url) {
            var inp = document.createElement('input');
            inp.value = url;
            document.body.appendChild(inp);
            inp.select();
            if (document.execCommand('copy')) {
                toastr.success("Ссылка скопирована в буфер обмена");
            } else {
                toastr.error("Не удалось скопировать ссылку");
            }
            document.body.removeChild(inp);
        }
        $(".copy-url").on('click', function (e) {
            e.preventDefault();
            var url = $(this).attr("data-url");
            $(this).copyToClipboard(url);
        });
    };
})(jQuery || django.jQuery);
