import numpy as np
from cpr_app.models import AnalysisResult,PeakDataAppropriate
import copy

def cal_appropriate_recoil_compression(analysis_result:AnalysisResult):#Used
  # 圧迫解除・深度適性率を求める
  #複製の作成
    recoil_values = analysis_result.peak_data.recoil_peak_values
    depth_values = analysis_result.peak_data.depth_peak_values
    recoil_line = analysis_result.recoil_threshold
    depth_line = analysis_result.depth_threshold

    app_r_index = [] #適切な圧迫のindex
    app_d_index = []

    for i,rv in enumerate(recoil_values):
        if rv <= recoil_line:
            app_r_index.append(i)
    for j,dv in enumerate(depth_values):
        if dv >= depth_line:
            app_d_index.append(j)
    

    total_depth_count = analysis_result.results.peak_data.depth_peak_count
    total_recoil_count = analysis_result.results.peak_data.recoil_peak_count

    appro_recoil_percent = len(app_r_index) / total_recoil_count
    appro_depth_percent = len(app_d_index) / total_depth_count

    app_peak_data = PeakDataAppropriate(appro_depth_indexes=app_d_index,
                                        appro_recoils_indexes=app_r_index)

    analysis_result.results.appropriate_peak_data = app_peak_data
    analysis_result.report.appro_recoil_percent = appro_recoil_percent
    analysis_result.report.appro_depth_percent = appro_depth_percent

    

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
