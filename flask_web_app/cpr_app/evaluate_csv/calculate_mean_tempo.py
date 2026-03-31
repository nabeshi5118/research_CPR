from cpr_app.models import AnalysisResult

def cal_mean_tempo(analysis_result:AnalysisResult):
    CC = analysis_result.report.compression_count
    FPS = analysis_result.source.video_info.fps
    TIME = analysis_result.source.video_info.time
    FRAME = analysis_result.source.video_info.flame

    mean_tempo = (CC*FPS*TIME)/FRAME

    analysis_result.report.mean_tempo = mean_tempo

# def cal_mean_tempo(analysis_result:AnalysisResult):
#     # 初期化
#     tempo_list_sec = np.empty_like(peak_upper_indexes, dtype=float)
#     # 初期化
#     tempo_list_flame = np.empty_like(peak_upper_indexes, dtype=float)


#     for i, peak_upper_index in enumerate(peak_upper_indexes):
#         if i == 0:
#         # 最初のピーク位置の場合
#             tempo_list_flame[i] = peak_upper_index
#         # 一回の圧迫をフレーム単位から秒単位に変換
#             tempo_list_sec[i] = fps / tempo_list_flame[i] 
#         else:
#             tempo_list_flame[i] = (peak_upper_index - peak_upper_indexes[i - 1])
#         # フレーム数を秒単位に変換
#             tempo_list_sec[i] = fps / tempo_list_flame[i] 

#     if 60 % time == 0:
#         mean_tempo_per_min = 60 / time * compression_count
#     else:
#         # 1秒あたりの平均テンポを計算
#         mean_tempo_per_sec = np.sum(tempo_list_sec) / len(tempo_list_sec)
#         # 1分間の平均テンポに変換
#         mean_tempo_per_min = mean_tempo_per_sec * 60
    
#     return mean_tempo_per_min, tempo_list_flame