# encoding: utf-8

from setuptools import setup
from datasift import __version__

setup(
    name="datasift",
    version=__version__,
    author="Courtney Robinson"      ,
    author_email="courtney.robinson@datasift.com",
    maintainer="DataSift",
    maintainer_email="opensource@datasift.com",
    description=("The official DataSift API library for Python."),
    license="Copyright (C) 2012 by MediaSift Ltd. All Rights Reserved. See LICENSE for the full license.",
    url="https://github.com/datasift/datasift-python",
    packages=['datasift', 'tests'],
    pkg_resources=['requests>=2.0.1'],
    tests_require=[],
    include_package_data=True,
    platforms='any',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Setuptools Plugin",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
