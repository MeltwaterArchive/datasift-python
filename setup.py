# encoding: utf-8

from setuptools import setup

setup(
    name="datasift",
    version="2.0.0",
    author="Courtney Robinson",
    author_email="courtney.robinson@datasift.com",
    maintainer="DataSift",
    maintainer_email="opensource@datasift.com",
    description="The official DataSift API library for Python.",
    long_description = open('README.rst').read(),
    license=(
        "Copyright (C) 2012 by MediaSift Ltd. "
        "All Rights Reserved. "
        "See LICENSE for the full license."
    ),
    url="https://github.com/datasift/datasift-python",
    packages=['datasift'],
    install_requires=[
        'requests<3.0.0',
        'autobahn<0.8.0',
        'six<1.6.0',
        'twisted<14.0.0'
    ],
    tests_require=[
        'httmock>=1.1.1',
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
        "Programming Language :: Python :: 3.3"
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
