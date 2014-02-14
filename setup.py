# encoding: utf-8

from setuptools import setup
import os.path

setup(
    name="datasift-beta",
    version="2.0.0",
    author="DataSift",
    author_email="opensource@datasift.com",
    maintainer="DataSift",
    maintainer_email="opensource@datasift.com",
    description="The official DataSift API library for Python.",
    long_description = os.path.isfile("README.rst") and open('README.rst').read() or None,
    license=(
        "Copyright (C) 2012-Present by MediaSift Ltd. "
        "All Rights Reserved. "
        "See LICENSE for the full license."
    ),
    url="https://github.com/datasift/datasift-python",
    packages=['datasift'],
    install_requires=[
        'requests <3.0.0, >=2.2.0',
        'autobahn <0.8.0, >=0.7.4',
        'six <1.6.0, >=1.5.2',
        'twisted <14.0.0, >=13.0.0'
    ],
    tests_require=[
        'httmock >=1.1.1, < 2.0.0',
        'pytest',
        'beautifulsoup4'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
