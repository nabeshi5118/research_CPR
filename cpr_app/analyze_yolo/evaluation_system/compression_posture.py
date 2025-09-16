import numpy as np

# 左右で実行する
# angle_dollは別で実行 左右無し
def cal_posture_evaluation(shoulder_list, elbow_list, wrist_list, fps, tempo_mean):
  correlation_list = []
  # 各キーポイントのリストのインデックスは0:x, 1:y
  # correlation_listのインデックスは0,1:shoulder(x,y), 2,3:elbow(x,y), 4,5:wrist(x,y) or hand(x,y)
  correlation_list.append(cal_autocorrelation(shoulder_list[0], fps, tempo_mean))
  correlation_list.append(cal_autocorrelation(shoulder_list[1], fps, tempo_mean))
  correlation_list.append(cal_autocorrelation(elbow_list[0], fps, tempo_mean))
  correlation_list.append(cal_autocorrelation(elbow_list[1], fps, tempo_mean))
  correlation_list.append(cal_autocorrelation(wrist_list[0], fps, tempo_mean))
  correlation_list.append(cal_autocorrelation(wrist_list[1], fps, tempo_mean))

  # 肘の角度
  alpha_list = cal_angle_elbow(shoulder_list, elbow_list, wrist_list)
  alpha_mean = np.nanmean(alpha_list)
  # 肘の角度の適性率
  wrist_condition = (alpha_list >= 165) & (alpha_list <= 180)
  indices = np.nonzero(wrist_condition)[0]
  angle_elbow_appropriate_count = len(indices)
  try:
    angle_elbow_appropriate_rate = angle_elbow_appropriate_count / len(alpha_list)
  except ZeroDivisionError:
    angle_elbow_appropriate_rate = 0
  if angle_elbow_appropriate_count == float('nan'):
    angle_elbow_appropriate_count = 0
  
  return correlation_list, alpha_list, alpha_mean, angle_elbow_appropriate_count, angle_elbow_appropriate_rate

def cal_autocorrelation(data, fps, tempo_mean):
  """
  自己相関関数を計算する関数
  :param data: 時系列データの配列
  :return: 自己相関関数のtime_shift時の値
  """
  # kの計算
  if tempo_mean == 0:
    k = 110
  else:
    k = int( (60 * fps) / tempo_mean)
  # yの平均
  y_avg = np.nanmean(data)
  # 分子の計算
  data_k = data[k:]
  data_k_minus_k = data[:-k]
  sum_of_covariance = np.sum((data_k - y_avg) * (data_k_minus_k - y_avg))
  # 分母の計算
  sum_of_denominator = np.sum((data - y_avg)**2)
  try:
    autocorrelation = sum_of_covariance / sum_of_denominator
  except ZeroDivisionError:
    autocorrelation = 0
  if autocorrelation == float('nan'):
    autocorrelation = 0
  return autocorrelation

def cal_angle_elbow(shoulder_list, elbow_list, wrist_list):
  # 肘から肩へのベクトル
  shoulder_to_elbow = elbow_list - shoulder_list
  # 肘から手首へのベクトル
  elbow_to_wrist = wrist_list - elbow_list
  # 肩から手首へのベクトル
  shoulder_to_wrist = wrist_list - shoulder_list
  # ベクトルの大きさ
  shoulder_to_elbow_norm = np.linalg.norm(shoulder_to_elbow, axis=0)
  elbow_to_wrist_norm = np.linalg.norm(elbow_to_wrist, axis=0)
  shoulder_to_wrist_norm = np.linalg.norm(shoulder_to_wrist, axis=0)
  # 内積
  #dot = np.sum(shoulder_to_elbow * elbow_to_wrist, axis=0)
  # 余弦定理
  #cosine = dot / (shoulder_to_elbow_norm * elbow_to_wrist_norm)
  cosine = (shoulder_to_elbow_norm**2 + elbow_to_wrist_norm**2 - shoulder_to_wrist_norm**2) / (2 * shoulder_to_elbow_norm * elbow_to_wrist_norm)
  # 角度
  cosine[cosine < -1] = -1
  cosine[cosine > 1] = 1
  alpha_list = np.degrees(np.arccos(cosine))
  
  return alpha_list

# angle_dollは別で実行
def cal_angle_doll(left_shoulder_list, right_shoulder_list, left_wrist_list, right_wrist_list):
  midpoint_shoulder_list = (left_shoulder_list + right_shoulder_list) / 2
  midpoint_wrist_list = (left_wrist_list + right_wrist_list) / 2
  vertical_point_list = np.array([midpoint_wrist_list[0], midpoint_shoulder_list[1]])
  # 肩から手首へのベクトル 
  shoulder_to_wrist = midpoint_wrist_list - midpoint_shoulder_list
  # 垂直点から手首へのベクトル
  vertical_point_to_wrist = midpoint_wrist_list - vertical_point_list
  # 肩から垂直点へのベクトル
  shoulder_to_vertical_point = vertical_point_list - midpoint_shoulder_list
  # ベクトルの大きさ
  shoulder_to_wrist_norm = np.linalg.norm(shoulder_to_wrist, axis=0)
  vertical_point_to_wrist_norm = np.linalg.norm(vertical_point_to_wrist, axis=0)
  shoulder_to_vertical_point_norm = np.linalg.norm(shoulder_to_vertical_point, axis=0)
  # 余弦定理
  cosine = (shoulder_to_wrist_norm**2 + vertical_point_to_wrist_norm**2 - shoulder_to_vertical_point_norm**2) / (2 * shoulder_to_wrist_norm * vertical_point_to_wrist_norm)
  # 角度
  cosine[cosine < -1] = -1
  cosine[cosine > 1] = 1
  beta_list = np.degrees(np.arccos(cosine))
  beta_mean = np.nanmean(beta_list)
  # 人形との角度
  doll_condition = (beta_list >= 0) & (beta_list <= 5)
  indices = np.nonzero(doll_condition)[0]
  angle_doll_appropriate_count = len(indices)
  try:
    angle_doll_appropriate_rate = angle_doll_appropriate_count / len(beta_list)
  except ZeroDivisionError:
    angle_doll_appropriate_rate = 0
  if angle_doll_appropriate_count == float('nan'):
    angle_doll_appropriate_count = 0
  
  return beta_list, beta_mean, angle_doll_appropriate_count, angle_doll_appropriate_rate


if __name__ == "__main__":
  # 自己相関関数の計算
  np.random.seed(0)
  time_series_data = np.random.rand(10)
  fps = 30
  tempo_mean = 10
  autocorrelation_result = cal_autocorrelation(time_series_data, fps, tempo_mean)
  print("自己相関係数:", autocorrelation_result)
  
  # 肘の角度
  shoulder_list = np.array([[0.8, 0.2, 0.4],[0.3, 1, 1]])
  elbow_list = np.array([[0.7, 0.2, 0.7], [0.2, 0.6, 0.6]])
  wrist_list = np.array([[0.6, 0.6, 0.7], [0.1, 0.2, 0.2]])
  hand_list = np.array([[0.6, 0.6, 0.7], [0.1, 0.2, 0.2]])
  alpha = cal_angle_elbow(shoulder_list, elbow_list, wrist_list)
  print("alpha:", alpha)

  # 人形との角度
  left_shoulder_list = np.array([[0.2, 0.4, 0.6],[0.6, 0.8, 0.6]])
  right_shoulder_list = np.array([[1,0.8,1],[1,0.8,0.6]])
  left_wrist_list = np.array([[0.8,0.4,0.2],[0.3,0.2,0]])
  right_wrist_list = np.array([[1,0.8,0.6],[0.5,0.2,0.4]])
  beta, beta_mean, angle_doll_appropriate_count, angle_doll_appropriate_rate = cal_angle_doll(left_shoulder_list, right_shoulder_list, left_wrist_list, right_wrist_list)
  print("beta:", beta)
  
  print(cal_posture_evaluation(shoulder_list, elbow_list, wrist_list, fps, tempo_mean))
