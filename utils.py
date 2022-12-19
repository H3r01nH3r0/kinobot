from json import load, dump
from os import listdir
from io import BytesIO


def get_config(filename: str) -> dict:
    with open(filename, "r", encoding="utf-8") as file:
        data: dict = load(file)

    return data

def get_lang_file(lang: str) -> dict:
    filename = "locales/{}.json".format(lang)

    with open(filename, "r", encoding="utf-8") as f:
        return load(f)


def str2file(text: str, filename: str) -> BytesIO:
    file = BytesIO(text.encode())
    file.name = filename
    file.seek(0)

    return file


def check_int(query: str) -> bool:
    if query.startswith("-"):
        query = query[1:]

    return query.isdigit()

def save_config(filename: str, data: dict) -> None:
    for key in data.keys():
        if len(key) == 2:
            del data[key]

    with open(filename, "w", encoding="utf-8") as file:
        dump(data, file, indent=4, ensure_ascii=False)

def filter(message):
    message = message.split(' ')
    for x in message:
        if x.startswith('http'):
            return True
    return False
