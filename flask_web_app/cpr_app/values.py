# cpr_app/config.py

# ==================================
# 解析アルゴリズム用パラメータ
# ==================================

# 平滑化のためのウィンドウサイズ
ANALYSIS_WINDOW_SIZE = 10

RECOIL_STATE_VALUE = 10
DEPTH_STATE_VALUE = 70


# ピークを検出するための閾値
PEAK_DETECTION_THRESHOLD = 0.8

# 1分あたりの目標テンポ
TARGET_TEMPO_PER_MINUTE = 110


# "mediapipe_flg" : 0,
# "y_lim_upper" : 0.85,
# "y_lim_lower" : 0.55,
# "h_line_upper" : 0.84,
# "h_line_lower" : 0.8,
# "fps" : 119.88,
# "window_size" : 10,
# "upper_line" : 754,
# "lower_line":715


#一旦、そのまま代入していた値をクラスにして呼び出せるようにした
#ゆくゆくは何かしらの方法で代入したい
# flask_web_app/cpr_app/analyze_yolo/value_info.py
# class ValueInfo():
#     def __init__(self):
#         #mediapipe_flg=0, y_lim_upper=0.85, y_lim_lower=0.55, h_line_upper=0.84, h_line_lower=0.8 ,fps=119.88, 
#         self._mediapipe_flg = 0
#         self._y_lim_upper = 0.85
#         self._y_lim_lower = 0.55
#         self._h_line_upper = 0.84
#         self._h_line_lower = 0.8
#         self._fps = 119.88
#         self._window_size = 10

    
#     def mediapipe_flg(self):
#         return self._mediapipe_flg
#     def y_lim_upper(self):
#         return self._y_lim_upper
#     def y_lim_lower(self):
#         return self._y_lim_lower
#     def h_line_upper(self):
#         return self._h_line_upper
#     def h_line_lower(self):
#         return self._h_line_lower
#     def fps(self):
#         return self._fps
#     def window_size(self):
#         return self._window_size


#plot_info.json
# {
#     "x_columns":0,
#     "y_columns":1,
#     "x_labels":"time",
#     "y_labels":"value",
#     "title":"Single Plot"
# }

#yolo_info.json
# {
#     "landmark":17,
#     "keypoint":10
# }