jQuery(function () {
  var webStorage = function () {
    if (sessionStorage.getItem('access')) {
      //2回目以降アクセス時の処理
      $('.start').addClass('is-active')
    } else {
      sessionStorage.setItem('access', 0);
      setTimeout(function(){
        $('.start p').fadeIn(1600);
      },500); //0.5秒後にロゴをフェードイン
      setTimeout(function(){
        $('.start').fadeOut(500);
      },2500);
    }
  }
  webStorage();
});

// $(function() {
// 	setTimeout(function(){
// 		$('.start p').fadeIn(1600);
// 	},500); //0.5秒後にロゴをフェードイン!
// 	setTimeout(function(){
// 		$('.start').fadeOut(500);
// 	},2500); //2.5秒後にロゴ含め真っ白背景をフェードアウト！
// });


// $(function() {
//   alert('OK!');
// });