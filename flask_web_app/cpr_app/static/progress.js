// static/progress.js

// サーバーから進捗状況を取得し、進捗バーとメッセージを更新する関数
async function checkProgress(filename) {

  let currentStep = 0;
  //current stepはviews.pyで動かしているstepと連動している
  while (currentStep < 4) {
    try {
      const response = await fetch(`/progress_status/${filename}`, {
        method: 'GET'
      });
      //jsonからデータを入手して反映している
      const data = await response.json();
      console.log('message:', data.message, 'progress:', data.progress);
      document.getElementById('message').textContent = data.message;
      document.getElementById('progress').style.width = data.progress + '%';

      if (data.progress >= 100 && data.step > currentStep) {
        currentStep = data.step;
        if (currentStep === 4) {
          console.log('All tasks completed');
          return 1;
        }
      }
    } catch (error) {
      console.error('Error checking progress:', error);
      break;
    }
    await new Promise(resolve => setTimeout(resolve, 1000));  // 1秒待機
  }
}

// サーバーに処理の開始を要求し、進捗状況のチェックを開始する関数
async function startProcessing(filename) {
  // サーバーのエンドポイントにPOSTリクエストを送信
  const response = fetch(`/progress/${filename}`, {
    method: 'POST'
    }
  );
  //ここ過剰かもだけど一応
  finish = 0
  finish = await checkProgress(filename);
  console.log("finish checkProgress")
  // すべての処理が完了したらfinish.htmlにリダイレクト
  if (finish == 1){
    window.location.href = '/finish';
  }
}


// ページが読み込まれたときに処理を開始
document.addEventListener("DOMContentLoaded", () => {
  // <body>タグのdata-filename属性からファイル名を取得
  const filename = document.querySelector('body').getAttribute('data-filename');
  startProcessing(filename);
});
