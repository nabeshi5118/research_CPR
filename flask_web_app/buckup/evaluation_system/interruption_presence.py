import numpy as np
import itertools

def check_interruption(x_lines, fps, wrist_list, recoil_order_list, depth_order_list, noise):
    """
    中断をチェックする関数
    """
    x_lines_adjusted = x_lines.copy()
    x_lines_adjusted[0] -= 0.3
    x_lines_adjusted[1] += 0.3
    interruption_1 = find_x_out_border(x_lines_adjusted, wrist_list)
    interruption_2 = find_weak_peaks(recoil_order_list, noise, fps)
    interruption_2_2 = find_weak_peaks(depth_order_list, noise, fps)
    interruption_3 = find_large_gaps(depth_order_list, fps)
        
    frame_arrays = np.concatenate((interruption_1, interruption_2, interruption_2_2, interruption_3))
    frame_arrays = np.delete(frame_arrays, np.nonzero(frame_arrays==-1))
    frame_arrays = np.unique(np.sort(frame_arrays))
    #中断判定を探す鍵かも
    interruption_pair_list = find_contiguous_pairs(frame_arrays)

    interruption_sec_list = np.array([(end - start + 1) / fps for start, end in interruption_pair_list])

    return interruption_pair_list, interruption_sec_list

def find_contiguous_pairs(indices):
    """
    連続した値の最初と最後のインデックスを見つける関数
    """
    if len(indices) == 0:
        return np.array([])

    diff = np.diff(indices)
    split_points = np.nonzero(diff != 1)[0] + 1

    starts = np.insert(split_points, 0, 0)
    ends = np.append(split_points, len(indices))
    pairs = np.array([[indices[starts[i]], indices[ends[i]-1]] for i in range(len(starts)) if starts[i] != ends[i]-1])
    return pairs

def find_x_out_border(x_lines, wrist_list):
    """
    x座標のボーダラインを超えるフレームを見つける関数
    """
    wrist_x = np.ravel(wrist_list[0])
    first_condition = (wrist_x < x_lines[0]) | (wrist_x > x_lines[1])
    interruption_1 = np.nonzero(first_condition)[0]

    return interruption_1

def find_weak_peaks(order_list, noise, fps):
    """
    ピーク間が小さすぎるフレームを見つける関数
    """
    interruption_2 = []
    small_gap = fps / (noise / 60)
    # 要修正
    for i in range(len(order_list)-1):
        if order_list[i+1] - order_list[i] < small_gap:
            interruption_2.append(order_list[i+1])
  
    return np.array(interruption_2)

def find_large_gaps(depth_order_list, fps):
    """
    深度の方のピーク間が1秒以上間が空いているフレームを見つける関数
    """
    interruption_3 = []
    for i in range(len(depth_order_list)-1):
        gap_frame = depth_order_list[i+1] - depth_order_list[i]
        if gap_frame > fps:
            interruption_3.append(list(range(int(depth_order_list[i]+ gap_frame/2) , int(depth_order_list[i+1] + gap_frame/2))))
    interruption_3 = list(itertools.chain.from_iterable(interruption_3))
    return np.array(interruption_3)


if __name__ == "__main__":
  # wrist_list[0]の0はx座標、1はy座標
  # x_lines[hand_flg][0]の0は小さい値、1は大きい値
  x_lines = np.array([0.5, 0.8])
  fps = 1
  wrist_list = np.array([[0.1, 0.6, 0.7, 0.4, 0.5, 0.6, 0.7, 0.7, 0.8, 1.0, 0.1, 0.6, 0.7, 0.4, 0.5, 0.6, 0.7, 0.7, 0.8, 1.0, 0.1, 0.6, 0.7, 0.4, 0.5, 0.6, 0.7, 0.7, 0.8, 1.0, 0.5, 0.6, 0.7, 0.7, 0.8, 1.0], [0.5, 0.6, 0.7, 0.4, 0.3, 0.4, 0.5, 0.4, 0.3, 0.33, 0.6, 0.9, 0.7, 0.5, 0.2, 0.4, 0.6, 0.597, 0.596, 0.6, 0.598, 0.6, 0.598, 0.4, 0.5, 0.7, 0.65, 0.6, 0.65, 0.63, 0.61, 0.63, 0.5, 0.7, 0.9, 0.8]])
  noise = 0.06
  depth_order_list = np.array([2, 6, 11, 16, 19, 21, 25, 28, 31, 34])
  #depth_order_list = np.array([4, 8, 14, 18, 20, 23, 27, 30, 32])
  recoil_order_list = np.array([4, 8, 14, 18, 20, 23, 27, 30, 31,32,33])
  
  print(check_interruption(x_lines, fps, wrist_list, recoil_order_list, depth_order_list, noise))
