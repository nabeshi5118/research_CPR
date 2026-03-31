from PIL import Image
import numpy as np
from ultralytics import YOLO
import cv2
from cpr_app.make_result import reconstruction_video as kari
from cpr_app.analyze_yolo.rotate_video import RotateVideo
import os
import glob
import shutil
import csv
import torch
import json
import random
import os
import subprocess

from util import Config
from util import ConfigCSV

class YOLOv8Estimator:
    #input_path 動画のパス(最後が動画名.mp4)
    #output_path 結果を保存してほしい場所のパス(最後がディレクトリ名)
    #動画名のファイルが作成してあるからそこに保存しよう
    def __init__(self, input_path, output_path, model_path,error_message):
        #video videoの存在するパス
        self.input_video_path = input_path
        #csv_paths
        video_name = os.path.basename(input_path)
        self.video_name = os.path.splitext(video_name)[0]
        self.model_path = model_path

        self.key_point_num = 17


        csv_path = Config.create_directory(output_path, "csv")
        self.csv_paths = ConfigCSV.initialize_files(csv_path)
        self.img_path = Config.create_directory(output_path, "img") 
        self.json_path = Config.create_directory(output_path, "json")
        self.output_video_path = os.path.join(output_path,video_name)#output_path + '/' + video_name
        #色々なゴミを入れるパス
        #主に、回転が必要なときに使う
        self.tmp_path = Config.create_directory(output_path, "tmp")
        self.tmp_csv_paths = ConfigCSV.initialize_files(self.tmp_path)

        self.tmp_movie_name = "tmp.mp4"
        self.analyze_movie_name = "analyze.py"
        self.error_message = error_message
        print("setup YOLOv8Estimator")

    #progress: 進捗出力用jsonファイルのパス　flame: 推定写真の合計枚数 いずれもwebアプリ用
    def estimation_algorithm(self, progress=None, flame=None):
        """
        YOLOv8を使用して人体パーツの推定を行い、GUI描画と結果のCSVファイルへの書き込みを行うメソッド
        """
        print("start analyze yolo")
        #webアプリケーション用
        if progress != None:
            status = cj(progress)


        self.check_movie_aspect()
        print("check_movie_aspect")

        #webアプリケーションはviews.pyでcsvデータとフォルダを作成してい
        # Load a model
        model = YOLO(self.model_path)

        #コード内データ保存場所
        data_buffer = {i: [] for i in range(self.key_point_num)}

        # Loop through the video images
        count = 0
        cap = cv2.VideoCapture(self.output_video_path)
        while cap.isOpened():
            # Read a image from the video
            success, image = cap.read()
            if not success and count == 0:
                print("Ignoring empty camera image.")
                # If loading a video, use 'break' instead of 'continue'.
                break
            if success and count == 0:
                print("\n" + self.output_video_path + " processing ...\n")
            if not success:
                print("Finish\n")
                break

            # Run YOLOv8 inference on the image、画像をnumpyで読み込んで処理すると早くなるかも？ model.predict(np_image)
            results = model(image, verbose=False)
            #model.track(image, persist=True, half=False, conf=0.3)
            annotated_image = results[0].plot()

            # keypointsの整理
            conn_person_keypoints = []
            if len(results[0].keypoints) > 0:
                for person_keypoints in results[0].keypoints:
                    conn_person_keypoints.append(person_keypoints.data[0])
                    #print(conn_person_keypoints)
                conn_person_keypoints = torch.cat(conn_person_keypoints, 1)
                conn_person_keypoints = conn_person_keypoints.cpu().numpy()
                #print(conn_person_keypoints)

                # keypointをcsvに書き込む、
                #print(self.csv_paths)
                for i in range(self.key_point_num):
                    try:
                        keypoints = conn_person_keypoints[i]
                        data_buffer[i].append(keypoints.tolist())
                    except IndexError:
                        data_buffer[i].append(['None', 'None', 'None', 'None'])

            #cv2.imshow('YOLOv8 Inference', annotated_image)
            cv2.imwrite(self.img_path + str(format(count, '06')) + '.jpg',
                        annotated_image)
            count += 1
            #ここで100枚ごとにコメントを書いてる
            if count % 100 is 0:
                print("finished", count)
                #webアプリケーション用
                if (progress != None):
                    print(str(flame))
                    update_progress(status, count, flame)

            if cv2.waitKey(5) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

        for i, rows in data_buffer.items():
            csv_path = self.csv_paths[i]
            ConfigCSV.write_rows(csv_path, rows)

    def check_movie_aspect(self):
        RV = RotateVideo(self.input_video_path, self.tmp_path,
                         self.tmp_movie_name)
        print(f"video チェック{self.input_video_path}")
        orient = check_video_orientation(self.input_video_path)
        #もし動画が縦だったらそのまま通す

        #今、回転できないバグが起きているから修正が必要
        #コードが動くかどうかの確認
        orient = "Portrait"


        if orient == "Portrait":
            rotated_video_path = RV.rotate_video(None)
            shutil.copy2(rotated_video_path, self.output_video_path)  #コピー
            return
        elif orient == "Landscape":
            print("横")
            #もし横だったら、動画を回転する
            rotated_video_path = RV.rotate_video("rigte")
            print(rotated_video_path)
            orient = check_video_orientation(rotated_video_path)
            #回転が効いてない場合、エラー
            if orient == "Landscape":
                print("error in orient")
                return
            #もししっかり縦になってたら、動画の上下を確認する
            else:
                tmp = self.check_movie_top_and_botom(rotated_video_path)
                if tmp == True:
                    shutil.copy2(rotated_video_path,
                                 self.output_video_path)  #コピー
                    return
                else:
                    os.remove(rotated_video_path)
                    clean_directory(self.tmp_path)
                    rotated_video_path = RV.rotate_video("left")
                    shutil.copy2(rotated_video_path,
                                 self.output_video_path)  #コピー
                    return
        else:
            print("ファイルパスなどがおかしい")
            return

    def check_movie_top_and_botom(self, tmp_video_path):
        #動画の上下をnoze(0)と右手首(10)で推定する
        model = YOLO(self.model_path)

        tmp_data_buffer = {i: [] for i in range(17)}

        # Loop through the video images
        count = 0
        cap = cv2.VideoCapture(tmp_video_path)
        while cap.isOpened():
            # Read a image from the video
            success, image = cap.read()
            if not success and count == 0:
                print("Ignoring empty camera image.")
                # If loading a video, use 'break' instead of 'continue'.
                break
            results = model(image, verbose=False)
            annotated_image = results[0].plot()

            # keypointsの整理
            conn_person_keypoints = []
            if len(results[0].keypoints) > 0:
                for person_keypoints in results[0].keypoints:
                    conn_person_keypoints.append(person_keypoints.data[0])
                    #print(conn_person_keypoints)
                conn_person_keypoints = torch.cat(conn_person_keypoints, 1)
                conn_person_keypoints = conn_person_keypoints.cpu().numpy()
                #print(conn_person_keypoints)

                for i in range(self.key_point_num):
                    try:
                        tmp_data_buffer[i].append(conn_person_keypoints[i].tolist())
                    except IndexError:
                        tmp_data_buffer[i].append(['None', 'None', 'None', 'None'])
            count += 1
            if count == 2:
                break
        # ここで頭と手首の位置をチェックする
        for i, rows in tmp_data_buffer.items():
            ConfigCSV.write_rows(self.tmp_csv_paths[i], rows)

        head_data = read_csv(self.tmp_csv_paths[0])
        #print(head_data)
        wrist_data = read_csv(self.tmp_csv_paths[10])
        #print("head"+str(head_data))
        #print("wrist"+str(wrist_data))
        if head_data[0] < wrist_data[0]:
            return True
        else:
            return False

    def return_paths(self):
        return self.csv_paths, self.img_path


def update_progress(status,count,total):
    #ここで100枚ごとにコメントを書いてる
    progress = int((count / total)*100)
    print("progress"+str(progress))

    #こっちはjson書き込み用
    i = {'progress':progress}
    status.add(i)

def check_video_orientation(video_path):
    """
    動画が縦向きか横向きかを判別する関数。

    """
    try:
        # 動画ファイルを読み込む
        video = cv2.VideoCapture(video_path)

        # 動画が開けない場合の処理
        if not video.isOpened():
            print("動画を開けませんでした。パスを確認してください。")
            return None

        # 幅と高さを取得
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"幅{width}:高さ{height}")

        # 向きを判定
        orientation = "Portrait" if height > width else "Landscape"

        # 動画の解放
        video.release()

        return orientation
    except Exception as e:
        return f"エラーが発生しました: {e}"

def overwrite_video(source_path, target_path):
    """
    指定したパスAにあるmp4動画をパスBにあるmp4動画に上書き保存する。

    Args:
        source_path (str): 上書き元の動画ファイルのパス（パスA）。
        target_path (str): 上書き先の動画ファイルのパス（パスB）。

    Returns:
        str: 上書き先の動画ファイルのパス。
    """
    try:
        # パスBのディレクトリとファイル名を取得
        target_dir = os.path.dirname(target_path)
        target_filename = os.path.basename(target_path)

        # 上書きする動画の保存先パスを生成
        save_path = os.path.join(target_dir, target_filename)

        # 動画を上書き保存
        shutil.copyfile(source_path, save_path)

        return save_path
    except Exception as e:
        return f"エラーが発生しました: {e}"


def clean_directory(directory_path, keep_one_jpg=False):
    """
    指定したディレクトリ内のファイルを削除。
    - `keep_one_jpg=True` の場合は、.jpgファイルを1枚だけ残して他を削除。
    - `keep_one_jpg=False` の場合は、全てのファイルを削除。
    """
    if not os.path.exists(directory_path):
        print(f"指定されたディレクトリが存在しません: {directory_path}")
        return

    # ディレクトリ内のファイルをリストアップ
    files = os.listdir(directory_path)
    jpg_files = [file for file in files if file.lower().endswith('.jpg')]

    if keep_one_jpg:
        if jpg_files:
            # jpgファイルからランダムに1つ選択して残す
            file_to_keep = random.choice(jpg_files)
            print(f"この.jpgファイルを保持します: {file_to_keep}")
        else:
            print("ディレクトリ内に.jpgファイルがありません。全て削除します。")
            file_to_keep = None
    else:
        file_to_keep = None

    # ディレクトリ内のファイルを削除
    for file_name in files:
        file_path = os.path.join(directory_path, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                # 保持対象でない場合のみ削除
                if keep_one_jpg and file_name == file_to_keep:
                    continue
                os.remove(file_path)
                print(f"削除しました: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"エラーが発生しました: {file_path}, {e}")


def setup_csv(path):
    with open(path, 'w') as f:
        #ファイル内の初期化
        f.truncate(0)

def read_csv(filename):#利用
    # CSVファイルをNumPy配列に読み込む(y座標のみ)
    data = np.genfromtxt(filename, delimiter=',', usecols=1).T
    return data

# テストコード (インスタンス作成とメソッド呼び出し)
