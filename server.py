from cpr_app import app

#撮影した動画を格納するパス
app.config['UPLOAD_FOLDER'] = 'cpr_app/uploads'
#許可する拡張子をまとめたもの
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mkv'}
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024


#解析中の出力をまとめたパス CSV_PASSの後ろには動画名を足す
app.config['OUTPUT_ANALYZING_PATH'] = "cpr_app/output_analyzing"
#htmlで出力する結果を保存するjsonファイル
app.config['JSON_ANALYZING_RESULT'] = "cpr_app/output_analyzing/json/result.json"
#現在の進捗を保存するjsonファイル
app.config['JSON_ANALYZING_PROGRESS'] = "cpr_app/output_analyzing/json/progress.json"

#webに出力したいデータを保存するパス
app.config['RESULT_PATH'] = "cpr_app/static/result"


app.config['RESULTS_FOLDER_PATH'] = "cpr_app/results"
app.config['RESULTS_INFORMATION_JSON'] = "cpr_app/results/results.json"


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