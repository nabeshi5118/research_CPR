import numpy as np
from cpr_app.models import AnalysisResult,PeakData
from cpr_app import values


from scipy.signal import find_peaks_cwt, find_peaks,medfilt
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage import maximum_filter1d

# plot_csv用
# 2種類のピーク検出
#ここにpeak_detectにあった２つのピーク検出方法が有った

def peak_detect_find_peaks(analysis_result:AnalysisResult):
    #x座標,y座標,正解率
    #data = maximum_filter1d(data, 10)
    #data = medfilt(data, 35)

    window_size = values.ANALYSIS_WINDOW_SIZE
    data = analysis_result.keypoint_data


    data_maxi = maximum_filter(data, window_size)


    #第2返り値は使わないため、_にしている
    
    peaks_depth, _ = find_peaks(data_maxi, height=0)#depth
    peaks_recoil, _ = find_peaks(-data_maxi)#recoil
    
    recoil_values = data[peaks_recoil]
    depth_values = data[peaks_depth]
    
    recoil_order_list = peaks_recoil
    depth_order_list = peaks_depth

    peak_recoil_count = len(peaks_recoil)
    peak_depth_count = len(peaks_depth)

    peak_data = PeakData(recoil_peak_indexes=recoil_order_list,
                         depth_peak_indexes=depth_order_list,
                         recoil_peak_values=recoil_values,
                         depth_peak_values=depth_values,
                         recoil_peak_count=peak_recoil_count,
                         depth_peak_count=peak_depth_count
                         )
    analysis_result.results.peak_data = peak_data
    

    #absは絶対値をintで返す
    #圧迫の深さとリコイルの差が1以上のとき、差がなくなるように調整する
    # if abs( len(pd.recoil_order_list) - len(pd.depth_order_list)) > 1:
    #     pd = adjust_peak_flask(pd, data)

# recoilとdepthの個数調整
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
