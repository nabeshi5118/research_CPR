import numpy as np

def cal_appropriate_recoil(data, recoil_line, recoil_order_list):
  condition_met_indices = np.abs(data[recoil_order_list]) <= recoil_line
  recoil_appropriate_order_list = np.nonzero(recoil_order_list[condition_met_indices])[0]
  
  # recoilの適性率
  try:
    recoil_appropriate_rate = len(recoil_appropriate_order_list) / len(recoil_order_list)
  except ZeroDivisionError:
    recoil_appropriate_rate = 0
  if recoil_appropriate_rate == float('nan'):
    recoil_appropriate_rate = 0  
  
  return recoil_appropriate_order_list, recoil_appropriate_rate

def cal_appropriate_depth(data, depth_line, depth_order_list):
  condition_met_indices = np.abs(data[depth_order_list]) >= depth_line
  depth_appropriate_order_list = np.nonzero(depth_order_list[condition_met_indices])[0]
  
  # depthの適性率
  try:
    depth_appropriate_rate = len(depth_appropriate_order_list) / len(depth_order_list)
  except ZeroDivisionError:
    depth_appropriate_rate = 0
  if depth_appropriate_rate == float('nan'):
    depth_appropriate_rate = 0
  return depth_appropriate_order_list, depth_appropriate_rate

if __name__ == "__main__":
  data = np.array([0.5, 0.6, 0.7, 0.4, 0.3, 0.4, 0.5, 0.4, 0.3, 0.33, 0.6, 0.9, 0.7, 0.5, 0.2, 0.4, 0.6, 0.597, 0.596, 0.6, 0.598, 0.6, 0.598, 0.4, 0.5, 0.7, 0.65, 0.6, 0.65, 0.63, 0.61, 0.63, 0.5, 0.7, 0.9, 0.8])
  depth_line = 0.3
  depth_order_list = np.array([4, 8, 14, 23, 27, 32])
  print(cal_appropriate_depth(data, depth_line, depth_order_list))
  # recoilも同様に計算する
