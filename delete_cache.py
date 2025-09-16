import os
import shutil
class DeleteCache():
    def __init__(self):
        self._file_names =  [
        "cpr_app/static/result",
        "cpr_app/uploads",
        "cpr_app/output_analyzing",
        "cpr_app/results",
        # 他のパスを追加
    ]

    def delete_cache(self):
        for path in self._file_names:
            delete_contents_of_directory(path)

def count_files_and_dirs(path):
    file_count = 0
    dir_count = 0
    for root, dirs, files in os.walk(path):
        file_count += len(files)
        dir_count += len(dirs)
    return file_count, dir_count

def delete_contents_of_directory(path):
    if os.path.exists(path):
        file_count, dir_count = count_files_and_dirs(path)
        print(f"The directory {path} contains {file_count} files and {dir_count} directories.")
        if file_count != 0:
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    file_path = os.path.join(root, name)
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    shutil.rmtree(dir_path)
                    print(f"Deleted directory: {dir_path}")
            print(f"Deletion completed for {path}.")
        else:
            print("This directory is empty.")
    else:
        print(f"The path {path} does not exist")


def delete_specific_file(path, file_name):
    # 再帰的に指定されたディレクトリを探索
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == file_name:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")


if __name__ == "__main__":
    path_to_search = "/home/watanabe/research/Docker-composes/flask_CPR_web_app"
    file_name_to_delete = "yolov8x-pose-p6.pt"  # 削除したいファイル名

    # 指定したパスの配列を入力してください
    directory_paths = [
        "cpr_app/static/result",
        "cpr_app/uploads",
        "cpr_app/output_analyzing",
        "cpr_app/results",
        # 他のパスを追加
    ]
    for directory_path in directory_paths:
        delete_contents_of_directory(directory_path)

    #delete_specific_file(path_to_search, file_name_to_delete)

