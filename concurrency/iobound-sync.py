import requests
from argparse import ArgumentParser

from utils import timer


def download_site(url: str) -> bytes:
    """Downloads a website given the url.

    Args:
        url: str, the url of the website
    Returns:
        bytes
    """
    with requests.get(url) as response:
        print(f"Read {len(response.content)} from {url}")
        return response.content


@timer
def download_all_sites(sites: list) -> None:
    """Downloads all websites given as input.

    Args:
        sites: list of strings, websites to download
    """
    for url in sites:
        download_site(url)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-n', '--n-sites', type=int, default=30, help='Number of websites to download')
    args = parser.parse_args()

    sites = ["http://olympus.realpython.org/dice"] * args.n_sites
    download_all_sites(sites)
