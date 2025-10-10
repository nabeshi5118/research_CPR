import cv2
#解析を始めるビデオのデータを管理する
class VideoData():
    def __init__(self,place,name = None):
        #name
        if name != None:
            self._name = name
        else:
            self._name = "output_data"
        self._place = place
        cap = cv2.VideoCapture(place)
        fps = cap.get(cv2.CAP_PROP_FPS)
        #fps = 119.88
        self._fps = fps
        flame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        time = float(flame) / float(fps)
        self._time  = int(time)
        self._flame = flame
        
        
        # print("fps"+str(fps))
        # print(str(type(fps)))
        # print("frame count"+str(flame))
        # print(str(type(flame)))
        # print("time"+str(time))


    #動画時間
    @property
    def time(self):
        return self._time
    #動画のパス
    @property
    def place(self):
        return self._place
    #動画名(使わないかも)
    @property
    def name(self):
        return self._name
    #動画のfps
    @property
    def fps(self):
        return self._fps
    #動画のフレーム数
    @property
    def flame(self):
        return self._flame
    



