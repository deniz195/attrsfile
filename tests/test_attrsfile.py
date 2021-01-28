#!/usr/bin/env python

'''Tests for `attrsfile` package.'''

import pytest

import attr
from attrsfile import attrsfile


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    '''Sample pytest test function with the pytest fixture as an argument.'''
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_d():
    @attrsfile('abc{x}.yaml')
    @attr.s()
    class D:

        x = attr.ib(1)
        y = attr.ib(2)

        def to_dict(self):
            return attr.asdict(self)

        @classmethod
        def from_dict(cls, d):
            return cls(**d)

    d1 = D(x=99, y=42)
    d1.to_dict()

    assert d1.save() == 'abc99.yaml'

    import pytest

    with pytest.raises(FileNotFoundError):
        D.load(x=2)

    d2 = D.load(x=99)
    assert d1 == d2


def test_attr():
    @attrsfile('xyz.yaml')
    @attr.s()
    class XYZ:
        x = attr.ib(1)
        y = attr.ib(2)

    x1 = XYZ()
    assert x1.filename() == 'xyz.yaml'

    x1.save()
    x2 = XYZ.load()
    assert x1 == x2


def test_import():
    from attrsfile import attrsfile
    from attrsfile import mapper
