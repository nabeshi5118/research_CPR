import cv2
import math

def get_video_aspect_ratio(video_path):
    """
    動画ファイルのパスを受け取り、そのアスペクト比（例: "16:9"）を文字列で返す関数。

    Args:
        video_path (str): 動画ファイルのパス。

    Returns:
        str: 計算されたアスペクト比の文字列。エラーの場合はNoneを返す。
    """
    # 動画ファイルを読み込む
    video = cv2.VideoCapture(video_path)

    # 動画が正常に開けたかを確認
    if not video.isOpened():
        print(f"エラー: 動画ファイルが開けませんでした。パスを確認してください: {video_path}")
        return None

    # 幅と高さを取得
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # 使い終わったのでリソースを解放
    video.release()

    # 幅か高さが0の場合はエラー（ファイル破損の可能性）
    if width == 0 or height == 0:
        print("エラー: 動画の解像度を取得できませんでした。")
        return None
        
    # 幅と高さの最大公約数（GCD）を計算
    common_divisor = math.gcd(width, height)

    # 最大公約数で割って、最も簡単な整数比を求める
    ar_width = width // common_divisor
    ar_height = height // common_divisor

    # "横:縦" の形式の文字列で返す
    return f"{ar_width}:{ar_height}"

# --- このコードの使い方 ---
if __name__ == '__main__':
    # ここに調べたい動画のパスを指定してください
    path_to_my_video = 'debug/debug_10.mp4'  # 例として先ほどの動画パスを入れました

    aspect_ratio = get_video_aspect_ratio(path_to_my_video)

    if aspect_ratio:
        print("-" * 30)
        print(f"動画ファイル: {path_to_my_video}")
        print(f"解像度: {cv2.VideoCapture(path_to_my_video).get(cv2.CAP_PROP_FRAME_WIDTH)} x {cv2.VideoCapture(path_to_my_video).get(cv2.CAP_PROP_FRAME_HEIGHT)}")
        print(f"アスペクト比: {aspect_ratio}")
        print("-" * 30)