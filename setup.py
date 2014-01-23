# encoding: utf-8

from setuptools import setup

setup(
    name="datasift",
    version="2.0.0",
    author="Courtney Robinson",
    author_email="courtney.robinson@datasift.com",
    maintainer="DataSift",
    maintainer_email="opensource@datasift.com",
    description=("The official DataSift API library for Python."),
    license="Copyright (C) 2012 by MediaSift Ltd. All Rights Reserved. See LICENSE for the full license.",
    url="https://github.com/datasift/datasift-python",
    packages=['datasift'],
    install_requires=['requests>=2.2.0', 'autobahn>=0.7.4', 'six>=1.5.2', 'twisted>=13.0.0'],
    tests_require=['httmock>=1.1.1', 'pytest', 'beautifulsoup4'],
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
