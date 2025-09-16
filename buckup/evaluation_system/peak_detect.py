import numpy as np
from scipy.signal import find_peaks
from scipy.ndimage.filters import maximum_filter
#ここでは、ピークの検出方法をまとめている
# 2種類のピーク検出とscipyを用いた検出方法
#ウィンドウを用いた検出方法
def peak_detect_window(data, window_size=80):

  peaks_upper = np.zeros(len(data))
  peaks_lower = np.zeros(len(data))

  for i in range(len(data) - window_size):
    window = data[i:i+window_size]
    recoil = min(window)
    depth = max(window)
    if data[i+window_size//2] == depth:
      peaks_upper[i+window_size//2] = depth
    if data[i+window_size//2] == recoil:
      peaks_lower[i+window_size//2] = recoil

  # np.whereからnp.nonzeroに変更
  recoil_order_list = np.nonzero(peaks_upper != 0)[0]
  depth_order_list = np.nonzero(peaks_lower != 0)[0]
  
  return recoil_order_list, depth_order_list

def peak_detect_diff(data):
  recoil_count = 0
  depth_count = 0
  peaks_upper = np.zeros(len(data))
  peaks_lower = np.zeros(len(data))

  for i in range(1, len(data) - 1):
    if data[i] > data[i-1] and data[i] > data[i+1]:
      recoil_count += 1
      peaks_upper[i] = data[i]
    if data[i] < data[i-2] and data[i] < data[i+2]:
      depth_count += 1
      peaks_lower[i] = data[i]
  
  # np.whereからnp.nonzeroに変更
  recoil_order_list = np.nonzero(peaks_upper != 0)[0]
  recoil_values = np.delete(peaks_upper, np.nonzero(peaks_upper == 0))
  depth_order_list = np.nonzero(peaks_lower != 0)[0]
  depth_values = np.delete(peaks_lower, np.nonzero(peaks_lower == 0))
  
  return recoil_count, depth_count, recoil_order_list, recoil_values, depth_order_list, depth_values

def peak_detect_scipy(data, window_size):

  data = maximum_filter(data, window_size)
  depth_order_list, _ = find_peaks(data, height=0)
  recoil_order_list, _ = find_peaks(-data)

  return recoil_order_list, depth_order_list
