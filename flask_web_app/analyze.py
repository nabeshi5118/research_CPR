#yoloで出力
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import os
import sys
import copy
import random
import shutil
sys.path.append(os.path.join(os.path.dirname(__file__), 'evaluation_system'))
from cpr_app.analyze_yolo.peak_detect_plot import PeakDetectPlot
from cpr_app.analyze_yolo.peak_data import PeakData ,PeakDataAppropriate
from cpr_app.analyze_yolo.value_info import ValueInfo as vi
from cpr_app.config_json import ConfigJson
from cpr_app.data.video_data import VideoData as vd
from cpr_app.analyze_yolo import write_csv_yolo_cpr
from cpr_app.analyze_yolo import plot_csv
from cpr_app.analyze_yolo import reconstruction_video
#video_pathは読み込む動画,csv_pathは出力されるデータのパス
# 動画ファイルのパスを格納するリスト
def recreate_mp4_structure(src_folder, dest_folder):
    video_paths = []
    # 出力ディレクトリのパスを格納するリスト
    output_directories = []

    # 指定フォルダ内の全.mp4ファイルを取得
    for root, _, files in os.walk(src_folder):
        for file in files:
            if file.endswith('.mp4'):
                # .mp4ファイルの完全なパス
                src_file_path = os.path.join(root, file)
                video_paths.append(src_file_path)

                # 出力フォルダに再現されるべき相対パス
                relative_path = os.path.relpath(root, src_folder)
                dest_dir = os.path.join(dest_folder, relative_path)

                # mp4ファイル名の拡張子を除いたディレクトリを作成
                file_name_without_ext = os.path.splitext(file)[0]
                file_specific_dir = os.path.join(dest_dir, file_name_without_ext)

                # ディレクトリの作成
                os.makedirs(file_specific_dir, exist_ok=True)

                # 作成したディレクトリをリストに追加
                output_directories.append(file_specific_dir)

    # 動画ファイルのパスと作成されたディレクトリのリストを返す
    return video_paths, output_directories

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
                #print(f"削除しました: {file_path}")
            #ディレクトリも消す処理をコメントアウト
            # elif os.path.isdir(file_path):
            #     shutil.rmtree(file_path)
        except Exception as e:
            print(f"エラーが発生しました: {file_path}, {e}")

def read_csv(filename):#利用
    # CSVファイルをNumPy配列に読み込む(y座標のみ)
    data = np.genfromtxt(filename, delimiter=',', usecols=1).T
    return data

def split_path(file_path):
    """
    ファイルパスを '_' で分割し、すべての部分を配列として返します。
    """
    # ファイルパスを '/' で分割して最後のファイル名部分を取得
    file_name = file_path.split("/")[-1]
    
    # '_' で分割
    parts = file_name.split("_")
    
    # 拡張子を削除
    if parts[-1].endswith(".mp4"):
        parts[-1] = parts[-1].replace(".mp4", "")
    
    return parts

# def convert_ndarray_to_str(data):
#     if isinstance(data, np.ndarray):
#         return ",".join(map(str,data.tolist()))
#     elif isinstance(data, list):
#         return ",".join(map(str,[convert_ndarray_to_str(i) for i in data]))
#     else:
#         return data
    
def convert_ndarray_to_str(data):
    if isinstance(data, np.ndarray):
        # int 型の場合
        if np.issubdtype(data.dtype, np.integer):
            return ",".join(map(str, data.tolist()))
        # float 型の場合
        elif np.issubdtype(data.dtype, np.floating):
            processed = (data * 10).astype(int)  # 10倍して int 型に変換
            return ",".join(map(str, processed.tolist()))
        else:
            raise ValueError("Unsupported ndarray data type.")
    elif isinstance(data, list):
        # リスト内の要素を再帰的に処理
        return ",".join(map(str, [convert_ndarray_to_str(i) for i in data]))
    else:
        return str(data)  # その他の型はそのまま文字列に変換

def get_index(group, number):
    # 各グループの内容を辞書で定義
    groups = {
        'A': [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 14, 15, 16],
        'B': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15],
        'C': [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        'D': [1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16]
    }
    # グループが存在し、数字がリストにある場合
    if group in groups and int(number) in groups[group]:
        return str(groups[group].index(number) + 1 )# インデックスを1始まりに調整
    else:
        return None  # 該当しない場合はNoneを返す
def get_test_number(group,number):
    groups = {
        'A': [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 14, 15, 16],
        'B': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15],
        'C': [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        'D': [1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16]
    }
    if group in groups:
        return str(groups[group][int(int(number)-1)])
    
def str_to_list(tmp_str):
    tmp_list = [float(value) for value in tmp_str.split(',')]
    return tmp_list
def list_to_str(tmp_list):
    tmp_str = ",".join(map(str, tmp_list))
    return tmp_str

def get_type(group,number):
    rand_3 = {
        "A":"Rapid_Strong",
        "B":"Rapid_Week",
        "C":"Slow_Strong",
        "D":"Slow_Week"
    }
    if int(number)%3==0:
        return rand_3[group]
    elif (group =="A" and int(number) ==4) or (group =="B" and int(number) ==8) or (group =="C" and int(number) ==12) or (group =="D" and int(number) ==16):
        return "Random"
    else:
        return "Best"
def index_recoil(tmp_list,threshold):
    #ボーダーライン以上のindexとvalueを返す
    #approRecoilを作る
    indices_values = [
        (index, value) for index, value in enumerate(tmp_list)
        if is_valid_number(value) and float(value) >= float(threshold)
    ]
    indices = [item[0] for item in indices_values]
    values = [item[1] for item in indices_values]
    return indices, values
def index_depth(tmp_list, threshold):
    indices_values = [
        (index, value) for index, value in enumerate(tmp_list)
        if is_valid_number(value) and float(value) <= float(threshold)
    ]
    indices = [item[0] for item in indices_values]
    values = [item[1] for item in indices_values]
    return indices, values
def is_valid_number(value):
    """数値かどうかを判定する関数"""
    try:
        float(value)  # 数値に変換可能かチェック
        return True
    except ValueError:
        return False

def check_CC(depth,recoil):
    if depth > recoil:
        return depth
    elif recoil>depth:
        return recoil
    else:
        return depth

#print(csv_paths)
#print(video_paths)
def main(video_path_list,output_path_list,movie_json_path,Group):
    window_size = 10
    print(window_size)
    for i in range(len(output_path_list)):
        #動画名
        file_name = os.path.basename(video_path_list[i])
        file_name = os.path.splitext(file_name)[0]

        #分割結果: ['s1290229', 'C', '50', '30', '6']
        print(video_path_list[i])
        print(file_name)
        VD = vd(video_path_list[i],file_name)
        #ここで、csvを作成中
        parts = split_path(video_path_list[i])
        #s1290148_A
        ID_type  = parts[0]+"_"+parts[1]
        #1~14
        ID_index = get_index(parts[1],int(parts[4]))
        print(ID_index)

        Name = Group+"_"+parts[1]+"_"+parts[4]
        json_path = movie_json_path +ID_type+".json"
        CJ = ConfigJson(json_path)
        dictionaly = CJ.dict()

        # if dictionaly[ID_type][ID_index][parts[3]]["AllData"] != "":
        #     continue

        exe = write_csv_yolo_cpr.YOLOv8Estimator(video_path_list[i],output_path_list[i],"yes")
        exe.estimation_algorithm(None,flame=VD.flame)
        clean_directory(output_path_list[i]+"/cache/",True)
        clean_directory(output_path_list[i]+"/tmp/",False)
        clean_directory(output_path_list[i]+"/",False)

        #左手首は9
        csv_path_10 = output_path_list[i] + "/csv/9.csv"
        
        data = read_csv(csv_path_10)
        person0_values = data
        
        # Nanの処理
        # 先頭がNaNの場合は0に置き換える
        if np.isnan(person0_values[0]):
            person0_values[0] = 0
        # NaNのインデックスを取得
        nan_indices = np.isnan(person0_values)
        # NaNを前の値で補完する処理
        person0_values[nan_indices] = np.interp(np.flatnonzero(nan_indices), np.flatnonzero(~nan_indices), person0_values[~nan_indices])

        dictionaly[ID_type][ID_index][parts[3]]["Name"]=Name
        dictionaly[ID_type][ID_index][parts[3]]["Type"]=get_type(parts[1],parts[4])
        dictionaly[ID_type][ID_index][parts[3]]["Height"]=parts[2]
        dictionaly[ID_type][ID_index][parts[3]]["Angle"]=parts[3]
        dictionaly[ID_type][ID_index][parts[3]]["Time"]=VD.time
        dictionaly[ID_type][ID_index][parts[3]]["AllData"]=convert_ndarray_to_str(person0_values)
        pd = PeakData()
        pdp = PeakDetectPlot()
        pdp.peak_detect_find_peaks(person0_values, window_size)
        #引数2,返り値2
        pd.setup_order_list(*pdp.return_order_list())
        pd.setup_values(*pdp.return_values())
        pd.setup_peak_count(*pdp.return_peak_count())

        dictionaly[ID_type][ID_index][parts[3]]["DepthOrderList"]=convert_ndarray_to_str(pd.depth_order_list)
        dictionaly[ID_type][ID_index][parts[3]]["RecoilOrderList"]=convert_ndarray_to_str(pd.recoil_order_list)
        dictionaly[ID_type][ID_index][parts[3]]["DepthValue"]=convert_ndarray_to_str(pd.depth_values)
        dictionaly[ID_type][ID_index][parts[3]]["RecoilValue"]=convert_ndarray_to_str(pd.recoil_values)
        dictionaly[ID_type][ID_index][parts[3]]["DepthCount"]=pd.peak_depth_count
        dictionaly[ID_type][ID_index][parts[3]]["RecoilCount"]=pd.peak_recoil_count
        dictionaly[ID_type][ID_index][parts[3]]["CompressionCount"] = check_CC(pd.peak_depth_count,pd.peak_recoil_count)
        CJ.add(dictionaly)
        if os.path.exists(output_path_list[i]) and output_path_list[i].endswith('.mp4'):
            os.remove(output_path_list[i])  # ファイルを削除

if __name__ =="__main__":
    Group = "C"
    video_path = "./movie/Group"+Group+"_trim_processed"
    output_path = "./CPR_video_2024_output"
    movie_json_path = "./movie/Movie_info_left/"
    print(video_path)
    print(output_path)
    video_path_list, output_path_list = recreate_mp4_structure(video_path,output_path)
    print(output_path_list)
    print(video_path_list)
    main(video_path_list=video_path_list,output_path_list=output_path_list,movie_json_path=movie_json_path,Group=Group)
    
