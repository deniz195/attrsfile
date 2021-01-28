#!/usr/bin/env python

'''Tests for `attrsfile` package.'''

import pytest
import os
from pathlib import Path

import attr
from attrsfile import attrsfile


@pytest.fixture
def cd_chdir():
    """Sample pytest fixture. """
    os.chdir(Path(__file__).parent)


def test_d(cd_chdir):
    '''Testing basic use case with formatted filename.'''

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

    Path('abc99.yaml').unlink()


def test_attr():
    '''Testing basic use case with unformatted filename.'''

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

    Path('xyz.yaml').unlink()


def test_nested_attr():
    '''Testing basic use case with nested classes.'''

    @attr.s()
    class AB:
        a = attr.ib(99)
        b = attr.ib(42)

    @attrsfile('xyz_ab.yaml')
    @attr.s()
    class XYZ_AB:
        x = attr.ib(1)
        y = attr.ib(2)

        ab = attr.ib(factory=AB, type=AB)

    x1 = XYZ_AB()
    assert x1.filename() == 'xyz_ab.yaml'

    x1.save()
    x2 = XYZ_AB.load()
    assert x1 == x2

    Path('xyz_ab.yaml').unlink()


def test_import():
    from attrsfile import attrsfile
    from attrsfile import mapper
