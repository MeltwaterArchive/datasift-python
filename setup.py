# encoding: utf-8

from setuptools import setup
import os.path

setup(
    name="datasift",
    version="2.11.0",
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
        'requests <3.0.0, >=2.8.0',
        'autobahn <0.10.0, >=0.9.4',
        'six <2.0.0, >=1.6.0',
        'twisted <16.0.0, >=14.0.0',
        'pyopenssl <0.16.0, >=0.15.1',
        'python-dateutil <3, >=2.1',
        'service_identity >= 14.0.0',
        'requests-futures >= 0.9.5',
        'ndg-httpsclient >= 0.4.0'
    ],
    tests_require=[
        'httmock >=1.1.1, < 2.0.0',
        'pytest',
        'beautifulsoup4',
        'behave'
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
