#一旦、そのまま代入していた値をクラスにして呼び出せるようにした
#ゆくゆくは何かしらの方法で代入したい
class ValueInfo():
    def __init__(self):
        #mediapipe_flg=0, y_lim_upper=0.85, y_lim_lower=0.55, h_line_upper=0.84, h_line_lower=0.8 ,fps=119.88, 
        self._mediapipe_flg = 0
        self._y_lim_upper = 0.85
        self._y_lim_lower = 0.55
        self._h_line_upper = 0.84
        self._h_line_lower = 0.8
        self._fps = 119.88
        self._window_size = 10

    
    def mediapipe_flg(self):
        return self._mediapipe_flg
    def y_lim_upper(self):
        return self._y_lim_upper
    def y_lim_lower(self):
        return self._y_lim_lower
    def h_line_upper(self):
        return self._h_line_upper
    def h_line_lower(self):
        return self._h_line_lower
    def fps(self):
        return self._fps
    def window_size(self):
        return self._window_size