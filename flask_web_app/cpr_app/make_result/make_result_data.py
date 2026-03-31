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


def make_result_data(analysis_result:AnalysisResult):
     
    PI = ConfigJson("cpr_app/information/plot_info.json")
    if analyzing_result_json!=None:
            ARJ = ConfigJson(analyzing_result_json)
            #出力用のjsonデータを作成する

    # とりあえず、初期値（index0）をupper_lineにする
    #実際のコードはどうなっているのか確認
    #upper_line = VI.load("upper_line")#754
    #lower_line = VI.load("lower_line")#715

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