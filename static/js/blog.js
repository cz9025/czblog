$(document).ready(function () {

    // 我的博客，分页
    $('#pageBtn').click(function () {
        var nu = $("#gotoPage").val();
        console.log(nu);
        if (nu<1){
            nu=1
        }
        $(this).attr('href','?page='+nu);

    });

    // 置顶功能  这个要重新做，这里只是调试
    // $(".feedlist_id>li:first>h2").append("<span></span>");
		
});