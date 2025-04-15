(function($) {

    var original_onPageLoad = $.fn.onPageLoad;
    $.fn.onPageLoad = function () {
        original_onPageLoad();

        $(".news-container button.layout-toggler").click(function(){
            setCookie('news_list_layout', $(this).attr("data"), 7, path=$(this).attr("path"));
            window.location.reload();
        });

        $('#news-filter input.autoapply').on('change', function() {
            $(this).closest("form").submit();
            
        });
        $('#news-filter input#filter-reset').on('click', function() {
            $(this).closest("form").reset();
            //$(this).closest("form").find('input:not([type="submit"])').val('');
        });

        $(".news-container #filter-toggler").click(function(){
            $("#news-content").toggleClass("col-md-8");
            $("#news-sidebar").toggleClass("hidden"); 

            if ($("#news-sidebar").hasClass("hidden")) {
                setCookie('news_filter_state', "hidden", 7, path=$(this).attr("path"));
                $(".news-container #filter-toggler").html("<i class=\"fa fa-filter\"></i>");
            } else {
                setCookie('news_filter_state', "visible", 7, path=$(this).attr("path"));
                $(".news-container #filter-toggler").html("<i class=\"fa fa-angle-left\"></i>");
            }
            // вызываем ивент для перестроения контента
            window.dispatchEvent(new Event('resize'));
        });
    };
})(jQuery || django.jQuery);
