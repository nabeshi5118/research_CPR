import os
import subprocess
import re

#動画を30秒か1分にトリミングするコード

# 動画情報を取得する関数（解像度と再生時間）
def get_video_info(input_file):
    if not os.path.exists(input_file):
        print(f"ファイルが見つかりません: {input_file}")
        return None, None, None

    try:
        result = subprocess.run(
            ["ffmpeg", "-i", input_file],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )

        # FFmpeg 出力のデバッグ表示
        print(f"FFmpeg 出力 ({input_file}):\n", result.stderr)

        # 解像度の取得（例: 1920x1080）
        resolution_match = re.search(r'(\d{2,5})x(\d{2,5})', result.stderr)
        if resolution_match:
            width, height = map(int, resolution_match.groups())
        else:
            raise ValueError("解像度の取得に失敗しました")

        # 再生時間の取得（例: Duration: 00:01:01.73）
        duration_match = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', result.stderr)
        if duration_match:
            hours, minutes, seconds = map(float, duration_match.groups())
            duration = hours * 3600 + minutes * 60 + seconds
        else:
            raise ValueError("再生時間の取得に失敗しました")

        return width, height, duration

    except Exception as e:
        print(f"エラー発生: {e}")
        return None, None, None

# 動画を処理する関数
def process_video(input_file, output_file):
    width, height, duration = get_video_info(input_file)

    if width is None or height is None or duration is None:
        print(f"ビデオ情報の取得に失敗しました: {input_file}")
        return

    # トリミング時間の決定
    trim_duration = 30 if duration < 50 else 60

    # 出力ファイルが既に存在する場合削除
    if os.path.exists(output_file):
        os.remove(output_file)

    # FFmpegコマンドの構築
    cmd = [
        'ffmpeg', '-y', '-ss', '0', '-i', input_file, '-t', str(trim_duration),
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
        '-c:a', 'aac', '-b:a', '192k',
        '-vsync', '0', output_file
    ]

    print(f"処理中: {input_file} → {output_file}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.returncode == 0:
        print(f"変換成功: {output_file}")
    else:
        print(f"エラー発生: {result.stderr}")

# メイン関数（ディレクトリ探索＆処理）
def main(input_dir, output_parent):
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.mp4'):
                input_file = os.path.join(root, file)

                # 出力ディレクトリを作成
                relative_path = os.path.relpath(root, input_dir)
                output_dir = os.path.join(output_parent, os.path.basename(input_dir) + "_processed", relative_path)
                os.makedirs(output_dir, exist_ok=True)

                # 出力ファイル名設定（元の名前を維持）
                output_file = os.path.join(output_dir, file)

                # 動画処理の実行
                process_video(input_file, output_file)

if __name__ == "__main__":
    input_directory = "./GroupC_trim"  # 入力フォルダ
    output_directory = "./"            # 出力先の親フォルダ
    main(input_directory, output_directory)
