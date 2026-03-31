from cpr_app import app


#HTMLのパス
app.config['UPLOAD_HTML_PATH'] = 'cpr_app/upload.html'
app.config['GUIDE_HTML_PATH'] = 'cpr_app/guide.html'
app.config['TIPS_HTML_PATH'] = 'cpr_app/tips.html'
app.config['HISTORY_HTML_PATH'] = 'cpr_app/history.html'
app.config['ANALYZE_HTML_PATH'] = 'cpr_app/analyze.html'
app.config['ANALYZE_HTML_PATH'] = 'cpr_app/analyze.html'


#許可する拡張子をまとめたもの
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mkv'}
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

#解析、出力、保存で使われる共通のファイル名
video = "video.MP4"
graph = "graph.png"
result = "result.json"
app.config['VIDEO_NAME'] = video
app.config['GRAPH_NAME'] = graph
app.config['RESULT_NAME'] = result

#解析モデルの場所
app.config['YOLO_MODEL_PATH'] = 'model/yolov8x-pose-p6.pt'

#撮影した動画を格納するパス
app.config['CACHE_PATH'] = "cpr_app/cache" #キャッシュ全体のパス
app.config['CACHE_UPLOAD_PATH'] = 'cpr_app/cache/uploads'#uploadした動画の原型をおいておくパス
#キャッシュの中でも、解析時に使われるパス
app.config['CACHE_IMG_PATH'] = "cpr_app/cache/img"#画像のパス
app.config['CACHE_CSV_PATH'] = "cpr_app/cache/csv"#キーポイントcsvデータのパス
app.config['CACHE_TMP_PATH'] = "cpr_app/cache/tmp"#一時置き場のパス 便利に使って良いフォルダ
app.config['CACHE_CSV_EVALUATE'] = "cpr_app/cache/csv/10.csv"#今回の推定は手首

#キャッシュの中でも、web出力時に使われるパス
app.config['CACHE_OUTPUT_PATH'] = "cpr_app/cache/output"#Web出力時に一旦置く場所
app.config['CACHE_OUTPUT_MOVIE'] = "cpr_app/cache/output/" + video
app.config['CACHE_OUTPUT_GRAPH'] = "cpr_app/cache/output/" + graph

app.config['CACHE_ANALYZE_RESULT_JSON'] = "cpr_app/cache/analyze/result.json"#htmlで出力する結果を保存するjsonファイル
app.config['CACHE_ANALYZE_PROGRESS_JSON'] = "cpr_app/cache/analyze/progress.json"#現在の進捗を保存するjsonファイル

#Webアプリで出された後の結果を保管する場所
app.config['RESULTS_PATH'] = "cpr_app/results"
app.config['RESULTS_RECORDS_JSON'] = "cpr_app/results/records.json"
app.config['VIDEO_RECORD_NAME'] = "video_record.MP4"
app.config['GRAPH_RECORD_NAME'] = "graph_record.png"
app.config['RESULT_RECORD_NAME'] = "result_record.json"



#ここから過去のコード
#解析中の出力をまとめたパス CSV_PASSの後ろには動画名を足す
app.config['OUTPUT_ANALYZING_PATH'] = "cpr_app/output_analyzing"
#htmlで出力する結果を保存するjsonファイル
app.config['JSON_ANALYZING_RESULT'] = "cpr_app/output_analyzing/json/result.json"
#現在の進捗を保存するjsonファイル
app.config['JSON_ANALYZING_PROGRESS'] = "cpr_app/output_analyzing/json/progress.json"

#webに出力したいデータを保存するパス
app.config['OUTPUT_ANALYZING_RESULT_PATH'] = "output_analyzing/result"

#撮影した動画を格納するパス
app.config['UPLOAD_FOLDER'] = 'cpr_app/uploads'




app.config['RESULTS_FOLDER_PATH'] = "cpr_app/results"
app.config['RESULTS_INFORMATION_JSON'] = "cpr_app/results/results.json"

#デバックデータに関する情報
app.config['DEBUG_VIDEO_PATH'] = './debug/debug_10.mp4'


#informationの情報はプログラム中で上書きしない
#テスト用データのパスについて書いてあるjson
app.config['INPUT_INFO'] = "cpr_app/information/input_info.json"

app.config['OUTPUT_INFO'] = "cpr_app/information/output_info.json"
app.config['YOLO_INFO'] =  "cpr_app/information/yolo_info.json"
app.config['PLOT_INFO'] = "cpr_app/information/plot_info.json"
app.config['ANALYZE_INFO'] = "cpr_app/information/analyze.json"

app.config['ERROR_MESSAGE'] = "yes"
app.secret_key = 'hogehoge'

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=8080)