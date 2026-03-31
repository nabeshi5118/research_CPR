import cv2
from typing import Optional
from typing import Optional, Dict, List
from dataclasses import dataclass, field # dataclassをインポート
#解析を始めるビデオのデータを管理する
class VideoData():
    def __init__(self,place,name = None):
        #name
        if name != None:
            self.name = name
        else:
            self.name = "output_data"
        self.place = place
        cap = cv2.VideoCapture(place)
        fps = cap.get(cv2.CAP_PROP_FPS)
        #fps = 119.88
        self.fps = fps
        flame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        time = float(flame) / float(fps)
        self.time  = int(time)
        self.flame = flame
        cap.release()
        
        
        # print("fps"+str(fps))
        # print(str(type(fps)))
        # print("frame count"+str(flame))
        # print(str(type(flame)))
        # print("time"+str(time))


    # #動画時間
    # @property
    # def time(self):
    #     return self._time
    # #動画のパス
    # @property
    # def place(self):
    #     return self._place
    # #動画名(使わないかも)
    # @property
    # def name(self):
    #     return self._name
    # #動画のfps
    # @property
    # def fps(self):
    #     return self._fps
    # #動画のフレーム数
    # @property
    # def flame(self):
    #     return self._flame
    

class PeakData:
    def __init__(self,
                 _recoil_peak_indexes,
                 _depth_peak_indexes,
                 _recoil_peak_values,
                 _depth_peak_values,
                 _recoil_peak_count,
                 _depth_peak_count,
                 ):
        #名前かぶりを避けるために頭に_を入れている
        #ピークのインデックスの配列
        #peak_upper_indexesとpeak_lower_indexesと書かれている場合あり
        #recoil_order_listと書かれている場合あり
        self.recoil_peak_indexes = _recoil_peak_indexes
        self.depth_peak_indexes = _depth_peak_indexes
        #実際の値の配列
        #peak_upper_valuesとpeak_lower_valuesと書かれている場合あり
        self.recoil_peak_values = _recoil_peak_values
        self.depth_peak_values = _depth_peak_values
        #peak_upper_countとpeak_lower_countと書かれている場合あり
        self.recoil_peak_count = _recoil_peak_count
        self.depth_peak_count = _depth_peak_count
    

class PeakDataAppropriate():
    def __init__(self,appro_recoils_indexes,appro_depth_indexes,total_depth_count,total_recoil_count):
        self.appro_recoil_peak_indexes = appro_recoils_indexes
        self.appro_depth_peak_indexes = appro_depth_indexes

class Thresholds():
    def __init__(self,depth_threshold: float, recoil_threshold: float):
        self.depth_threshold: Optional[float] = depth_threshold
        self.recoil_threshold: Optional[float] = recoil_threshold



# (VideoData と PeakDataクラスは変更なしと仮定)
# ...

# ▼▼▼ 変更点1: グループ化のための小さなデータクラスを定義 ▼▼▼

@dataclass
class SourceData:
    """解析の元となったデータを格納するクラス。"""
    video_info: VideoData
    keypoint_data: Dict[int, List] = field(default_factory=dict)

@dataclass
class AnalysisSubResults:
    """解析の途中結果を格納するクラス。"""
    thresholds: Optional[Thresholds] = None
    peak_data: Optional[PeakData] = None
    appropriate_peak_data: Optional[PeakDataAppropriate] = None

@dataclass
class FinalReport:
    """最終的に出力・表示するための指標を格納するクラス。"""
    # (ここに最終結果の変数を追加していく)
    compression_count = Optional[int] = None
    tempo: Optional[float] = None
    appro_recoil_percent:Optional[float] = None
    appro_depth_percent:Optional[float] = None
    appro_compression_percent:Optional[float] = None
    mean_tempo:Optional[float] = None


# ▼▼▼ 変更点2: AnalysisResultクラスを、上記のグループを持つように修正 ▼▼▼

class AnalysisResult:
    """
    一つの動画解析に関する全ての情報を、グループ化して管理するコンテナクラス。
    """
    def __init__(self, video_data: VideoData):
        # 各グループを初期化
        self.source = SourceData(video_info=video_data)
        self.results = AnalysisSubResults()
        self.report = FinalReport()

    def display_summary(self):
        """この解析結果のサマリーを分かりやすく表示する。"""
        print("--- Analysis Summary ---")
        print(f"Video File: {self.source.video_info.place}")
        print(f"Duration: {self.source.video_info.time}s, FPS: {self.source.video_info.fps:.2f}")
        print("-" * 25)
        
        # アクセス方法が .source や .results を経由するように変わる
        print("\n[Final Report]")
        if self.report:
            print(f"CPR Tempo: {self.report.cpr_tempo} bpm")
            print(f"Average Depth: {self.report.average_depth_mm} mm")
        else:
            print("Not available.")