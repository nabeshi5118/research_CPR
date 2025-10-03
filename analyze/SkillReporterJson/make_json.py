import json

def parse_numbers(input_string):
    result = []
    if not input_string.strip():
        return result
    parts = input_string.split(",")
    for part in parts:
        if "-" in part:
            try:
                start, end = map(int, part.split("-"))
                result.extend(range(start, end + 1))
            except ValueError:
                continue
        else:
            try:
                result.append(int(part))
            except ValueError:
                continue
    return result

def create_string_from_numbers(numbers):
    if not numbers:
        return ""
    numbers = sorted(set(numbers))
    ranges = []
    start = end = numbers[0]
    for num in numbers[1:]:
        if num == end + 1:
            end = num
        else:
            if start == end:
                ranges.append(f"{start}")
            else:
                ranges.append(f"{start}-{end}")
            start = end = num
    if start == end:
        ranges.append(f"{start}")
    else:
        ranges.append(f"{start}-{end}")
    return ",".join(ranges)

def process_json(file_path, output_path):
    # JSONファイルを読み込む
    with open(file_path, 'r') as file:
        data = json.load(file)

    # データを処理
    for outer_item in data:  # 外側のリストを繰り返し処理
        for key, records in outer_item.items():  # 各アイテムの辞書を処理
            for record_id, record in records.items():
                depth_times = parse_numbers(record.get("AppDepthTime", ""))
                recoil_times = parse_numbers(record.get("AppRecoilTime", ""))

                # AppDepthCountとAppRecoilCountを更新
                record["AppDepthCount"] = len(depth_times)
                record["AppRecoilCount"] = len(recoil_times)

                # AppCompressionTimeを計算して更新
                intersection = sorted(set(depth_times) & set(recoil_times))
                record["AppCompressionTime"] = create_string_from_numbers(intersection)

                # AppCompressionCountを更新
                record["AppCompressionCount"] = len(intersection)

    # 更新したJSONを保存
    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)

# 使用例
input_file_path = 'SkillReporter_C.json'  # 入力ファイルパス
output_file_path = 'SkillReporter_C_updated.json'  # 出力ファイルパス
process_json(input_file_path, output_file_path)
print(f"更新されたファイルは {output_file_path} に保存されました。")
