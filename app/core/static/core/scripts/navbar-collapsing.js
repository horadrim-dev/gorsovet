var autocollapse = function (menubar) {
    var menu = menubar.find("#main-menu");
    var menu_items = menu.find(" > li:not(#more)");
    var more = menu.find(" > li#more");
    more.removeClass("hidden");
    
    if ($("body").width() > 994){
        var logo_block = menubar.find(".navbar-header")
        var right_block = menubar.find(".navbar-right")
        var hidden_menu_items = more.find("ul > li");
        var available_space = menubar.width() - logo_block.width() - right_block.width() - more.width();
        var cnt = 0;
        menu_items.each(function(index, value){
            $(this).removeClass("hidden");
            var isLastElement = index == menu_items.length - 1;
            cnt += $(this).width();
            if (cnt > available_space) {
                menu_items.slice( menu_items.index(this) )
                    .each(function(){$(this).addClass("hidden")});
                hidden_menu_items.slice(0, menu_items.index(this) )
                    .each(function(){$(this).addClass("hidden")});
                hidden_menu_items.slice(menu_items.index(this) )
                    .each(function(){$(this).removeClass("hidden")});
                return false; //exiting loop
            } else {
                if (isLastElement) {
                    more.addClass("hidden");
                }
            }
        });
    }
    else {
        menu_items.each(function(index, value){
            $(this).removeClass("hidden");
        });
        more.addClass("hidden");
    }
};

$(document).ready(function () {
    // when the page laods
    autocollapse( $('.navbar-main .container')); 
    
    // when the window is resized
    $(window).on('resize', function () {
        // autocollapse('#main-menu',50); 
        autocollapse( $('.navbar-main .container')); 
    });

});