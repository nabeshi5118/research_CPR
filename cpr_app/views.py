from cpr_app import app
from flask import Flask,g, render_template, request, redirect, url_for, flash, jsonify,current_app
import os, glob
import cv2
import asyncio
import shutil
from datetime import datetime
from .analyze_yolo import write_csv_yolo_cpr
from .analyze_yolo import plot_csv
from .analyze_yolo import reconstruction_video
from .config_json import ConfigJson
from .delete_cache import DeleteCache

from .data.video_data import VideoData

#allowed_extensionsにある有効な拡張子を持つ場合にTrueを返す
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def initialize_file():
  for file in glob.glob('cpr_app/outputs/**/*', recursive=True):
    try :
      os.remove(file)
    except IsADirectoryError :
      print()

#user_nameがない場合に日時を名前として作成する
def make_username():
  now = datetime.now()
    # フォーマットして文字列として返す
  return now.strftime('%Y_%m_%d_%H_%M')
import os

def create_folder(directory, folder_name):
    """
    指定したパスに指定した名前のフォルダを作成し、そのパスを返します。
    """
    folder_path = os.path.join(directory, folder_name)
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"フォルダを作成しました: {folder_path}")
    except Exception as e:
        print(f"フォルダ作成中にエラーが発生しました: {e}")
    return folder_path

# @app.before_request
# def before_request():
#   #g.my_object = PeakDataOutput()
#   print("peak before")

#最初に飛ぶ所
@app.route('/')
def index():
  my_dict = {}
  initialize_file()
  cj = ConfigJson(app.config['JSON_ANALYZING_PROGRESS'])
  cj.add({'message':'',"progress":0,"step":0})
  # my_dict = {
  #   'insert_something1': 'views.pyのinsert_something1部分です。',
  #   'insert_something2': 'views.pyのinsert_something2部分です。',
  #   'test_titles': ['title1', 'title2', 'title3']
  # }
  return render_template('cpr_app/upload.html', my_dict=my_dict)

# 評価画面の見方ページ
@app.route('/guide')
def guide():
    return render_template('cpr_app/guide.html')

# 胸骨圧迫のコツページ
@app.route('/tips')
def tips():
    return render_template('cpr_app/tips.html')

@app.route('/clear_cache', methods=['POST'])
def clear_cache():
    # キャッシュ削除処理（例として簡単なメッセージ表示）
    cache = DeleteCache()
    cache.delete_cache()
    print("キャッシュが削除されました。")
    return render_template('cpr_app/upload.html', message="キャッシュを削除しました。")

# 履歴ページ
@app.route('/history')
def history():
    RIJ = ConfigJson(app.config['RESULTS_INFORMATION_JSON'])
    results_dict = RIJ.dict()
     # JSONのキー（タイムスタンプ）だけを抽出
    timestamps = list(results_dict.keys())
    return render_template('cpr_app/history.html', timestamps=timestamps)

@app.route('/clear_history', methods=['POST'])
def clear_history():
    # キャッシュ削除処理（例として簡単なメッセージ表示）
    cache = DeleteCache()
    cache.delete_history()
    print("履歴が削除されました。")
    return render_template('cpr_app/history.html', message="履歴を削除しました。")

@app.route('/select_date', methods=['POST'])
def select_date():
    selected_date = request.form.get('timestamp')
    RIJ = ConfigJson(app.config['RESULTS_INFORMATION_JSON'])
    results_dict = RIJ.dict()
    if selected_date and selected_date in results_dict:
        # 選択された日付に応じた処理（例：詳細ページにリダイレクト）
        shutil.copy(results_dict[selected_date]["video"],app.config['RESULT_PATH']+"/movie.MP4")
        shutil.copy(results_dict[selected_date]["graph"],app.config['RESULT_PATH']+"/graph.png")
        RI = ConfigJson(results_dict[selected_date]["json"])
        return render_template('cpr_app/finish.html', result=RI.dict())
    return redirect(url_for('history'))



#ファイルアップロード時の状態を確認する関数
#@app.route('/analyze/<filename>')　ここに飛ぶ
#
@app.route('/upload', methods=['POST'])
def upload_file():
  II = ConfigJson(app.config['INPUT_INFO'])
  cache = DeleteCache()
  cache.delete_cache()
  sample_Filepath = II.load("filepath_10")
  sample_Filename = II.load("filename_10")
  upload_folder_path = app.config['UPLOAD_FOLDER']
 #テスト用データの処理が汚いからここ直したい
  #キー名にtest_10を探している
  if II.load("name") in request.form:
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

@app.route('/analyze/<filename>')
def analyze(filename):
  template_name = 'cpr_app/analyze.html'
  template_path = os.path.join(current_app.root_path, 'templates', template_name)

    # os.path.exists() を使ってファイルの存在を確認します
  if not os.path.exists(template_path):
        # ファイルが存在しない場合、404エラーを返して処理を中断します
    print("not found")
  else:
     print("found")
  return render_template('cpr_app/analyze.html', filename=filename)

@app.route('/progress/<filename>', methods=['POST'])
def progress(filename):
  #progressの状態を保存するjsonファイル "cpr_app/output_analyzing/progress.json"
  JP = ConfigJson(app.config['JSON_ANALYZING_PROGRESS'])
  JAR = ConfigJson(app.config['JSON_ANALYZING_RESULT'])
  #output_analyzingのフォルダ
  RJ = ConfigJson(app.config['RESULTS_INFORMATION_JSON'])
  #JR = ConfigJson(app.config['JSON_RESULT'])
  rj_dict = RJ.dict()
  #記録を保存する用のフォルダを作成する
  user_file = make_username()
  upload_video_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
  print(upload_video_path)
  video = VideoData(upload_video_path)
  analyzing_folder_path = app.config['OUTPUT_ANALYZING_PATH']
  #webに出力する用
  output_analyzing_graph_path = app.config['RESULT_PATH'] + "/graph.png"
  output_analyzing_movie_path = app.config['RESULT_PATH'] + "/movie.MP4"
  #resultsに保存するときのパス
  result_save_path = create_folder(app.config['RESULTS_FOLDER_PATH'],user_file)
  rj_dict[user_file] = {
     "graph":os.path.join(result_save_path,"graph.png"),
     "video":os.path.join(result_save_path,"movie.MP4"),
     "json":os.path.join(result_save_path,"results.json")
  }
  RJ.add(rj_dict)
  #追加してほしいとろろにそれぞれパスあある
  output_video_path = rj_dict[user_file]["video"]
  output_graph_path = rj_dict[user_file]["graph"]
  output_json_path = rj_dict[user_file]["json"]

  #実際には、姿勢推定しつつ、csvに書き込んでいる
  JP.add({'message':'Pose Estimate',"progress":0,"step":1})
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
