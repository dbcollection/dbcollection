"""
Test dataset's urls download status.
"""


import pytest
import signal
import requests
from dbcollection.core.api import fetch_list_datasets


TIMEOUT_SECONDS = 3


def get_list_urls_dataset():
    available_datasets = fetch_list_datasets()
    dataset_urls = []
    for name in available_datasets:
        url_list = []
        urls = available_datasets[name]['urls']
        for url in urls:
            if isinstance(url, str):
                url_list.append(url)
            elif isinstance(url, dict):
                try:
                    url_ = url['url']
                    url_list.append(url_)
                except KeyError:
                    pass  # do nothing
            else:
                raise Exception('Unknown format when downloading urls: {}'.format(type(url)))
        # add list to the out dictionary
        dataset_urls.append((name, url_list))
    return dataset_urls


class Timeout():
    """Timeout class using ALARM signal."""
    class Timeout(Exception):
        pass

    def __init__(self, sec):
        self.sec = sec

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)

    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm

    def raise_timeout(self, *args):
        raise Timeout.Timeout()


def check_url_redirect(url):
    try:
        with Timeout(TIMEOUT_SECONDS):
            response = requests.get(url)
            return response.status_code == 200
    except Timeout.Timeout:
        return True


@pytest.mark.parametrize("dataset_name, urls", get_list_urls_dataset())
def test_check_urls_are_valid(dataset_name, urls):
    for url in urls:
        response = requests.head(url)  # try without redirect enabled
        if response.status_code == 200:
            status = True
        else:
            if response.status_code == 301:
                status = check_url_redirect(url)  # try with redirect enabled
            else:
                status = False
        assert status, 'Error downloading urls from {}: {}'.format(dataset_name, url)
