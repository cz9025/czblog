$(function () {
    $(".ulist li:eq(0)").addClass("current");

    $(".ulist li").on("click", function () {
        $(this).addClass("current").siblings("li").removeClass("current");
        // $(".p_about").eq($(this).index()).css("display","block").siblings().css("display","none");

        //右上角的文字也要变换
        // $(".dlnews label").text($(this).children("a").children("h3").text());
    })
});