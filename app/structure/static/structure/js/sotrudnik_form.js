(function($) {
    $(document).ready(function () {
        // при выборе организации, подгружаем в поле "Отдел" список ее отделов через ajax
        // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
        $("select[name='organization']").on('change', function(){
            var url = $(this).attr("data-otdels-url");  // получаем url переданный из forms.py и отрезаем последние 2 символа, "1/"
            var orgId = $(this).val(); // get the selected org
            if (!orgId) return;
            $.ajax({
                url: url,
                data: {
                'org_id': orgId // add id to the GET parameters
                },
                success: function (res) {  
                    let options='<option value="" selected="">---------</option>';
                    res.data.forEach(otdel => {
                        options += '<option value=\"' + otdel.id +'\">' + otdel.name + '</option>';
                    });
                    $("select[name='otdel']").html(options);
                }
            });
        });
    });
})(jQuery || django.jQuery);