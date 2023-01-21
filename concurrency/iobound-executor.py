import requests
import concurrent.futures
from argparse import ArgumentParser

from utils import timer


def download_site(url: str) -> bytes:
    with requests.get(url) as response:
        print(f"Read {len(response.content)} from {url}")
        return response.content


@timer
def download_all_sites(sites: list) -> None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(download_site, sites)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-n', '--n-sites', type=int, default=30, help='Number of websites to download')
    args = parser.parse_args()

    sites = ["http://olympus.realpython.org/dice"] * args.n_sites
    download_all_sites(sites)
