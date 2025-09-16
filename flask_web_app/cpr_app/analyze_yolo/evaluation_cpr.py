import numpy as np
from .peak_data import PeakData
import copy

def cal_compare_compression(peak_recoil_count,peak_depth_count):#Used
  # リコイルと圧迫の回数を比較して、少ない方を採用　（要修正）
  compression_count = min(peak_recoil_count, peak_depth_count)
  return compression_count


def cal_appropriate_recoil_compression(recoil_values,depth_values, recoil_line, depth_line):#Used
  # 圧迫解除・深度適性率を求める
  #複製の作成
    count_r = 0
    count_d = 0
    app_r_index = []
    app_d_index = []
    # print(recoil_line)
    # print(recoil_values)
    for i,rv in enumerate(recoil_values):
        if rv <= recoil_line:
            count_r +=1
            app_r_index.append(i)
    for j,dv in enumerate(depth_values):
        if dv >= depth_line:
            count_d +=1
            app_d_index.append(j)
    
    appro_recoil_percent = count_r / len(recoil_values)
    appro_depth_percent = count_d / len(depth_values) 

    return app_r_index,app_d_index,appro_recoil_percent,appro_depth_percent


#   tmp_recoil = recoil_values
#   tmp_depth = copy.deepcopy(pd)
#   # upper_lineとlower_lineはアノテーションファイルで求める
#   # upper_lineより小さいpeak_upper_valuesのインデックスをpeak_upper_indexesから消す
#   print(tmp_recoil)
#   print(tmp_depth)

#   appro_recoils_indexes = np.where(recoil_values >= recoil_line)
#   appro_recoils_indexes = np.delete(tmp_recoil.recoil_order_list, appro_recoils_indexes)
#   # lower_lineより大きいpeak_lower_valuesのインデックスをpeak_lower_indexesから消す


#   appro_depth_indexes = np.where(tmp_depth.depth_values <= depth_line)
#   appro_depth_indexes = np.delete(tmp_depth.depth_order_list, appro_depth_indexes)  
#   print(recoil_line)
#   print(depth_line)
#   # 適性率の計算
#   print(appro_recoils_indexes)
#   print(appro_depth_indexes)
#   print(len(tmp_recoil.recoil_order_list))
#   print(len(tmp_depth.depth_order_list) )

#   appro_recoils_percent = len(appro_recoils_indexes) / len(tmp_recoil.recoil_order_list)
#   appro_compression_percent = len(appro_depth_indexes) / len(tmp_depth.depth_order_list) 
  
#   pd.setup_appro(appro_recoils_indexes,appro_depth_indexes,appro_recoils_percent,appro_compression_percent)

#back_upに保存してある
#平均テンポの計算
def cal_mean_tempo(peak_upper_indexes, num_person0_values,compression_count, fps,time):#Used
    # 初期化
    tempo_list_sec = np.empty_like(peak_upper_indexes, dtype=float)
    # 初期化
    tempo_list_flame = np.empty_like(peak_upper_indexes, dtype=float)


    for i, peak_upper_index in enumerate(peak_upper_indexes):
        if i == 0:
        # 最初のピーク位置の場合
            tempo_list_flame[i] = peak_upper_index
        # 一回の圧迫をフレーム単位から秒単位に変換
            tempo_list_sec[i] = fps / tempo_list_flame[i] 
        else:
            tempo_list_flame[i] = (peak_upper_index - peak_upper_indexes[i - 1])
        # フレーム数を秒単位に変換
            tempo_list_sec[i] = fps / tempo_list_flame[i] 

    if 60 % time == 0:
        mean_tempo_per_min = 60 / time * compression_count
    else:
        # 1秒あたりの平均テンポを計算
        mean_tempo_per_sec = np.sum(tempo_list_sec) / len(tempo_list_sec)
        # 1分間の平均テンポに変換
        mean_tempo_per_min = mean_tempo_per_sec * 60
    
    return mean_tempo_per_min, tempo_list_flame

#backupに保存してる
def cal_appropriate_tempo(tempo_list, fps, baseline_lower_bpm=100, baseline_upper_bpm=120):#Used
    # テンポの適正率を求める
    # 初期化
    appro_tempo_flag_list = np.empty_like(tempo_list, dtype=int)

    # 適正テンポの範囲をフレーム単位で計算
    tempo_lower = 60 * fps / baseline_lower_bpm
    tempo_upper = 60 * fps / baseline_upper_bpm
    print(tempo_lower,tempo_upper)

    for i, tempo in enumerate(tempo_list):
        if tempo <= tempo_lower and tempo >= tempo_upper:
            appro_tempo_flag_list[i] = 1
        else:
            appro_tempo_flag_list[i] = 0

    appro_tempo_percent = np.sum(appro_tempo_flag_list) / len(appro_tempo_flag_list)
    return appro_tempo_percent
