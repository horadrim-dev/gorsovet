(function($) {

    // var original_onPageLoad = $.fn.onPageLoad;
    // $.fn.onPageLoad = function () {
    //     original_onPageLoad();

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            };
            return cookieValue;
        }
        function setCookie(cName, cValue, expDays, path="/") {
            let date = new Date();
            date.setTime(date.getTime() + (expDays * 24 * 60 * 60 * 1000));
            const expires = "expires=" + date.toUTCString();
            document.cookie = cName + "=" + cValue + "; " + expires + "; path=" + path;
        }

        
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
            $("#news-content").toggleClass("col-md-9").toggleClass("col-md-12");
            $("#news-sidebar").toggleClass("d-none"); //.toggleClass("col-md-3"); 

            if ($("#news-sidebar").hasClass("d-none")) {
                setCookie('news_filter_state', "hidden", 7, path=$(this).attr("path"));
                $(".news-container #filter-toggler").html("<i class=\"fa fa-filter\"></i>");
            } else {
                setCookie('news_filter_state', "visible", 7, path=$(this).attr("path"));
                $(".news-container #filter-toggler").html("<i class=\"fa fa-angle-left\"></i>");
            }
            // вызываем ивент для перестроения контента
            window.dispatchEvent(new Event('resize'));
        });

        // Isotope Сетка
        // var $news_maso_grid = $('.news-maso-grid').isotope({
        //     itemSelector: '.news-maso-item', 
        //     percentPosition: true,
        // });
        // $news_maso_grid.imagesLoaded().progress( function() {
        //     $news_maso_grid.isotope('layout');
        // });
})(jQuery || django.jQuery);
