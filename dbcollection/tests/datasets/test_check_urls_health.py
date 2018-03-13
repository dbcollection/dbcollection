"""
Test dataset's urls download status.
"""

import requests
import pytest

from dbcollection.utils.test import check_url_redirect
from dbcollection.core.api.metadata import get_list_urls_dataset


TIMEOUT_SECONDS = 3


@pytest.mark.parametrize("dataset_name, urls", get_list_urls_dataset())
@pytest.mark.slow
def test_check_urls_are_valid(dataset_name, urls):
    for url in urls:
        response = requests.head(url)  # try without redirect enabled
        if response.status_code == 200:
            status = True
        else:
            if response.status_code == 301:
                status = check_url_redirect(url, TIMEOUT_SECONDS)  # try with redirect enabled
            else:
                status = False
        assert status, 'Error downloading urls from {}: {}'.format(dataset_name, url)
