import numpy as np

def cal_tempo_mean(compression_count, frames_num, fps):
  return (compression_count * 60) / (frames_num / fps)

def cal_tempo_appropriate_rate(depth_order_list, fps):
  # 差分の計算
  difference_list = np.diff(depth_order_list)
  
  # １回の圧迫の適切なテンポ
  min_tempo = (fps * 60) / 100
  max_tempo = (fps * 60) / 120
  appropriate_tempo_order = (np.abs(difference_list) <= min_tempo) & (np.abs(difference_list) >= max_tempo)
  
  # 適切なテンポの圧迫回数
  appropriate_tempo_count = np.sum(appropriate_tempo_order)
  try:
    appropriate_tempo_rate = appropriate_tempo_count / len(depth_order_list)
  except ZeroDivisionError:
    appropriate_tempo_rate = 0
  if appropriate_tempo_rate == float('nan'):
    appropriate_tempo_rate = 0
  
  return appropriate_tempo_count, appropriate_tempo_rate
  
  
if __name__ == "__main__":
  compression_count = 6
  frames_num = 36
  fps = 2
  depth_order_list = np.array([4, 8, 14, 23, 27, 32])
  print(cal_tempo_mean(compression_count, frames_num, fps))
  print(cal_tempo_appropriate_rate(depth_order_list, fps))

  