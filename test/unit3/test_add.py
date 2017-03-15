import pytest


@pytest.fixture
def add2():
    return 2+2

def test_add2(add2):
    assert add2 == 4
