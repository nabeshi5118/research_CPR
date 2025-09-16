import ffmpeg
#from mediapipe_holistic import estimation_algorithm
import os
import shutil

def make_video(cache_path, output_path,fps):

  print('making movie...')

  # video conversion
  ffmpeg.input(cache_path + '/' + '%6d.jpg',framerate=fps)\
    .output(output_path, vcodec='libx264', pix_fmt='yuv420p', loglevel='error')\
    .run(overwrite_output=True)

# def make_video(cache_path, output_path, fps):
#   try:
#       print('making movie')
#       # fps を float 型に変換
#       #fps = float(fps)
#       ffmpeg.input(f'{cache_path}/%6d.jpg', framerate=fps) \
#             .output(output_path) \
#             .run(capture_stdout=True, capture_stderr=True)
#   except ffmpeg.Error as e:
#       print("FFmpeg error:")
#       print(e.stdout.decode('utf-8'))
#       print(e.stderr.decode('utf-8'))
#       raise
#   except ValueError as ve:
#       print("ValueError: fps の値が無効です。")
#       print(str(ve))
#       raise


if __name__ == "__main__":
  """
  select_parts = ['pose','left_hand','right_hand']
  cache_path = '/share/CPR_video_output/cache/'
  video = "/CPR-dataset/CPR_video_trimming/GroupA_trim/GoPro1/s1280015_01_Trim.MP4"
  output_path = "./output/output2.MP4"
  """
  select_parts = ['pose','left_hand','right_hand']
  cache_path = '/Share-2070super/Oki_dataset/cache1'
  video = "/Share-2070super/Oki_dataset/GX010018.MP4"
  output_path = "/Share-2070super/Oki_output/GX010018_mediapipe.MP4"

  #estimation_algorithm(video, select_parts, cache_path)
  make_video(cache_path, output_path)
