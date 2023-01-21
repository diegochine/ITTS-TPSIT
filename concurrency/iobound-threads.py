import requests
import threading
from argparse import ArgumentParser

from utils import timer


def download_site(url: str) -> bytes:
    with requests.get(url) as response:
        print(f"Read {len(response.content)} from {url}")
        return response.content


@timer
def download_all_sites(sites: list) -> None:
    threads = []
    for site in sites:
        t = threading.Thread(target=download_site, args=(site,))
        print(f'Starting thread {t.name}')
        t.start()
        threads.append(t)

    for t in threads:
        print(f'Waiting thread {t.name}')
        t.join()
        print(f'Joined thread {t.name}')


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-n', '--n-sites', type=int, default=30, help='Number of websites to download')
    args = parser.parse_args()

    sites = ["http://olympus.realpython.org/dice"] * args.n_sites
    download_all_sites(sites)
