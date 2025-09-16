import os
import glob
import shutil
import csv
import torch
import json
from cpr_app.config_json import ConfigJson as cj
from cpr_app.config_csv import ConfingCSV as CC
import random
import os
import subprocess
import cv2

class RotateVideo():
    def __init__(self,input_video_path,cache_path,movie_name):
        self.tmp_path = cache_path
        self.input_video_path = input_video_path
        self.tmp_movie_name = movie_name
        
    def rotate_video(self, rotate_direction):
        try:
            # 動画ファイルの読み込み
            video = cv2.VideoCapture(self.input_video_path)
            print("rotate_video")
            output_path = self.tmp_path + "/" + self.tmp_movie_name

            # 動画が開けない場合の処理
            if not video.isOpened():
                return "動画を開けませんでした。パスを確認してください。"

            # 動画のプロパティを取得
            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = video.get(cv2.CAP_PROP_FPS)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 出力フォーマット

            # 出力動画の設定
            if rotate_direction == "right" or rotate_direction == "left":
                rotated_width, rotated_height = height, width  # 回転する場合は幅・高さを入れ替える
            else:
                rotated_width, rotated_height = width, height  # 回転しない場合はそのまま

            out = cv2.VideoWriter(output_path, fourcc, fps, (rotated_width, rotated_height))

            while True:
                ret, frame = video.read()
                if not ret:
                    break

                # フレームを回転
                if rotate_direction == "right":
                    rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)  # 右回転
                elif rotate_direction == "left":
                    rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)  # 左回転
                else:
                    rotated_frame = frame  # そのまま

                # 回転後のフレームを書き込み
                out.write(rotated_frame)

            # 動画の解放
            video.release()
            out.release()

            return output_path
        except Exception as e:
            return f"エラーが発生しました: {e}"
# def rotate_video(self, rotate_direction):
#     try:
#         # 動画ファイルの読み込み
#         video = cv2.VideoCapture(self.input_video_path)
        
#         # 動画が開けない場合の処理
#         if not video.isOpened():
#             return "動画を開けませんでした。パスを確認してください。"

#         # 動画のプロパティを取得
#         width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         fps = video.get(cv2.CAP_PROP_FPS)
#         if fps == 0 or fps is None:
#             fps = 30  # FPSが取得できない場合のデフォルト値
        
#         # 出力フォルダと一時フレーム保存フォルダを作成
#         tmp_frame_dir = os.path.join(self.tmp_path, "frames")
#         os.makedirs(tmp_frame_dir, exist_ok=True)

#         frame_count = 0
#         while True:
#             ret, frame = video.read()
#             if not ret:
#                 break

#             # フレームを回転
#             if rotate_direction == "right":
#                 rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)  # 右回転
#             elif rotate_direction == "left":
#                 rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)  # 左回転
#             else:
#                 rotated_frame = frame  # そのまま

#             # 画像として保存（FFmpegで動画化するため）
#             frame_path = os.path.join(tmp_frame_dir, f"frame_{frame_count:05d}.png")
#             cv2.imwrite(frame_path, rotated_frame)
#             frame_count += 1

#         # 動画の解放
#         video.release()

#         # FFmpeg で画像から動画を作成
#         output_path = os.path.join(self.tmp_path, self.tmp_movie_name)
#         ffmpeg_cmd = [
#             "ffmpeg",
#             "-y",  # 既存のファイルを上書き
#             "-framerate", str(fps),
#             "-i", os.path.join(tmp_frame_dir, "frame_%05d.png"),  # 画像の連番ファイルを入力
#             "-c:v", "libx264",  # H.264 コーデック
#             "-crf", "18",  # 高画質（数値が小さいほど高画質、0はロスレス）
#             "-preset", "slow",  # 品質優先
#             "-pix_fmt", "yuv420p",  # 色空間の互換性維持
#             output_path
#         ]

#         subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#         # 一時画像を削除
#         for file in os.listdir(tmp_frame_dir):
#             os.remove(os.path.join(tmp_frame_dir, file))
#         os.rmdir(tmp_frame_dir)

#         return output_path
#     except Exception as e:
#         return f"エラーが発生しました: {e}"

# def rotate_video(self, rotate_direction):
#     try:
#         # 動画ファイルの読み込み
#         video = cv2.VideoCapture(self.input_video_path)
#         if not video.isOpened():
#             return "動画を開けませんでした。パスを確認してください。"

#         width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         fps = video.get(cv2.CAP_PROP_FPS)
#         if fps == 0 or fps is None:
#             fps = 30  # FPSが取得できない場合のデフォルト値

#         # 出力フォルダと一時フレーム保存フォルダを作成
#         tmp_frame_dir = os.path.join(self.tmp_path, "frames")
#         os.makedirs(tmp_frame_dir, exist_ok=True)

#         # GPU メモリにフレームを格納
#         gpu_frame = cv2.cuda_GpuMat()

#         frame_count = 0
#         while True:
#             ret, frame = video.read()
#             if not ret:
#                 break

#             # フレームを GPU にアップロード
#             gpu_frame.upload(frame)

#             # 回転処理 (GPU ベース)
#             if rotate_direction == "right":
#                 rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), -90, 1.0)
#             elif rotate_direction == "left":
#                 rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), 90, 1.0)
#             else:
#                 rotation_matrix = np.eye(2, 3)

#             gpu_rotated = cv2.cuda.warpAffine(gpu_frame, rotation_matrix, (width, height))
#             rotated_frame = gpu_rotated.download()  # CPU に戻す

#             # 画像として保存（FFmpegで動画化するため）
#             frame_path = os.path.join(tmp_frame_dir, f"frame_{frame_count:05d}.png")
#             cv2.imwrite(frame_path, rotated_frame)
#             frame_count += 1

#         video.release()

#         # FFmpeg で GPU エンコーディング
#         output_path = os.path.join(self.tmp_path, self.tmp_movie_name)
#         ffmpeg_cmd = [
#             "ffmpeg",
#             "-y",
#             "-framerate", str(fps),
#             "-i", os.path.join(tmp_frame_dir, "frame_%05d.png"),
#             "-c:v", "h264_nvenc",  # GPU ベースのエンコーディング
#             "-b:v", "5M",
#             output_path
#         ]
#         subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#         # 一時画像を削除
#         for file in os.listdir(tmp_frame_dir):
#             os.remove(os.path.join(tmp_frame_dir, file))
#         os.rmdir(tmp_frame_dir)

#         return output_path

#     except Exception as e:
#         return f"エラーが発生しました: {e}"
