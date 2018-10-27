import subprocess


def download_subtitle(url):
    try:
        subprocess.run(["youtube-dl",
                        "--skip-download",
                        "--write-sub",
                        url])
        return True
    except FileNotFoundError:
        return False

# youtube-dl --skip-download --write-sub --sub-format srt --sub-lang en https://www.youtube.com/watch?v=4pSUtWBiuB4
