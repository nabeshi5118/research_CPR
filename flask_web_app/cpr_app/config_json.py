import json
import os
#結果出力用のjsonファイルを作成している
class ConfigJson():
    def __init__(self,json_path):
        self._json_path = json_path
        # ファイルパスのディレクトリを確認し、存在しない場合は作成
        mkdir_setup(json_path)
       
    #addについて
    #既存のデータは保持され、新しいキーと内容は追加する
    #もし、既存のキー名があれば内容が変更される
    def add(self,add_data):
        #なんでこれが必要なのかいまいちわからない(initの際にディレクトリ作ってるはずなんだけど...)
        mkdir_setup(self._json_path)

        #print(self._json_pass + "add json")
        with open(self._json_path,'r') as f:
            data = json.load(f)
        data.update(add_data)
        with open(self._json_path,'w') as f:
            json.dump(data,f,indent=4) 

    #jsonファイルの内容物１個だけを返す
    def load(self,word,tmp_i=None,tmp_j=None):
        tmp_dict = path_to_dict(self._json_path)

        if tmp_i is None:
            return tmp_dict[word]
        elif tmp_i is not None and tmp_j is None:
            return tmp_dict[word][tmp_i]
        else:
            return tmp_dict[word][tmp_i][tmp_j]

    #jsonデータを辞書にして送る
    def dict(self,json_path = None):
        if json_path == None:
            data = path_to_dict(self._json_path)
        else:
            data = path_to_dict(json_path)
        return data

#パスから辞書を返す
def path_to_dict(json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

#パスからディレクトリを作って初期化する
def mkdir_setup(json_path):
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

        # ファイルが存在しない場合、新しいファイルを作成
    if not os.path.exists(json_path):
        with open(json_path, 'w') as f:
            json.dump({}, f)  # 空のJSONオブジェクトを初期化


