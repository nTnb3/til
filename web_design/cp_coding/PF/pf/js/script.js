$(function () {

  //ページ内スクロール
  var navHeight = $(".header").outerHeight();

  $('a[href^="#"]').on("click", function () {
    var href = $(this).attr("href");
    var target = $(href == "#" || href == "" ? "html" : href);
    var position = target.offset().top - navHeight;
    $("html, body").animate({ scrollTop: position, }, 300, "swing");
    return false;
  });

  //ページトップ
  $("#js-page-top").on("click", function () {
    $("body,html").animate({ scrollTop: 0, }, 300);
    return false;
  });

});

$(function(){
    $("#open").show();
    $("#close").hide();
  // アイコンをクリック
  $("#open").click(function(){
  // ulメニューを開閉する
  $("#navi").slideToggle();
    $("#open").hide();
    $("#close").show();
  });
    
  // アイコンをクリック
  $("#close").click(function(){
  // ulメニューを開閉する
  $("#navi").slideToggle();
    $("#open").show();
    $("#close").hide();
  });

});

$(function(){
	// メニューをクリック
	$("a[href*=#]:not([href=#])").click(function(){
		// 移動先のコンテンツ位置を取得
		var target = $($(this).attr("href")).offset().top;
		// 50px減らす
		target -= 50;
		// 各コンテンツへスクロール
		$("html, body").animate({scrollTop: target}, 500);
		return false;
	});
});
