def parse_numbers(input_string):
    result = []

    if not input_string.strip():  # 空文字列や空白のみの場合
        return [0]

    parts = input_string.split(",")  # "," で分割

    for part in parts:
        if "-" in part:
            try:
                start, end = map(int, part.split("-"))  # "-"で分割し数値に変換
                result.extend(range(start, end + 1))  # 範囲内の数を追加
            except ValueError:
                continue  # 無効な値の場合は無視
        else:
            try:
                result.append(int(part))  # 数値を追加
            except ValueError:
                continue  # 無効な値の場合は無視

    return result if result else [0]  # 結果が空の場合は[0]を返す

def create_string_from_numbers(numbers):
    if not numbers:
        return "0"

    numbers = sorted(set(numbers))  # 重複を排除してソート
    ranges = []
    start = end = numbers[0]

    for num in numbers[1:]:
        if num == end + 1:  # 連続している場合
            end = num
        else:  # 連続が途切れた場合
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

def intersect_strings(string_a, string_b):
    list_a = parse_numbers(string_a)
    list_b = parse_numbers(string_b)

    intersection = sorted(set(list_a) & set(list_b))  # 積集合を計算

    return create_string_from_numbers(intersection)

# 使用例
string_a = "17,19,21,26,45,47,49-54,56-58,60-63,65,67,70-72,75,76,78"
string_b = "1,11,17,19,25-28,29,31,33,35-38,40-45,47,48,50-56,59,61-64,66,69,72"
print(len(parse_numbers(string_a)))
print(len(parse_numbers(string_b)))

output = intersect_strings(string_a, string_b)
print(output)  # "3-5,8"
print(len(parse_numbers(output)))
