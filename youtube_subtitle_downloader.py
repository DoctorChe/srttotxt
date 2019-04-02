import subprocess
import os


def download_subtitle(url):
    """
    Скачивает субтитры с youtube используя youtube-dl
    :param url: url видео
    :return: имя файла субтитров
    """
    try:
        output = subprocess.check_output(["youtube-dl", "--skip-download", "--write-sub", url],
                                         universal_newlines=True)
        s = "[info] Writing video subtitles to: "
        file_name = [x[len(s):] for x in output.split("\n") if x.startswith(s)][0]
        if os.path.isfile(file_name):
            file_name = os.path.join(os.getcwd(), file_name)
        else:
            raise FileNotFoundError
        return file_name
    except (FileNotFoundError, IndexError):
        return None
