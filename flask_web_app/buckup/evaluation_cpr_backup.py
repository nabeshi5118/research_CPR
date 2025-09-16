# def cal_mean_tempo(peak_upper_indexes, num_person0_values,fps):
#   # 今後リアルタイムに適応させる
#   #初期化
#   #num_person0_valueはperson0_valueの長さ
#   tempo_list = np.empty_like(peak_upper_indexes)

#   #インデックス番号と内容を入手できる
#   #なんでここpeak_upper_indexesを使ってるの？

#   for i, peak_upper_index in enumerate(peak_upper_indexes):
#     if i == 0:
#       tempo_list[i] = num_person0_values / peak_upper_index
#     else:
#       tempo_list[i] = num_person0_values / (peak_upper_index - peak_upper_indexes[i-1])
#   mean_tempo = np.sum(tempo_list) / len(peak_upper_indexes)
#   #mean_tenpoは平均のテンポ、tempo_listはそれぞれのテンポのリスト 
#   return mean_tempo, tempo_list

#def cal_appropriate_tempo(tempo_list,time):
  # # テンポの適性率を求める
  # # 初期化
  # appro_tempo_flag_list = np.empty_like(tempo_list, dtype=int)

  # tempo_lower = time * 100 // 60
  # tempo_upper = time * 120 // 60
  # for i, tempo in enumerate(tempo_list):
  #   #ここのテンポの上限下限を調整したい気持ちがある
  #   if tempo >= tempo_lower and tempo <= tempo_upper:
  #     appro_tempo_flag_list[i] = 1
  #   else:
  #     appro_tempo_flag_list[i] = 0
  # appro_tempo_percent = np.sum(appro_tempo_flag_list) / len(appro_tempo_flag_list)
  # return appro_tempo_percent
  