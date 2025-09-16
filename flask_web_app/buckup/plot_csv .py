#yoloで出力
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import os
import sys
import copy
sys.path.append(os.path.join(os.path.dirname(__file__), 'evaluation_system'))
#from evaluation_system import compression_count as cc,interruption_presence as ip,compression_tempo as ct,recoil_and_depth as rd,compression_posture as cp
from . import evaluation_cpr
from . import peak_detect_plot
from .peak_data import PeakData ,PeakDataAppropriate
from .value_info import ValueInfo as vi
from cpr_app.config_json import ConfigJson
from cpr_app.data.video_data import VideoData

# from .compression_data import CompressionData

# CSVファイルを読み込む関数
#必要なさそうだったら消す
# def read_csv(filename):
#     # CSVファイルをNumPy配列に読み込み、正規化する(y座標のみ)
#     #data = np.genfromtxt(filename, delimiter=',', usecols=(1,4),invalid_raise=False).T
#     data = np.genfromtxt(filename, delimiter=',', usecols=1,invalid_raise=False).T
#     data = data/1080
#     return data
  

def read_csv(filename):#利用
    # CSVファイルをNumPy配列に読み込む(y座標のみ)
    data = np.genfromtxt(filename, delimiter=',', usecols=1).T
    return data

#出力用のjsonデータを作成する
def make_dict(pd_appro,compression_count,mean_tempo,appro_tempo_percent):
    #データ渡し用のdictを作成
    
    appro_tempo_percent_out = round(appro_tempo_percent,3) *100
    appro_recoils_percent_out = round(pd_appro.appro_recoils_percent,3)*100
    appro_compression_percent_out = round(pd_appro.appro_compression_percent,3)*100
    mean_tempo_out = round(mean_tempo,1)
    output = {
        "compression_count" :compression_count,
        "appro_recoils_percent":appro_recoils_percent_out,
        "appro_compression_percent": appro_compression_percent_out,
        "mean_tempo":mean_tempo_out,
        "appro_tempo_percent": appro_tempo_percent_out
    }
    return output


def check_person0(person0_values):
# person0_values[0] が数値であるかを確認
    if person0_values and isinstance(person0_values[0], (int, float)):
        if np.isnan(person0_values[0]):
            # NaNの場合の処理
            print("person0_values[0] is NaN")
            return 0
        else:
            # 有効な数値の場合の処理
            print("person0_values[0] is a valid number")
            return 1
    else:
        # 数値でない場合の処理
        print("person0_values[0] is not a valid number or is empty")
        return 0

    

# CSVファイルをプロットする関数
#csv_file = cpr_app/outputs/filename/ファイル名_10.csv)
#plot_csv_data(csv_file, 0, 1, 'Time', ['PersonID=0', 'PersonID=1'], 'Single Plot', 'MediaPipe.png', video.time(), mediapipe_flg=1)
def plot_csv_data(csv_filenames,fps,time,output_pass=None, output_filename=None):
    #v_infoの中身   mediapipe_flg, y_lim_upper, y_lim_lower, h_line_upper, h_line_lower,fps 
    # プロット用のグラフを作成
    #ピーク検出におけるノイズ除去の範囲
    if check_person0 is 0:
        return
    #固定値の情報が入っているjson
    VI = ConfigJson("cpr_app/information/value_info.json")
    #plot画像の情報が入っているjson
    PI = ConfigJson("cpr_app/information/plot_info.json")
    #結果出力用jsonファイル
    CJ = ConfigJson("cpr_app/outputs/json/result.json")
    window_size = VI.load("window_size")

    if(output_pass != None and output_filename !=None):
        save_path = output_pass + '/'+ output_filename
        CJ.add({"image":save_path})
    elif(output_pass == None and output_filename == None):
        save_path = "/home/research"
        print("plot_csvでパス指定してね")
    else:
        print("plot_csvで引数ミスってるよ")
        return

    # 各CSVファイルを処理
    #webアプリの場合はキーポイント10番のみ取得するのでcsvファイルは一個しか読み込まないはず
    #for i,csv_filename in enumerate(csv_filenames):

    #デバックのために必要
    if isinstance(csv_filenames,list): 
        csv_filename = csv_filenames[10]
    else:
        csv_filename = csv_filenames
    
    data = read_csv(csv_filename)
    # X軸とY軸のデータを取得
    person0_values = data
    
    # Nanの処理
    # 先頭がNaNの場合は0に置き換える
    # ここで、空の配列の場合、エラー吐いちゃう、対策必要かも
    if np.isnan(person0_values[0]):
        person0_values[0] = 0
    # NaNのインデックスを取得
    nan_indices = np.isnan(person0_values)
    # NaNを前の値で補完する処理
    person0_values[nan_indices] = np.interp(np.flatnonzero(nan_indices), np.flatnonzero(~nan_indices), person0_values[~nan_indices])
    
    # ピーク検出
    pd = PeakData()
    pd = peak_detect_plot.peak_detect_find_peaks(person0_values,pd, window_size)

    #peak_detect.peak_detect_window(person0_values, 10)
    
    # CPR評価関数
    #圧迫回数
    compression_count = evaluation_cpr.cal_compare_compression(pd.peak_recoil_count, pd.peak_depth_count)
    
    # とりあえず、初期値（index0）をupper_lineにする
    #実際のコードはどうなっているのか確認
    #print("recoil_value")
    #print(pd.recoil_values)
    upper_line = VI.load("upper_line")#754
    lower_line = VI.load("lower_line")#715

    pd_appro = PeakDataAppropriate(pd)

    evaluation_cpr.cal_appropriate_recoil_compression(pd_appro,upper_line, lower_line)

    mean_tempo, tempo_list = evaluation_cpr.cal_mean_tempo(pd_appro.recoil_order_list, len(person0_values),compression_count,fps,time)
    print("mean_tempo,tempolist")
    print(mean_tempo)
    print(tempo_list)

    appro_tempo_percent = evaluation_cpr.cal_appropriate_tempo(tempo_list,fps)

    output = make_dict(pd_appro,compression_count,mean_tempo,appro_tempo_percent)
    #今はパスを直接書いてる
    CJ.add(output)

    # ピーク検出
    plt.figure(figsize=(10,6))
    plt.scatter(pd.depth_order_list/fps, person0_values[pd.depth_order_list], marker='o', facecolor='None', edgecolors='green', label="Recoil: "+str(pd.peak_depth_count)+' times')
    plt.scatter(pd.recoil_order_list/fps, person0_values[pd.recoil_order_list], marker='o', facecolor='None', edgecolors='red', label="Depth: "+str(pd.peak_recoil_count)+' times')

    #　csvデータ
    # print('確認')
    # pd_appro.print_contents()

    x_times = np.arange(len(data)) / fps
    plt.plot(x_times, person0_values, label="sample")
    #plt.plot(x_times, person1_values, label=os.path.basename(csv_filename) + ', PersonID=1')

    # ラベル、タイトル、凡例、保存

    plt.xlabel(PI.load("x_labels"))
    plt.ylabel(PI.load("y_labels"))

    high_lim = max(pd.recoil_values)+5
    low_lim = min(pd.depth_values)-5
    plt.ylim(low_lim,high_lim)
    
    
    plt.minorticks_on()
    plt.grid(which = "both", axis="x")
    plt.title(os.path.basename(csv_filename))
    plt.legend(fontsize="xx-small")
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    

if __name__ == "__main__":
    print('YOLOv8')
    VD = VideoData('cpr_app/uploads/debug/debug.mp4')
    #plot_csv_data('cpr_app/outputs/csv/debug/10.csv','output_csv',VD.fps)

    