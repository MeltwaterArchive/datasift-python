# encoding: utf-8

from setuptools import setup
from datasift import __version__

# read the install requirements from the requirements.txt
try:
    fh = open('requirements.txt')
    required = fh.read().splitlines()
except:
    if fh:
        fh.close()
    raise

setup(
    name = "datasift",
    version = __version__,
    author = "Stuart Dallas",
    author_email = "stuart@3ft9.com",
    maintainer = "MediaSift Ltd",
    maintainer_email = "opensource@datasift.com",
    description = ("The official DataSift API library for Python."),
    license = "Copyright (C) 2012 by MediaSift Ltd. All Rights Reserved. See LICENSE for the full license.",
    url = "https://github.com/datasift/datasift-python",
    packages=['datasift', 'tests'],
    install_requires=required,
    tests_require=['mock>=0.8.0', 'unittest2==0.5.1'],
    include_package_data = True,
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
