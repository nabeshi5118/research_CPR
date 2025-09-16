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
from cpr_app.analyze_yolo.peak_detect_plot import PeakDetectPlot 
from cpr_app.analyze_yolo.peak_data import PeakData ,PeakDataAppropriate
from .value_info import ValueInfo as vi
from cpr_app.config_json import ConfigJson
from cpr_app.data.video_data import VideoData

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


def cal_appro_compression(app_depth_index,app_recoil_index,depth_index,recoil_index):
    
    length = min(len(depth_index),len(recoil_index))
    same = set(app_depth_index) & set(app_recoil_index)
    return round(len(same)/length,2) 

# CSVファイルをプロットする関数
#csv_file = cpr_app/outputs/filename/ファイル名_10.csv)
def plot_csv_data(csv_filename,fps,time,window_size,output_graph_path,analyzing_result_json=None):
    # プロット用のグラフを作成
    #ピーク検出におけるノイズ除去の範囲

    #固定値の情報が入っているjson
    VI = ConfigJson("cpr_app/information/value_info.json")
    #plot画像の情報が入っているjson
    PI = ConfigJson("cpr_app/information/plot_info.json")
    #結果出力用jsonファイル
    if analyzing_result_json!=None:
        ARJ = ConfigJson(analyzing_result_json)


    # 各CSVファイルを処理
    #webアプリの場合はキーポイント10番のみ取得するのでcsvファイルは一個しか読み込まないはず

    data = read_csv(csv_filename)
    # X軸とY軸のデータを取得
    person0_values = data
    
    # Nanの処理
    # 先頭がNaNの場合は0に置き換える
    if np.isnan(person0_values[0]):
        person0_values[0] = 0
    # NaNのインデックスを取得
    nan_indices = np.isnan(person0_values)
    # NaNを前の値で補完する処理
    person0_values[nan_indices] = np.interp(np.flatnonzero(nan_indices), np.flatnonzero(~nan_indices), person0_values[~nan_indices])
    
    # ピーク検出
    pdp = PeakDetectPlot()
    pdp.peak_detect_find_peaks(data = person0_values,window_size=window_size)
    pd = PeakData()

    #引数2,返り値2
    pd.setup_order_list(*pdp.return_order_list())
    pd.setup_values(*pdp.return_values())
    pd.setup_peak_count(*pdp.return_peak_count())
    #pd.print_contents()


    # CPR評価関数
    #圧迫回数
    compression_count = evaluation_cpr.cal_compare_compression(pd.peak_recoil_count, pd.peak_depth_count)
    
    # とりあえず、初期値（index0）をupper_lineにする
    #実際のコードはどうなっているのか確認
    #upper_line = VI.load("upper_line")#754
    #lower_line = VI.load("lower_line")#715

    recoil = 10
    depth = 70
    recoil_line = int(person0_values[pd.recoil_order_list[0]]) +recoil

    depth_line = recoil_line +depth

    #plot用に調整
    # person0_values_plot = person0_values
    # recoil_plot_line = recoil_line 
    # depth_plot_line =  depth_line

    pd_appro = PeakDataAppropriate(pd)

    pd_appro.setup_appro(*evaluation_cpr.cal_appropriate_recoil_compression(recoil_values=pd.recoil_values, depth_values=pd.depth_values, recoil_line=recoil_line, depth_line=depth_line))

    mean_tempo, tempo_list = evaluation_cpr.cal_mean_tempo(pd_appro.recoil_order_list, len(person0_values),compression_count,fps,time)
    # print("mean_tempo,tempolist")
    # print(mean_tempo)
    # print(tempo_list)
    # appro_tempo_percent = evaluation_cpr.cal_appropriate_tempo(tempo_list,fps)
    
    appro_comp_percent = cal_appro_compression(pd_appro.appro_compression_indexes,pd_appro.appro_recoils_indexes,pd.depth_order_list,pd.recoil_order_list)

    output = make_dict(pd_appro,compression_count,mean_tempo,appro_comp_percent)
    if analyzing_result_json!=None:
        ARJ.add(output)

    person0_values_plot =  -np.array(person0_values)
    recoil_plot_line = -recoil_line
    depth_plot_line = -depth_line

    # high_lim = max(max(recoil_line -pd.recoil_values), max(recoil_line -pd.depth_values)) + 10
    # low_lim = min(min(recoil_line -pd.recoil_values), min(recoil_line -pd.depth_values)) - 10

    #high_lim = recoil_plot_line 
    #low_lim = depth_plot_line 

    high_lim = person0_values_plot[pd.recoil_order_list[0]]+30
    low_lim = person0_values_plot[pd.depth_order_list[0]] -30

    # 作図ピーク検出
    pd.print_contents()
    plt.figure(figsize=(10,6))
    # 縦線を追加

    plt.axhline(y=recoil_plot_line, color='red', linestyle='-', linewidth=3, label='x=recoil_border_line')
    plt.axhline(y=depth_plot_line, color='green', linestyle='-', linewidth=3, label='x=depth_border_line')
    plt.scatter(pd.depth_order_list/fps, person0_values_plot[pd.depth_order_list], marker='o', facecolor='None', edgecolors='green', label="Recoil: "+str(pd.peak_depth_count)+' times')
    plt.scatter(pd.recoil_order_list/fps, person0_values_plot[pd.recoil_order_list], marker='o', facecolor='None', edgecolors='red', label="Depth: "+str(pd.peak_recoil_count)+' times')

    #　csvデータ
    # print('確認')
    # pd_appro.print_contents()
    #プロットできるようにtimeを変更
    time_v = np.linspace(0, len(person0_values_plot)/fps, len(person0_values_plot))
    plt.plot(time_v, person0_values_plot, label="chest compression movement")


    # ラベル、タイトル、凡例、保存

    plt.xlabel(PI.load("x_labels"))
    plt.ylabel(PI.load("y_labels"))
    
    #縦軸を消している
    plt.gca().yaxis.set_visible(False)
    
    plt.ylim(low_lim,high_lim)
    plt.xlim(0, max(time_v)+0.1)
    
    
    plt.minorticks_on()
    plt.grid(which = "both", axis="x")
    plt.title("Compression line graph")
    plt.legend(fontsize="xx-small")
    plt.savefig(output_graph_path, dpi=300, bbox_inches='tight')
    plt.close()
    


if __name__ == "__main__":
    print('YOLOv8')
    VD = VideoData('cpr_app/uploads/debug/debug.mp4')
    #plot_csv_data('cpr_app/outputs/csv/debug/10.csv','output_csv',VD.fps_video)

    