#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
    Converter from SRT to TXT format.

    Usage: srttotxt.py [-h] [-v] [-i INPUTFILE] [-o [OUTPUTFILE]] [-j [JOIN]] [-c [CLEAN]]

      -h, --help                    show this help message and exit
      -v, --version                 show version of the program
      -i, --inputfile INPUTFILE     input file name
      -o, --outputfile OUTPUTFILE   output file name
      -j, --join 0|1                join lines (0 - no, 1 - yes)
      -c, --clean 0|1               clean SRT file of HTML markup (0 - no, 1 - yes) and exit

    Example:
    python3 srttotxt.py -i The-Fate-of-the-First-Stars-Space-Time.srt

    :copyright: (c) 2018 by Doctor_Che
    :license: GPLv3, see LICENSE for more details.
"""

import sys
import argparse
import os.path
import re

version = "0.2.1"


def create_parser():
    # Создаем класс парсера
    parser = argparse.ArgumentParser(
        prog='srttotxt.py',
        description='''Программа для перевода файлов субтитров
формата SRT в текстовые файлы формата TXT''',
        epilog='''(c) Doctor_Che 2018. Автор программы, как всегда,
не несет никакой ответственности ни за что.''',
        add_help=False
        )
    # Создаем группу параметров для родительского парсера,
    # ведь у него тоже должен быть параметр --help / -h
    # parent_group = parser.add_argument_group (title='Параметры')

    parser.add_argument('-h', '--help', action='help', help="Справка")
    parser.add_argument('-v', '--version',
                        action='version',
                        help='Вывести номер версии',
                        version='%(prog)s {}'.format(version))
    parser.add_argument('-i', '--inputfile',
                        default="inputfile.srt",
                        type=argparse.FileType('r'),
                        help="input file")
    parser.add_argument('-o', '--outputfile',
                        nargs='?',
                        type=argparse.FileType('w'),
                        help="output file")
    parser.add_argument('-j', '--join',
                        nargs='?',
                        default=0,
                        type=int,
                        help="Объединение строк в предложения")
    parser.add_argument('-c', '--clean',
                        nargs='?',
                        default=0,
                        type=int,
                        help="Очистка файла от HTML-разметки")
    return parser


def convert_srt_to_txt(text, join=False):
    """
    Removing information lines from file
    :param text: String in SRT format
    :param join: Merge lines into sentences
    :return: String in TXT format
    """
    lines = text.split('\n')
    result = []
    for line in lines:
        if not line.strip():  # Пропускаем пустые строки
            continue
        elif line.strip().isdigit():  # Пропускаем строки состоящие только из цифр
            continue
        elif (line.startswith("WEBVTT") or
              line.startswith("Kind: captions") or
              line.startswith("Language: en")):  # Пропускаем строки состоящие содержащие служебную информацию
            continue
        # Пропускаем строки имеющие формат "00:00:00,000 --> 00:00:03,090"
        elif re.match(r"\d{2}:\d{2}:\d{2}.\d{3} --> \d{2}:\d{2}:\d{2}.\d{3}", line.strip()):
            continue
        else:
            result.append(line.strip())
    if join:
        out = join_lines(result)  # Объединяем строки в предложения
    else:
        out = "\n".join(result)  # Объединяем строки без разбора на предложения
    return out


def join_lines(lst):
    """
    Merge lines into sentences
    :param lst: List of strings
    :return: String with sentences
    """
    out = ""
    for line in lst:
        if line.startswith("[") and line.endswith("]"):
            out = f"{out}\n{line}\n"
        elif out.endswith("."):
            out = f"{out}\n{line}"
        else:
            out = f"{out} {line}"
    return out


def clean_srt(text_srt):
    """
    Удаление HTML-разметки из текста
    """
    return re.sub(r"</?font.*?>", "", text_srt)


def main():
    output_file = ""
    try:
        parser = create_parser()
        namespace = parser.parse_args(sys.argv[1:])

        text_srt = namespace.inputfile.read()  # Считываем исходный текст из файла

        base, _ = os.path.splitext(namespace.inputfile.name)

        if namespace.clean:
            text_srt_cleaned = clean_srt(text_srt)  # Удаляем HTML-разметку из текста
            cleaned_file = f"{base}_cleaned.srt"  # Получаем путь для очищенного файла
            with open(cleaned_file, "w") as fout:
                fout.write(text_srt_cleaned)
        else:
            text_txt = convert_srt_to_txt(text_srt, namespace.join)  # Конвертируем текст

            # Записываем переконвертированный текст в файл
            if namespace.outputfile:
                output_file = namespace.outputfile.name
                namespace.outputfile.write(text_txt)
            else:
                output_file = f"{base}.txt"  # Получаем путь для выходного файла
                with open(output_file, "w") as fout:
                    fout.write(text_txt)

    except IOError:
        print("Во время конвертации произошла ошибка")
    else:
        print("Конвертация файла произведена успешно")
        print(f"Сохранённый файл: '{output_file}'")


if __name__ == '__main__':
    main()
