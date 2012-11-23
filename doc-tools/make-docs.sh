mkdir ../../master/datasift/doc
cp Makefile ../../master/datasift/doc
cp conf.py ../../master/datasift/doc
cp index.rst ../../master/datasift/doc
sphinx-build -b html datasift-python gh-pages
cd ../../master/datasift/doc
cd ../../gh-pages/doc-tools
cp -a ../master/datasift/doc/_build/html ./..
