from pathlib import Path
from typing import Union,Optional

# クラス名を大文字から始める (例: Config, Settings, Paths など)
class Config:
    # --- パス設定 (クラス変数) ---
    # __init__の外で定義することで、インスタンス化せずにアクセスできる
    
    # プロジェクトのルートディレクトリ
    BASE_DIR = Path(__file__).resolve().parent

    # 主要なディレクトリパス
    DATA_DIR = BASE_DIR / "data"
    OUTPUTS_DIR = BASE_DIR / "outputs"

    # デバッグデータに関するパス
    # Pathオブジェクトとして定義すると、後で扱いやすい
    DEBUG_VIDEO_PATH = BASE_DIR / "debug" / "debug_10.mp4"

    # --- 便利関数 (スタティックメソッド) ---
    
    @staticmethod
    def get_filename(filepath: Union[str, Path], no_extension: bool = False) -> str:
        """
        ファイルパスからファイル名を取得する。
        
        Args:
            filepath (Union[str, Path]): ファイルのパス。
            no_extension (bool, optional): Trueの場合、拡張子なしのファイル名を返す。
                                            デフォルトは False。
        Returns:
            str: ファイル名。
        """
        path_obj = Path(filepath)
        return path_obj.stem if no_extension else path_obj.name
    
    # ▼▼▼ 新しく追加する関数 ▼▼▼
    @staticmethod
    def create_directory(base_path: Union[str, Path], dir_name: Optional[str] = None) -> Path:
        """
        指定されたパスにディレクトリを作成する。

        Args:
            base_path (Union[str, Path]): ディレクトリを作成する基準となるパス。
            dir_name (Optional[str], optional): 作成するディレクトリ名。
                                                Noneの場合、base_pathの最後の部分が
                                                ディレクトリ名として扱われる。
                                                デフォルトは None。

        Returns:
            Path: 作成されたディレクトリのフルパス。
        """
        base_path = Path(base_path)
        
        # dir_nameが指定されていれば、それをbase_pathに結合する
        # そうでなければ、base_path自体を目的のディレクトリとする
        target_dir = base_path / dir_name if dir_name else base_path
        
        # ディレクトリが存在しない場合のみ作成する (parents=Trueで中間ディレクトリも作成)
        target_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"ディレクトリを確認・作成しました: {target_dir}")
        return target_dir

# --- 実行確認 ---
if __name__ == '__main__':
    # クラス変数の使い方 (インスタンス化は不要)
    print("--- パス設定の確認 ---")
    print(f"ベースディレクトリ: {Config.BASE_DIR}")
    print(f"データディレクトリ: {Config.DATA_DIR}")
    print(f"デバッグビデオのパス: {Config.DEBUG_VIDEO_PATH}")
    print(f"ビデオは存在しますか？: {Config.DEBUG_VIDEO_PATH.exists()}")

    # スタティックメソッドの使い方 (インスタンス化は不要)
    print("\n--- get_filenameの確認 ---")
    video_filename = Config.get_filename(Config.DEBUG_VIDEO_PATH)
    print(f"ビデオのファイル名 (拡張子あり): {video_filename}")

    video_filename_stem = Config.get_filename(Config.DEBUG_VIDEO_PATH, no_extension=True)
    print(f"ビデオのファイル名 (拡張子なし): {video_filename_stem}")