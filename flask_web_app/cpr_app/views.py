from cpr_app import app
from flask import Flask,g, render_template, request, redirect, url_for, flash, jsonify,current_app,send_from_directory
import os, glob
import cv2
import asyncio
import shutil
from datetime import datetime
from .analyze_yolo import write_csv_yolo_cpr
from .analyze_yolo import plot_csv
from .analyze_yolo import reconstruction_video
from .config_json import ConfigJson
from delete_cache import DeleteCache

from util import Config
from util import ConfigJson

from .services import AnalysisService # 新しくインポート
from .models import VideoData

#allowed_extensionsにある有効な拡張子を持つ場合にTrueを返す
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def initialize_file(tmp):
  path = tmp + "/**/*"
  for file in glob.glob(path, recursive=True):
    try :
      os.remove(file)
    except IsADirectoryError :
      print()

#user_nameがない場合に日時を名前として作成する
def make_username():
  now = datetime.now()
    # フォーマットして文字列として返す
  return now.strftime('%Y_%m_%d_%H_%M')

# @app.before_request
# def before_request():
#   #g.my_object = PeakDataOutput()
#   print("peak before")

#最初に飛ぶ所
@app.route('/')
def index():
  my_dict = {}
  initialize_file(app.config['CACHE_PATH'])
  cj = ConfigJson(app.config['CACHE_ANALYZE_PROGRESS'])
  cj.add({'message':'',"progress":0,"step":0})

  return render_template(app.config['UPLOAD_HTML_PATH'], my_dict=my_dict)

#upload.htmlからanalyze.html画面に飛ぶときに使う
@app.route('/analyze/<filename>')
def analyze(filename):
  #解析画面に飛ぶ前にやりたいことがあればする場所
  return render_template(app.config['ANALYZE_HTML_PATH'], filename=filename)

# 評価画面の見方ページ
@app.route('/guide')
def guide():
    return render_template(app.config['GUIDE_HTML_PATH'])

# 胸骨圧迫のコツページ
@app.route('/tips')
def tips():
    return render_template(app.config['TIPS_HTML_PATH'])

@app.route('/clear_cache', methods=['POST'])
def clear_cache():
    # キャッシュ削除処理（例として簡単なメッセージ表示）
    cache = DeleteCache()
    cache.delete_cache()
    print("キャッシュが削除されました。")
    return render_template(app.config['UPLOAD_HTML_PATH'], message="キャッシュを削除しました。")

# 履歴ページ
@app.route('/history')
def history():
    RIJ = ConfigJson(app.config['RESULTS_JSON'])
    results_dict = RIJ.dict()
     # JSONのキー（タイムスタンプ）だけを抽出
    timestamps = list(results_dict.keys())
    return render_template(app.config['HISTORY_HTML_PATH'], timestamps=timestamps)

@app.route('/clear_history', methods=['POST'])
def clear_history():
    # キャッシュ削除処理（例として簡単なメッセージ表示）
    cache = DeleteCache()
    cache.delete_history()
    print("履歴が削除されました。")
    return render_template(app.config['HISTORY_HTML_PATH'], message="履歴を削除しました。")

# views.py
@app.route('/select_date', methods=['POST'])
def select_date():
    selected_date = request.form.get('timestamp')
    RIJ = ConfigJson(app.config['RESULTS_JSON'])
    results_dict = RIJ.dict()
    if selected_date and selected_date in results_dict:
        # ★★★★★ ここから修正 ★★★★★
        
        # 1. コピー先のディレクトリパスを取得
        destination_dir = app.config['OUTPUT_ANALYZING_RESULT_PATH']
        
        # 2. util.pyの関数を使って、ディレクトリが存在することを保証する
        Config.create_directory(destination_dir)
        
        # 3. これで安全にファイルをコピーできる
        #    (os.path.joinを使うとより安全にパスを結合できます)
        shutil.copy(results_dict[selected_date]["video"], os.path.join(destination_dir, "movie.MP4"))
        shutil.copy(results_dict[selected_date]["graph"], os.path.join(destination_dir, "graph.png"))
        
        # ★★★★★ ここまで修正 ★★★★★

        RI = ConfigJson(results_dict[selected_date]["json"])
        return render_template('cpr_app/finish.html', result=RI.dict())
    return redirect(url_for('history'))



#ファイルアップロード時の状態を確認する関数
#@app.route('/analyze/<filename>')　ここに飛ぶ
@app.route('/upload', methods=['POST'])
def upload_file():
  cache = DeleteCache()
  cache.delete_cache()
  sample_Filepath = app.config['DEBUG_VIDEO_PATH']
  sample_Filename = Config.get_filename(sample_Filepath)
  sample_Filename_only = Config.get_filename(sample_Filepath,True)#ファイル名のみ
  upload_folder_path = app.config['CACHE_UPLOAD_PATH']


  #キー名にtest_10を探している
  #ファイル名がdebugのファイルの場合
  if sample_Filename_only in request.form:
    print("テストデータ Test data")
    shutil.copy(sample_Filepath,upload_folder_path)
    flash('アップロードが成功しました Success', 'success')
    print("アップロード成功")
    return redirect(url_for('analyze', filename=sample_Filename))
  
  if 'file' not in request.files:
    flash('ファイルが選択されていません File not selected', 'error')
    return redirect(request.url)

  file = request.files['file']
  if file.filename == '':
    flash('ファイル名が空です File name empty', 'error')
    return redirect(request.url)

  if file and allowed_file(file.filename):
    filepath = os.path.join(upload_folder_path, file.filename)
    file.save(filepath)
    flash('アップロードが成功しました success', 'success')
    return redirect(url_for('analyze', filename=file.filename))
  else:
    flash('許可されていないファイル形式です Unauthorized file format.', 'error')
    return redirect(request.url)


@app.route('/progress/<filename>', methods=['POST'])
def progress(filename):
  #progressの状態を保存するjsonファイル "cpr_app/output_analyzing/progress.json"
  AP = ConfigJson(app.config['CACHE_ANALYZE_PROGRESS_JSON'])# JP
  AR = ConfigJson(app.config['CACHE_ANALYZE_RESULT_JSON'])#JAR

  #記録を保存する用のフォルダを作成する
  #将来的にusernameからソートできるようにしたい
  user_file = make_username()#現状は日時をユーザーネームにしている


  upload_video_path = os.path.join(app.config['CACHE_UPLOAD_PATH'],filename)
  #video情報を保存するクラス
  video = VideoData(upload_video_path)
  
  analyzing_folder_path = app.config['CACHE_UPLOAD_PATH']#analyzing_folder_path = app.config['OUTPUT_ANALYZING_RESULT_PATH']
  #webに出力する用
  output_movie = app.config['CACHE_OUTPUT_MOVIE'] #output_analyzing_graph_path = app.config['OUTPUT_ANALYZING_RESULT_PATH'] + "/graph.png"
  output_graph = app.config['CACHE_OUTPUT_GRAPH'] #output_analyzing_movie_path = app.config['OUTPUT_ANALYZING_RESULT_PATH'] + "/movie.MP4"
  
  #結果を保存する際の前処理
  #resultsに保存するときのパス
  RJ = ConfigJson(app.config['RESULTS_RECORD_JSON'])
  rj_dict = RJ.dict()
  result_save_path = Config.create_directory(app.config['RESULTS_FOLDER_PATH'],user_file)
  video_record = app.config['VIDEO_RECORD_NAME']  
  graph_record = app.config['GRAPH_RECORD_NAME'] 
  result_record = app.config['RESULT_RECORD_NAME']
  result_paths = {
     os.path.splitext(os.path.basename(graph_record))[0]:os.path.join(result_save_path,graph_record),#graph_record:"path/to/graph_record"
     os.path.splitext(os.path.basename(video_record))[0]:os.path.join(result_save_path,video_record),
     os.path.splitext(os.path.basename(result_record))[0]:os.path.join(result_save_path,result_record)
  }
  rj_dict[user_file] = result_paths
  RJ.add(rj_dict)
  #追加してほしいとろろにそれぞれパスあある
  save_video_path = rj_dict[user_file]["video"]#output_video_path
  save_graph_path = rj_dict[user_file]["graph"]
  save_json_path = rj_dict[user_file]["json"]


  analysis_service = AnalysisService(video, app.config, result_paths)
  analysis_service.run_full_analysis()

  exe = write_csv_yolo_cpr.YOLOv8Estimator(upload_video_path,analyzing_folder_path,error_message=app.config['ERROR_MESSAGE'])
  exe.estimation_algorithm(app.config['JSON_ANALYZING_PROGRESS'],video.flame)
  csv_paths,cache_path = exe.return_paths()
  JP.add({"progress":100})
  print("finish step1")


  JP.add({'message':'Analyze Data',"progress":0,"step":2})
  #ここに本来データ解析(plot_csv.pyの前半部分)が入るはず
  JP.add({"progress":100})
  print("finish step2")
    

  JP.add({"message":"Make Graph","progress":0,"step":3})
  #キーポイントは10番の右手首で行ってみる(要確認)

  keypoint = 10
  window_size = 10
  print("video time"+str(video.time))
  plot_csv.plot_csv_data(csv_filename=csv_paths[keypoint] , fps =video.fps ,time=video.time, window_size=window_size,output_graph_path = output_analyzing_graph_path,analyzing_result_json=app.config['JSON_ANALYZING_RESULT'])
  JP.add({"progress":100})
  print("finish step3")


  JP.add({'message':'Make Movie',"progress":0,"step":4})
  reconstruction_video.make_video(cache_path , output_analyzing_movie_path ,video.fps)
  JP.add({"progress":100})
  print("finish step4")

  #結果をresultsの方にも保存しておく
  JAR.add({'message':"Finished Analyze"})
  shutil.copy(app.config['JSON_ANALYZING_RESULT'],output_json_path)
  shutil.copy(output_analyzing_graph_path,output_graph_path)
  shutil.copy(output_analyzing_movie_path,output_video_path)

  #ここでjson形式でresponceをjsに飛ばしている
  return jsonify(JP.dict())

#現在の進捗を更新する
@app.route('/progress_status/<filename>', methods=['GET'])
def progress_status(filename):
    try:
        status =  ConfigJson(app.config['JSON_ANALYZING_PROGRESS'])
        print(status.dict)
        print("進捗get中")
        return jsonify(status.dict())
    except FileNotFoundError:
        return jsonify({'progress': 0, 'message': '進捗情報が見つかりませんでした。'})



@app.route('/finish', methods=['GET'])
def finish():
  # ここで処理結果を取得するか、適切な方法で表示用のデータを用意
  print("finish来たよ")
  
  #余裕があればここを"result.json"にしたい
  CJ =  ConfigJson(app.config['JSON_ANALYZING_RESULT'])

  return render_template('cpr_app/finish.html', result=CJ.dict())


# output_analyzing/result フォルダ内のファイルを配信するためのルート
# views.py の serve_analyzed_file 関数を以下に置き換える

@app.route('/analyzed_files/<path:filename>')
def serve_analyzed_file(filename):
    """解析結果のファイル（画像や動画）を配信する"""
    
    # 1. configから相対パスを取得
    relative_dir = app.config['OUTPUT_ANALYZING_RESULT_PATH']
    
    # 2. プロジェクトルートを基準とした絶対パスに変換
    #    current_app.root_path は '.../cpr_app' を指すので、'..' で一つ上に行く
    absolute_dir = os.path.abspath(os.path.join(current_app.root_path, '..', relative_dir))
    
    # --- デバッグ用のprint文 ---
    full_path = os.path.join(absolute_dir, filename)
    print("--- serve_analyzed_file デバッグ情報 ---")
    print(f"設定された相対パス: {relative_dir}")
    print(f"計算された絶対パス: {absolute_dir}")
    print(f"探しているファイルのフルパス: {full_path}")
    print(f"ファイルは存在しますか？: {os.path.exists(full_path)}")
    print("------------------------------------")

    # 3. 絶対パスを使ってファイルを安全に配信
    return send_from_directory(absolute_dir, filename)
