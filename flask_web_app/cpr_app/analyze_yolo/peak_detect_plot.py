import numpy as np
from .peak_data import PeakData
from scipy.signal import find_peaks_cwt, find_peaks,medfilt
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage import maximum_filter1d

# plot_csv用
# 2種類のピーク検出
#ここにpeak_detectにあった２つのピーク検出方法が有った
class PeakDetectPlot:
    def __init__(self):
        #名前かぶりを避けるために頭に_を入れている
        #ピークのインデックスの配列
        #peak_upper_indexesとpeak_lower_indexesと書かれている場合あり
        self.recoil_order_list = []
        self.depth_order_list = []
        #実際の値の配列
        #peak_upper_valuesとpeak_lower_valuesと書かれている場合あり
        self.recoil_values = []
        self.depth_values = []
        #peak_upper_countとpeak_lower_countと書かれている場合あり
        self.peak_recoil_count = 0
        self.peak_depth_count = 0

    def peak_detect_find_peaks(self,data, window_size):
        #x座標,y座標,正解率
        #data = maximum_filter1d(data, 10)
        #data = medfilt(data, 35)

        data_maxi = maximum_filter(data, window_size)

        #第2返り値は使わないため、_にしている
        
        peaks_depth, _ = find_peaks(data_maxi, height=0)#depth
        peaks_recoil, _ = find_peaks(-data_maxi)#recoil
        
        self.recoil_values = data[peaks_recoil]
        self.depth_values = data[peaks_depth]
        
        self.recoil_order_list = peaks_recoil
        self.depth_order_list = peaks_depth

        self.peak_recoil_count = len(peaks_recoil)
        self.peak_depth_count = len(peaks_depth)

        #absは絶対値をintで返す
        #圧迫の深さとリコイルの差が1以上のとき、差がなくなるように調整する
        # if abs( len(pd.recoil_order_list) - len(pd.depth_order_list)) > 1:
        #     pd = adjust_peak_flask(pd, data)


    def return_values(self):
        return self.depth_values,self.recoil_values
    def return_order_list(self):
        return self.depth_order_list,self.recoil_order_list
    def return_peak_count(self):
        return self.peak_depth_count,self.peak_recoil_count
# recoilとdepthの個数調整
# evaluation_systemでも存在を確認
def adjust_peak_flask(pd, data):
    if len(pd.recoil_order_list()) - len(pd.depth_order_list()) > 1:
        # recoilの方が多い場合,
        for i in  range(len(pd.recoil_order_list)):
            #リコイル2回の間に圧迫が来なかった場合
            if not pd.recoil_order_list[i] < pd.depth_order_list[i] < pd.recoil_order_list[i+1]:
                #配列の中でも最小の値を新たな圧迫とする
                min_index = i + np.argmin(data[pd.recoil_order_list[i]:pd.recoil_order_list[i+1]+1])
                
                pd.depth_order_list(np.append(pd.depth_order_list, min_index))
                pd.depth_values(np.append(pd.depth_values, data[min_index]))
                if abs(len(pd.recoil_order_list) - len(pd.depth_order_list)) <= 1:
                    break
    
    else:
        # depthの方が多い場合
        for i in  range(len(pd.depth_order_list)):
            if not pd.depth_order_list[i] < pd.recoil_order_list[i] < pd.depth_order_list[i+1]:
                max_index = i + np.argmax(data[pd.depth_order_list[i]:pd.depth_order_list[i+1]+1])

                pd.recoil_order_list(np.append(pd.recoil_order_list, max_index))
                pd.recoil_values(np.append(pd.recoil_values, data[max_index]))

                if abs(len(pd.recoil_order_list) - len(pd.depth_order_list)) <= 1:
                    break
    
    return pd
