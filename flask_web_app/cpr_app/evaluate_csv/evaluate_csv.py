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

from cpr_app.evaluate_csv import calculate_peak, calculate_treshold,calculate_mean_tempo,calculate_appro_tempo,calculate_appro_peak

from cpr_app.models import AnalysisResult
from cpr_app import values

def read_csv_useful_evaluation(filename):#利用
    # CSVファイルをNumPy配列に読み込む(y座標のみ)
    data = np.genfromtxt(filename, delimiter=',', usecols=1).T
    return data

def cal_compare_compression(analysis_result:AnalysisResult):#Used
    depth_count = analysis_result.peak_data.depth_peak_count
    recoil_count = analysis_result.peak_data.recoil_peak_count
    # リコイルと圧迫の回数を比較して、少ない方を採用　（要修正）
    compression_count = min(recoil_count, depth_count)
    return compression_count

#appro_compression
def cal_appro_compression(analysis_result:AnalysisResult):
    depth_index = analysis_result.results.peak_data.depth_peak_indexes
    recoil_index = analysis_result.results.peak_data.recoil_peak_indexes

    app_depth_index = analysis_result.results.appropriate_peak_data.appro_depth_peak_indexes
    app_recoil_index = analysis_result.results.appropriate_peak_data.appro_recoil_peak_indexes

    length = min(len(depth_index),len(recoil_index))
    same = set(app_depth_index) & set(app_recoil_index)
    return round(len(same)/length,2) 

# CSVファイルをプロットする関数

def evaluate_csv_data(csv_filename,analysis_result:AnalysisResult):
    #webアプリの場合はキーポイント10番のみ取得するのでcsvファイルは一個しか読み込まないはず

    data = read_csv_useful_evaluation(csv_filename)
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
    
    analysis_result.source.keypoint_data(person0_values)

    # ピーク検出
    calculate_peak.peak_detect_find_peaks(analysis_result)


    # CPR評価関数
    #圧迫回数
    compression_count = cal_compare_compression(analysis_result)
    analysis_result.report.compression_count = compression_count

    #ここで、ボーダーラインを決めている
    calculate_treshold.make_treshold(analysis_result)

    #圧迫成功率を求める
    calculate_appro_peak.cal_appropriate_recoil_compression(analysis_result)

    #平均テンポを計算する
    calculate_mean_tempo.cal_mean_tempo(analysis_result)
    # print("mean_tempo,tempolist")
    # print(mean_tempo)
    # print(tempo_list)
    # appro_tempo_percent = evaluation_cpr.cal_appropriate_tempo(tempo_list,fps)
    
    #適切圧迫回数を割り出す
    appro_comp_percent = cal_appro_compression(analysis_result)
    analysis_result.report.appro_compression_percent = appro_comp_percent


    


if __name__ == "__main__":
    print('YOLOv8')
    VD = VideoData('cpr_app/uploads/debug/debug.mp4')
    #plot_csv_data('cpr_app/outputs/csv/debug/10.csv','output_csv',VD.fps_video)

    