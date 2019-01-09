$(document).ready(function () {
    var num = 0;


    var ulist = $(".foucsBox ul>li").length;
    //自动轮播
    timer = setInterval(bannertimer, 5000);
    //
    function bannertimer() {
        num++;
        if (num > (ulist - 1)) {
            num = 0;
        }
        $(".foucsBox ul>li").eq(num).fadeIn(250).siblings().fadeOut(250);
    }

    //鼠标停留在图片上时,暂停播放；离开时继续
    $(".foucsBox ul>li").on("mouseenter", function () {
        clearInterval(timer);
    })
        .on("mouseleave", function () {
            clearInterval(timer);
            timer = setInterval(bannertimer, 5000);
        });

    // 点击左边的按钮
    $(".lbtn").click(function () {
        // console.log(num);
        num -= 1;
        if (num < 0) {
            num = ulist - 1;
        }
        $(".foucsBox ul>li").eq(num).fadeIn(250).siblings().fadeOut(250);
    });

    // 点击右边的按钮
    $(".rbtn").click(function () {
        // console.log(num);
        num += 1;
        if (num > (ulist - 1)) {
            num = 0;
        }
        $(".foucsBox ul>li").eq(num).fadeIn(250).siblings().fadeOut(250);
    });
});