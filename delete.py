import os
import glob

def delete_mp4_files(directory):
    """ 指定したディレクトリ以下のすべての.mp4ファイルを削除する """
    # .mp4ファイルを再帰的に検索
    mp4_files = glob.glob(os.path.join(directory, '**', '*.mp4'), recursive=True)

    if not mp4_files:
        print("削除対象の.mp4ファイルは見つかりませんでした。")
        return
    
    print(f"削除対象のファイル {len(mp4_files)} 個:")
    for file in mp4_files:
        print(file)

    # ユーザーに確認
    confirmation = input("これらのファイルを削除しますか？ (y/N): ").strip().lower()
    if confirmation == 'y':
        for file in mp4_files:
            try:
                os.remove(file)
                print(f"削除しました: {file}")
            except Exception as e:
                print(f"削除に失敗しました: {file} ({e})")
    else:
        print("削除をキャンセルしました。")

# 使用例
target_directory = "/home/watanabe/research/Docker-composes/flask_CPR_web_app/CPR_video_2024_output"  # ここを適切なディレクトリに変更
delete_mp4_files(target_directory)
