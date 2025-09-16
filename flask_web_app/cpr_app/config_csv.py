#Yoloのキーポイントの数だけcsvファイルを作成している
import os
from .config_json import ConfigJson
import csv

class ConfingCSV():
    def __init__(self,csv_pass,other=None):
        self.csv_path = csv_pass
        if other =="YOLO":
            process_initialize_csv_YOLO(csv_pass)

    def get_column_values(self, column_name):
    #CSVファイルの指定した列の値をリストで返す関数。
        values = []
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                if column_name not in reader.fieldnames:
                    raise ValueError(f"指定された列名 '{column_name}' は存在しません。")
                for row in reader:
                    values.append(row[column_name])
        except Exception as e:
            print(f"エラーが発生しました: {e}")
        return values


def process_initialize_csv_YOLO(csv_path):
    #パーツごとにCSVフォルダ生成&ファイルを初期化する
    #cpr_app/output/csv/video名
    #video名はyear_month_day_hour_min
    #ファイル名はキー番号だけ
    #YOLO以外は、videoに数字を入れればその数だけtmp_paths以下に指定した数だけcsvファイルを作成する
    csv_paths = []
    #yoloに対応したディレクトリを作成している
    landmark = 17

    for i in range(landmark):
          #os.path.joinは2つのパスをくっつけれる
        #キーポイント毎にcsvファイルを作成
        csv_file_path = os.path.join(csv_path, f'{i}.csv')
            #パスの合成
        csv_paths.append(csv_file_path)

    set_csv(csv_paths)    
    return csv_paths

def set_csv(csv_file_paths):
    for i,csv_filename in enumerate(csv_file_paths):
        with open(csv_filename, 'w') as f:
        #ファイル内の初期化
            f.truncate(0)

