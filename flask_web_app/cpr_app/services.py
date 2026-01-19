# cpr_app/services.py

import shutil

from .evaluate_csv import evaluate_csv

from .make_result import reconstruction_video
from .models import VideoData,AnalysisResult  # VideoDataクラスをインポート
from util import ConfigJson
from .analyze_yolo import write_csv_yolo_cpr
from .make_result import make_result_data

class AnalysisService:
    """動画解析の全工程を管理するサービスクラス"""

    def __init__(self, video: VideoData, app_config: dict, result_paths: dict):
        self.video = video
        self.analysis_result = AnalysisResult(video)

        self.config = app_config
        
        self.result_paths = result_paths
        # このクラスが進捗トラッカーの責任を持つ
        self.progress_tracker = ConfigJson(self.config['CACHE_ANALYZE_PROGRESS_JSON'])

    def _update_progress(self, message: str, progress: int, step: int):
        """進捗を更新するための内部ヘルパー関数"""
        self.progress_tracker.add({'message': message, "progress": progress, "step": step})

    def run_full_analysis(self):
        """解析の全ステップを実行するメインメソッド"""
        
        # Step 1: 姿勢推定
        self._update_progress('Pose Estimate', 0, 1)
        exe = write_csv_yolo_cpr.YOLOv8Estimator(
            self.video.place, #動画のパス
            self.config['CACHE_PATH'], 
            self.config['YOLO_MODEL_PATH'],
            error_message=self.config['ERROR_MESSAGE']
        )
        exe.estimation_algorithm(self.config['JSON_ANALYZING_PROGRESS'], self.video.flame)
        
        self._update_progress('Pose Estimate', 100, 1)

        # Step 2: データ解析 
        self._update_progress('Analyze Data', 0, 2)
        # ... 本来のデータ解析ロジック ...
        evaluate_csv.evaluate_csv_data(self.config["CACHE_CSV_EVALUATE"],self.analysis_result)
        self._update_progress('Analyze Data', 100, 2)

        # Step 3: グラフ作成
        self._update_progress('Make Evaluation', 0, 3)
        make_result_data.make_result_data(self.analysis_result)
        self._update_progress('Make Graph', 100, 3)

        # Step 4: 動画作成
        self._update_progress('Make Movie', 0, 4)
        reconstruction_video.make_video(
            cache_path, 
            self.config['CACHE_OUTPUT_MOVIE'], 
            self.video.fps
        )
        self._update_progress('Make Movie', 100, 4)

        # Step 5: 結果の永続化
        self._save_results()
        
        # 最終メッセージ
        ar = ConfigJson(self.config['CACHE_ANALYZE_RESULT_JSON'])
        ar.add({'message': "Finished Analyze"})

    def _save_results(self):
        """解析結果をresultsフォルダにコピーする"""
        shutil.copy(self.config['CACHE_ANALYZE_RESULT_JSON'], self.result_paths["json"])
        shutil.copy(self.config['CACHE_OUTPUT_GRAPH'], self.result_paths["graph"])
        shutil.copy(self.config['CACHE_OUTPUT_MOVIE'], self.result_paths["video"])