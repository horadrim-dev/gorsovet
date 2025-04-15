(function($) {
    
    var original_onPageLoad = $.fn.onPageLoad;
    $.fn.onPageLoad = function () {
        original_onPageLoad();


        $("#publish-post form").on('submit', function(e){
            e.preventDefault();
            var url = $(this).attr("action");
            var data = $(this).attr("data");
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            $.ajax({
                url: url,
                method: 'post',
                headers: {'X-CSRFToken': csrftoken},
                xhrFields: { withCredentials: true },
                dataType: 'json',
                data: data,
                beforeSend: function () {
                    $("#publish-post button").css("display", "none");
                    $("#publish-post").append("<div class=\'loading\"><i class=\"fa fa-refresh fa-spin fa-1x fa-fw\"> Выполнение</i></div>");
                },
                success: function(data){

                    $("#publish-post .loading").html("");

                    switch (data.result) {
                        case "success":
                            toastr.success(data.message);
                            break;
                        case "error":
                            toastr.warning(data.message);
                            $("#publish-post button").css("display", "block");
                            break;
                        default:
                            toastr.error("Ошибка. Попробуйте обновить страницу.")
                            break;
                    }
                }
            });
        });
    }
})(jQuery || django.jQuery);
