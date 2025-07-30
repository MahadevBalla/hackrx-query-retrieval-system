import requests


def download_file(url: str, dest="temp.pdf") -> str:
    r = requests.get(url)
    with open(dest, "wb") as f:
        f.write(r.content)
    return dest
