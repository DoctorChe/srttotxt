#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import argparse
import os.path
import re

version = "0.1.2"


def create_parser():
    # Создаем класс парсера
    parser = argparse.ArgumentParser(
        prog='srttotxt',
        description='''Программа для перевода файлов субтитров
формата SRT в текстовые файлы формата TXT''',
        epilog='''(c) Doctor_Che 2017. Автор программы, как всегда,
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
    return parser


def get_file_name(srt_path):
    # Разделяем путь и имя файла
    (path, srt_name) = os.path.split(srt_path)
    # Выполняем замену
    # if os.path.exists(srt_name):
    txt_name = srt_name[0:-3] + "txt"
    # Возвращаем новый путь
    return os.path.join(path, txt_name)


def convertsrttotxt(text):
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
    if namespace.join == 1:
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
    return re.sub(r'</?font.*?>','',text_srt)


if __name__ == '__main__':
    try:
        parser = create_parser()
        namespace = parser.parse_args(sys.argv[1:])

        # Считываем исходный текст из файла
        text_srt = namespace.inputfile.read()

        # Удаляем HTML-разметку из текста
        text_srt_cleaned = clean_srt(text_srt)
        
        # Конвертируем текст
        text_txt = convertsrttotxt(text_srt_cleaned)

        # Записываем переконвертированный текст в файл
        if namespace.outputfile:
            namespace.outputfile.write(text_txt)
        else:
            try:
                outputfile = get_file_name(namespace.inputfile.name)
                with open(outputfile, "w") as fout:
                    fout.write(text_txt)
            except IOError:
                print("Во время записи файла произошла ошибка")
    except IOError:
        print("Во время конвертации произошла ошибка")
    else:
        print("Конвертация файла произведена успешно")
