import numpy as np
import peak_detect

# ピーク検出の実行 最初に実行する
def exe_peak_detection(data, window_size):
  recoil_order_list, depth_order_list = peak_detect.peak_detect_scipy(data, window_size)

  if abs( len(depth_order_list) - len(recoil_order_list)) >= 1:
    recoil_order_list, depth_order_list = adjust_peak(recoil_order_list, depth_order_list, data)
  # ピークが無い場合の対処　とりあえずなんか入れている
  if len(recoil_order_list) == 0:
    recoil_order_list = np.array([1])
  if len(depth_order_list) == 0:
    depth_order_list = np.array([0])

  return recoil_order_list, depth_order_list

def add_peak(major_list, minor_list, data, is_recoil_major):
  # ピークの個数が少ないリストを調整
  for i in range(len(major_list) - 1):
    # 1. Majorのピーク間にMinorのピークがないとき
    if not major_list[i] < minor_list[i] < major_list[i+1]:
      # ピークの個数が多いリストがrecoilの場合は最大値を、depthの場合は最小値を見つける
      func = np.argmax if is_recoil_major else np.argmin
      new_index = major_list[i] + func(data[major_list[i]:major_list[i+1]])+1
      # 新しいピークを追加
      minor_list = np.append(minor_list, new_index)
      minor_list = np.unique(minor_list)
      minor_list = np.sort(minor_list)

    # 2. ピークの個数がほぼ同じになったらループを抜ける
    if len(major_list) - len(minor_list) <= 1:
      return major_list, minor_list
    # 3. Minorのピークが先に終ってしまうとき
    elif len(minor_list) == i+1:
      # reject_peakを実行
      major_list, minor_list = reject_peak(major_list, minor_list, data, is_recoil_major)
      return major_list, minor_list
      
  return major_list, minor_list

def reject_peak(major_list, minor_list, data, is_recoil_major):
  # ピークの個数が多いリストを調整
  for i in range(2,len(minor_list)):
    if not minor_list[i-1] < major_list[i-1] < minor_list[i]:
      # ピークの個数が少ないリストがrecoilの場合は最小値を、depthの場合は最大値を見つける
      func = np.argmin if is_recoil_major else np.argmax
      new_index = minor_list[i-2] + func(data[minor_list[i-2]:minor_list[i-1]]) + 1
      # Minor[i-2]~Minor[i-1]の範囲の中でMajor[i-2]以外のピークを削除
      indexes = np.nonzero((major_list >= minor_list[i-2]) & (major_list <= minor_list[i-1]))
      major_list = np.delete(major_list, indexes)
      major_list = np.append(major_list, new_index)
      major_list = np.unique(major_list)
      major_list = np.sort(major_list)

      # ピークの個数がほぼ同じになったらループを抜ける
      if len(major_list) - len(minor_list) <= 1:
        return major_list, minor_list
  return major_list, minor_list

# recoilとdepthの個数調整
def adjust_peak(recoil_order_list, depth_order_list, data):
  # ピークが無い場合の対処
  if len(recoil_order_list) == 0:
    recoil_order_list = np.array([1])
  if len(depth_order_list) == 0:
    depth_order_list = np.array([0])
  # ピークの個数が多いリストと少ないリストを特定
  major_list, minor_list = (recoil_order_list, depth_order_list) if len(recoil_order_list) > len(depth_order_list) else (depth_order_list, recoil_order_list)
  #True,Falseで判別
  is_recoil_major = major_list is recoil_order_list
  
  # # ピークが先に来ている方が個数が多い方なら少ない方の追加、個数が少ない方なら多い方の削除
  # if major_list[0] < minor_list[0]:
  #   # ピークの個数が多いリストを調整
  #   major_list, minor_list = add_peak(major_list, minor_list, data, is_recoil_major)
  # else:
  #   # ピークの個数が少ないリストを調整
  #   major_list, minor_list = reject_peak(major_list, minor_list, data, is_recoil_major)
  
  # # ver.2
  # # ピークの個数が多いリストがrecoilの場合は、recoilを減らす
  # if is_recoil_major:
  #   major_list, minor_list = reject_peak(major_list, minor_list, data, is_recoil_major)
  # # ピークの個数が多いリストがdepthの場合は、depthを増やす
  # else:
  #   major_list, minor_list = add_peak(major_list, minor_list, data, is_recoil_major)
  # # ピークの個数が多いリストがrecoilだった場合は順番を戻す
  
  if is_recoil_major:
    #major_list, minor_list = reject_peak(major_list, minor_list, data, is_recoil_major)
    return major_list, minor_list
  else:
    return minor_list, major_list

# 中断の有無後に実行 圧迫回数、recoil・depthのピークリストを返す
def cal_compression_count(data, recoil_order_list, depth_order_list, interruption_pair_list):
  for interruption_pair in interruption_pair_list:
    for recoil in recoil_order_list:
      if interruption_pair[0] <= recoil <= interruption_pair[1]:
        recoil_order_list = np.delete(recoil_order_list, np.nonzero(recoil_order_list == recoil))
    for depth in depth_order_list:
      if interruption_pair[0] <= depth <= interruption_pair[1]:
        depth_order_list = np.delete(depth_order_list, np.nonzero(depth_order_list == depth))
  
  if abs( len(depth_order_list) - len(recoil_order_list)) >= 1:
    recoil_order_list, depth_order_list = adjust_peak(recoil_order_list, depth_order_list, data)
  return len(depth_order_list), recoil_order_list, depth_order_list


if __name__ == "__main__":
  # y座標データのみを渡す
  data = np.array( [0.5, 0.6, 0.7, 0.4, 0.3, 0.4, 0.5, 0.4, 0.3, 0.33, 0.6, 0.9, 0.7, 0.5, 0.2, 0.4, 0.6, 0.597, 0.596, 0.6, 0.598, 0.6, 0.598, 0.4, 0.5, 0.7, 0.65, 0.6, 0.65, 0.63, 0.61, 0.63, 0.5, 0.7, 0.9, 0.8])
  window_size = 3
  # 1. ピーク検出の実行
  recoil_order_list, depth_order_list = exe_peak_detection(data, window_size)
  # 2. 中断の有無の結果
  interruption_pair_list = np.array([[12, 13],[16, 21],[28, 31]])
  # 3. 圧迫回数、recoil・depthのピークリスト
  compression_count, recoil_order_list, depth_order_list = cal_compression_count(data, recoil_order_list, depth_order_list, interruption_pair_list)
  print(compression_count)
  print(recoil_order_list)
  print(depth_order_list)
