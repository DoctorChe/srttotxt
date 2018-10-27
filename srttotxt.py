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

version = "0.1.3"


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


def convert_srt_to_txt(text, join=0):
    """
Удаление служебных строк из файла
    """
    lines = text.split('\n')
    result = []
    out = ""
    for line in lines:
        # Пропускаем пустые строки
        # if line.strip().isspace():
            # continue
        if len(line.strip()) == 0:
            continue
        # Пропускаем строки состоящие только из цифр
        elif line.strip().isdigit():
            continue
        # Пропускаем строки имеющие формат "00:00:00,000 --> 00:00:03,090"
        elif (line.strip()[:1].isdigit() and line.strip()[2] == ':'
                and line.strip()[3:4].isdigit()
                and line.strip()[5] == ':'
                and line.strip()[6:7].isdigit()):
            continue
        else:
            result.append(line.strip())
    # if namespace.join == 1:
    if join == 1:
        # Объединяем строки в предложения
        for line in result:
            if out.endswith("."):
                out = out + "\n" + line
            else:
                out = out + " " + line
    else:
        # Объединяем строки без разбора на предложения
        out = "\n".join(result)
    return out


def clean_srt(text_srt):
    """
    Удаление HTML-разметки из текста
    """
    return re.sub(r'</?font.*?>', '', text_srt)


def main():
    try:
        parser = create_parser()
        namespace = parser.parse_args(sys.argv[1:])

        # Считываем исходный текст из файла
        text_srt = namespace.inputfile.read()

        if namespace.clean:
            # Удаляем HTML-разметку из текста
            text_srt_cleaned = clean_srt(text_srt)
            # Получаем путь для очищенного файла
            cleaned_file = f"{os.path.splitext(namespace.inputfile.name)[0]}_cleaned.srt"
            with open(cleaned_file, "w") as fout:
                fout.write(text_srt_cleaned)
        else:
            # Конвертируем текст
            text_txt = convert_srt_to_txt(text_srt, namespace.join)

            # Записываем переконвертированный текст в файл
            if namespace.outputfile:
                namespace.outputfile.write(text_txt)
            else:
                # Получаем путь для выходного файла
                output_file = f"{os.path.splitext(namespace.inputfile.name)[0]}.txt"
                with open(output_file, "w") as fout:
                    fout.write(text_txt)

    except IOError:
        print("Во время конвертации произошла ошибка")
    else:
        print("Конвертация файла произведена успешно")


if __name__ == '__main__':
    main()
