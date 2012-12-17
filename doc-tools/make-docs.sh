#!/bin/sh -v
if [ -z "$1" ]; then
    echo 'You must run this script with branch name as its argument, e.g.'
    echo 'sh ./make-docs.sh master'
    exit
fi
echo 'working on branch '$1
echo 'installing tools'
sudo apt-get install git
sudo apt-get install python-setuptools
sudo easy_install Pygments
sudo easy_install jinja
sudo easy_install sphinx
echo 'making temporary directory'
mkdir tmp
cd tmp
echo 'cloning repos'
git clone https://github.com/datasift/datasift-python.git code
git clone https://github.com/datasift/datasift-python.git gh-pages
cd code
git checkout $1
cd ..
cd gh-pages
git checkout gh-pages

mkdir -p ../code/datasift/doc/_static
cp doc-tools/Makefile ../code/datasift/doc
cp doc-tools/conf.py ../code/datasift/doc
cp doc-tools/index.rst ../code/datasift/doc
cd ../code/datasift/doc
export PYTHONPATH=$PYTHONPATH:../..
make html
cd ../../gh-pages
cp -a ../code/datasift/doc/_build/html/* .

git add *
git commit -m 'Updated to reflect the latest changes to '$1
echo 'You are going to update the gh-pages branch to reflect the latest changes to '$1
git push origin gh-pages
echo 'finished'
