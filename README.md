# flaskを用いたWebアプリケーションについて
m5291086(s1290148) 渡辺涼太

## 実行方法
1. まず、docker-composeを使って、仮想コンテナを作成、起動します
2. 

## ディレクトリ構成
analyze #研究のときに使用。web appでは使わない<br>
├── ...<br>
:  

flask_web_app  
├── cpr_app # 下に記載     
│   :      
│   └──...  
├── debug  
│   └── debug_10.mp4 #デバックの際に使用する動画  
├── model #YOLOのモデルを保存する場所  
│   └── YOLO~.pt  
├── delete_cache.py #キャッシュデータを削除するときに使う  
├── sercer.py # webアプリ起動時に使う  
├── util.py # webアプリで使う便利機能を保存している  
├── docker-compose.yml   
├── Dockerfile-flask-yolo  
├── requirement-flask.txt  
├── .bashrc  
├── .gitattributes  
├── .gitignore  
└── README.md  

 cpr_app    
├── analyze_yolo# YOLOでのキーポイント推定で使う  
│   ├── rotate_video.py  
│   └── write_csv_yolo_cpr.py  
├── evaluate_csv #キーポイント推定されたデータを解析する    
│   ├── calculate_appro_peak.py  
│   ├── calculate_appro_tempo.py  
│   ├── calculate_mean_tempo.py  
│   ├── calculate_peak.py  
│   ├── calculate_treshold.py  
│   └── evaluate_csv.py  
├── make_result#結果を作成するときに使う    
│   ├── make_result_data.py  
│   └── reconstruction_video.py  
├── results #キャッシュ削除を実施すると、中身がすべて消える  
│   ├── # ここに解析結果が保存される  
│    :  
│   └── records.json #解析結果を取り扱うjson  
├── static  
│   ├── result #画面の見方ページで使用、サンプル動画と画像   
│   │   ├── sample_graph.png    
│   │   └── sample_movie.MP4  
│   ├── progress.js # 進捗を進捗バーにして表示するためのコード  
│   └── styles.css  
├── templates  
│   └── cpr_app  
│        ├── analyze.html  
│        ├── finish.html  
│        ├── guide.html  
│        ├── history.html  
│        ├── tips.html      
│        └── upload.html  
├── uploads # 投稿された動画を保存する場所   
├── model.py  #推定に使うための情報を保存するための  
├── services.py  # 解析を実際に行う部分  
├── values.py  #固定値を保存する場所  
└── views.py #flaskアプリのサーバー部分   




## 機能実装したいことリスト
* ユーザーネームで履歴を探せる
* plot_csv_data内にある評価手段を確立させる