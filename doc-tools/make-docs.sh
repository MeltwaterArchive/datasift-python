mkdir ../../master/datasift/doc
mkdir ../../master/datasift/doc/_static
cp Makefile ../../master/datasift/doc
cp conf.py ../../master/datasift/doc
cp index.rst ../../master/datasift/doc
cd ../../master/datasift/doc
export PYTHONPATH=$PYTHONPATH:../..
make html
#sphinx-build -b html ../../datasift-python gh-pages
cd ../../../gh-pages/doc-tools
cp -a ../../master/datasift/doc/_build/html/* ./..
