import json
import os
import csv  # csvモジュールをインポート
from pathlib import Path
from typing import Union, Optional, List

# =================================================================
# 1. パス管理クラス
# =================================================================
class Config:
    """プロジェクト全体のパス設定を管理するクラス。"""
    
    # --- パス設定 (クラス変数) ---
    BASE_DIR = Path(__file__).resolve().parent
    OUTPUTS_DIR = BASE_DIR / "outputs"
    JSON_OUTPUT_DIR = OUTPUTS_DIR / "json"
    CSV_OUTPUT_DIR = OUTPUTS_DIR / "csv" # CSV用のパスも追加
    DEBUG_VIDEO_PATH = BASE_DIR / "debug" / "debug_10.mp4"

    # --- 便利関数 (スタティックメソッド) ---
    
    @staticmethod
    def get_filename(filepath: Union[str, Path], no_extension: bool = False) -> str:
        """ファイルパスからファイル名を取得する。"""
        path_obj = Path(filepath)
        return path_obj.stem if no_extension else path_obj.name
    
    @staticmethod
    def create_directory(base_path: Union[str, Path], new_folder_name: Optional[str] = None) -> Path:
        """指定されたパスにディレクトリを作成する。"""
        base_path_obj = Path(base_path)
        if new_folder_name:
            target_dir = base_path_obj / new_folder_name
        else:
            target_dir = base_path_obj
        target_dir.mkdir(parents=True, exist_ok=True)
        print(f"ディレクトリを確認・作成しました: {target_dir}")
        return target_dir

# =================================================================
# 2. JSON操作関連
# =================================================================

# (ConfigJsonクラスと関連関数は変更なしのため、省略します)
# ... (前のコードと同じものがここに入ります) ...

def mkdir_setup(file_path: Union[str, Path]):
    """
    ファイルのフルパスを受け取り、そのファイルが存在するディレクトリを作成し、
    ファイルがなければ空のJSONファイルを作成する。
    """
    path_obj = Path(file_path)
    dir_path = path_obj.parent
    dir_path.mkdir(parents=True, exist_ok=True)
    if not path_obj.exists():
        with open(path_obj, 'w', encoding='utf-8') as f:
            json.dump({}, f, indent=4)

def path_to_dict(json_path: Union[str, Path]) -> dict:
    """JSONパスからデータを読み込み、辞書として返す。"""
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

class ConfigJson:
    """結果出力用のJSONファイルを操作するクラス。"""

    def __init__(self, json_path: Union[str, Path]):
        self._json_path = Path(json_path)
        mkdir_setup(self._json_path)
       
    def add(self, add_data: dict):
        """JSONファイルにデータを追加・更新する。"""
        mkdir_setup(self._json_path)
        current_data = path_to_dict(self._json_path)
        current_data.update(add_data)
        with open(self._json_path, 'w', encoding='utf-8') as f:
            json.dump(current_data, f, indent=4)

    def load(self, word: str, tmp_i: Optional[int] = None, tmp_j: Optional[int] = None):
        """JSONファイルから特定のキーの値を取得する。"""
        tmp_dict = path_to_dict(self._json_path)
        if tmp_i is None:
            return tmp_dict.get(word)
        elif tmp_j is None:
            return tmp_dict.get(word, [])[tmp_i]
        else:
            return tmp_dict.get(word, [])[tmp_i][tmp_j]

    def dict(self) -> dict:
        """JSONファイルの内容全体を辞書として返す。"""
        return path_to_dict(self._json_path)

# =================================================================
# 3. CSV操作関連
# =================================================================

class ConfigCSV:
    """CSVファイルの操作を管理するクラス。"""

    def __init__(self, csv_path: Union[str, Path]):
        """特定のCSVファイルパスを扱うインスタンスを作成する。"""
        self.csv_path = Path(csv_path)

    @staticmethod
    def initialize_files(base_dir: Union[str, Path], num_files: int = 17) -> List[Path]:
        """
        指定されたディレクトリに、連番の空のCSVファイルを指定された数だけ作成する。
        (旧 initialize_yolo_csv_files)

        Args:
            base_dir (Union[str, Path]): ファイルを作成する親ディレクトリのパス。
            num_files (int): 作成するCSVファイルの数。

        Returns:
            List[Path]: 作成された全CSVファイルのパスのリスト。
        """
        base_dir_path = Path(base_dir)
        # ディレクトリが存在しない場合は作成
        base_dir_path.mkdir(parents=True, exist_ok=True)
        
        csv_paths = []
        for i in range(num_files):
            # 0.csv, 1.csv, ... という名前でファイルを作成
            csv_file_path = base_dir_path / f'{i}.csv'
            # 'w'モードでファイルを開くと、既存のファイルは空になる（初期化される）
            with open(csv_file_path, 'w', newline='') as f:
                pass  # 空のファイルを作成するだけ
            csv_paths.append(csv_file_path)
            
        print(f"{num_files}個のCSVファイルを '{base_dir_path}' に作成・初期化しました。")
        return csv_paths

    def get_column_values(self, column_name: str) -> List[str]:
        """インスタンスが持つCSVファイルの指定した列の値をリストで返す。"""
        # (この部分のコードは変更ありません)
        values = []
        if not self.csv_path.exists():
            print(f"エラー: ファイルが存在しません: {self.csv_path}")
            return values
            
        try:
            with open(self.csv_path, mode='r', encoding='utf-8', newline='') as file:
                reader = csv.DictReader(file)
                if column_name not in (reader.fieldnames or []):
                    raise ValueError(f"指定された列名 '{column_name}' はヘッダーに存在しません。")
                for row in reader:
                    values.append(row[column_name])
        except Exception as e:
            print(f"エラーが発生しました: {e}")
        return values
    
    @staticmethod
    def write_rows(csv_path: Union[str, Path], data_rows: List[List], mode: str = 'w'):
        """
        指定された単一のCSVファイルに、複数行のデータ（リストのリスト）を一括で書き込む。

        Args:
            csv_path (Union[str, Path]): 書き込み先のファイルパス。
            data_rows (List[List]): 書き込むデータ。
            mode (str, optional): 書き込みモード ('w': 上書き, 'a': 追記)。デフォルトは 'w'。
        """
        try:
            with open(csv_path, mode, newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(data_rows) # writerowsで一括書き込み
        except Exception as e:
            print(f"CSVファイル '{csv_path}' への書き込み中にエラーが発生しました: {e}")
# =================================================================
# 4. 実行確認
# =================================================================
if __name__ == '__main__':
    # ... (JSONまでの実行確認は省略) ...
    
    # --- ConfigJsonクラスの動作確認 ---
    print("\n--- 3. ConfigJsonの確認 ---")
    my_result_json_path = Config.JSON_OUTPUT_DIR / "my_result.json"
    json_handler = ConfigJson(my_result_json_path)
    json_handler.add({"city": "Tokyo", "skills": ["Python", "C++"]})
    print(f"操作対象のJSONファイル: {my_result_json_path}")
    
    # --- ConfigCSVクラスの動作確認 ---
    print("\n--- 4. ConfigCSVの確認 ---")
    
    # YOLO用のCSVファイルを作成するディレクトリを定義
    yolo_csv_dir = Config.CSV_OUTPUT_DIR / "yolo_test_run"
    
    # 1. YOLO用のCSVファイルを一括で初期化
    csv_file_list = initialize_yolo_csv_files(yolo_csv_dir)
    
    # 2. 最初のCSVファイル (0.csv) にサンプルデータを書き込む
    target_csv_path = csv_file_list[0]
    print(f"\nサンプルデータを '{target_csv_path}' に書き込みます...")
    with open(target_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['frame', 'x', 'y']) # ヘッダー
        writer.writerow([1, 100, 200])
        writer.writerow([2, 105, 210])
        writer.writerow([3, 110, 220])
    
    # 3. ConfigCSVクラスを使って、特定の列のデータを読み込む
    csv_handler = ConfigCSV(target_csv_path)
    x_values = csv_handler.get_column_values('x')
    
    print(f"'{target_csv_path}' から 'x' の列を読み込みました: {x_values}")