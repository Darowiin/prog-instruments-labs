import json
import csv
import re
import hashlib
from typing import List, Tuple
import chardet

PATTERN = {
    "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    "http_status_message": r'^\d{3} [A-Za-z ]+$',
    "snils": r'^\d{11}$',
    "passport": r'^\d{2} \d{2} \d{6}$',
    "ip_v4": r'^(?:\d{1,3}\.){3}\d{1,3}$',
    "longitude": r'^-?\d+\.\d+$',
    "hex_color": r'^#[0-9a-fA-F]{6}$',
    "isbn": r'^\d+-\d+-\d+-\d+-\d+$',
    "locale_code": r'^[a-z]{2}(-[a-z]{2})?$',
    "time": r'^\d{2}:\d{2}:\d{2}\.\d{6}$'
}


def detect_encoding(file_path: str) -> str:
    with open(file_path, 'rb') as file:
        raw_data = file.read(10000)
        return chardet.detect(raw_data)['encoding']


def validate_row(row: dict) -> dict:
    invalid_data = {key: row[key] for key, pattern in PATTERN.items() if not re.match(pattern, row.get(key, "").strip('"'))}
    return invalid_data


def parse_csv(file_path: str) -> tuple:
    encoding = detect_encoding(file_path)
    invalid_rows = []
    invalid_row_numbers = []
    
    with open(file_path, mode='r', encoding=encoding) as file:
        reader = csv.DictReader(file, delimiter=';')
        for index, row in enumerate(reader):
            invalid_data = validate_row(row)
            if invalid_data:
                invalid_rows.append({"row": row, "invalid_data": invalid_data})
                invalid_row_numbers.append(index)
    
    return invalid_rows, invalid_row_numbers


def calculate_checksum(row_numbers: List[int]) -> str:
    """
    Вычисляет контрольную сумму (MD5) по номерам строк.

    :param row_numbers: Список целочисленных номеров строк, которые были недопустимыми.
    :return: Строка, представляющая контрольную сумму в формате MD5.
    """
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()


def serialize_result(variant: int, checksum: str) -> None:
    """
    Сериализует результаты в файл result.json.

    :param variant: Номер варианта.
    :param checksum: Контрольная сумма, вычисленная через calculate_checksum().
    """
    result = {
        "variant": variant,
        "checksum": checksum
    }
    with open('result.json', 'w') as json_file:
        json.dump(result, json_file, indent=4)


if __name__ == "__main__":
    file_path = "lab_3/57.csv"  # Путь к файлу
    variant_number = 57  # Номер варианта

    invalid_entries, invalid_row_numbers = parse_csv(file_path)
    checksum = calculate_checksum(invalid_row_numbers)

    serialize_result(variant_number, checksum)

    print(f"Найдено {len(invalid_entries)} недопустимых записей.")
    print(f"Контрольная сумма: {checksum}")
