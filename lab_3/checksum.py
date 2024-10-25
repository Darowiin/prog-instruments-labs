import argparse
import csv
import hashlib
import json
import logging
import re
from typing import List

import chardet

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='file.log',
                    filemode='a'
                    )

PATTERN = {
    "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    "http_status_message": r'^\d{3} [A-Za-z ]+$',
    "snils": r'^\d{11}$',
    "passport": r'^\d{2} \d{2} \d{6}$',
    "ip_v4": r'^(?:\d{1,3}\.){3}\d{1,3}$',
    "longitude": r'^-?\d+\.\d+$',
    "hex_color": r'^#[0-9a-fA-F]{6}$',
    "isbn": r'(\d{3}-)?\d-(\d{5})-(\d{3})-\d',
    "locale_code": r'^[a-z]{2}(-[a-z]{2})?$',
    "time": r'^\d{2}:\d{2}:\d{2}\.\d{6}$'
}


def detect_encoding(file_path: str) -> str:
    """
    Определяет кодировку файла с помощью библиотеки chardet.

    :param file_path: Путь к CSV файлу.
    :return: Кодировка файла в виде строки.
    """
    try:
        with open(file_path, 'rb') as file:
            raw_data = file.read(10000)
            return chardet.detect(raw_data)['encoding']
    except Exception as ex:
        logging.error(f"Не удалось распознать кодировку: {ex}")


def validate_row(row: dict) -> dict:
    """
    Проверяет строки на соответствие регулярным выражениям.

    :param row: Словарь, представляющий строку CSV.
    :return: Словарь с недопустимыми значениями и их ключами.
    """
    try:
        invalid_data = {key: row[key] for key, pattern in PATTERN.items()
                        if not re.match(pattern, row.get(key, "").strip('"'))}
        return invalid_data
    except Exception as ex:
        logging.error(f"Не удалось проверить строку на валидность: {ex}")


def check_csv(file_path: str) -> tuple:
    """
    Проверяет CSV файл и возвращает недопустимые строки и их номера.

    :param file_path: Путь к CSV файлу.
    :return: Кортеж из списка недопустимых строк и списка их номеров.
    """
    encoding = detect_encoding(file_path)
    invalid_rows = []
    invalid_row_numbers = []
    try:
        with open(file_path, mode='r', encoding=encoding) as file:
            reader = csv.DictReader(file, delimiter=';')
            for index, row in enumerate(reader):
                invalid_data = validate_row(row)
                if invalid_data:
                    invalid_rows.append({
                        "row": row,
                        "invalid_data": invalid_data
                        })
                    invalid_row_numbers.append(index)
        return invalid_rows, invalid_row_numbers
    except Exception as ex:
        logging.error(f"Не удалось обработать CSV файл: {ex}")


def calculate_checksum(row_numbers: List[int]) -> str:
    """
    Вычисляет контрольную сумму (MD5) по номерам строк.

    :param row_numbers: Список номеров невалидных строк.
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
    parser = argparse.ArgumentParser(
        description='Программа для вычисления контрольной суммы')
    parser.add_argument('--file_path',
                        type=str,
                        help='Путь к CSV файлу',
                        default="57.csv")
    parser.add_argument('--variant',
                        type=int,
                        help='Номер варианта',
                        default=57)
    args = parser.parse_args()
    
    invalid_entries, invalid_row_numbers = check_csv(args.file_path)
    checksum = calculate_checksum(invalid_row_numbers)

    serialize_result(args.variant, checksum)

    logging.info(f"{len(invalid_entries)} invalid entries found.")
    logging.info(f"Check sum: {checksum}")
