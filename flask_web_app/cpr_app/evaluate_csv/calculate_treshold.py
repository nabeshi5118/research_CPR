#yoloで出力
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import os
import sys
import copy
sys.path.append(os.path.join(os.path.dirname(__file__), 'evaluation_system'))
#from evaluation_system import compression_count as cc,interruption_presence as ip,compression_tempo as ct,recoil_and_depth as rd,compression_posture as cp
from . import calculate_appro_peak


from cpr_app.models import AnalysisResult,Thresholds
from cpr_app import values

#リコイルボーダーラインとdepthボーダーラインを決める
def make_treshold(analysis_result:AnalysisResult):
    recoil_order_indexes = analysis_result.peak_data.recoil_peak_indexes
    keypoint_data = analysis_result.keypoint_data
    #ここで、ボーダーラインを決めている
    recoil = values.RECOIL_STATE_VALUE
    depth = values.DEPTH_STATE_VALUE
    recoil_line = int(keypoint_data[recoil_order_indexes[0]]) +recoil
    depth_line = recoil_line +depth

    thresholds = Thresholds(depth_threshold=depth_line,recoil_threshold=recoil_line)

    analysis_result.results.thresholds = thresholds


