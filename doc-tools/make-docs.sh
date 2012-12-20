#!/bin/bash
#-v

export BASE_DIR="$( cd "$( dirname $0 )/../../../.." && pwd )/"

source ${BASE_DIR}ms-tools/doc-tools/docathon/sub/make-docs-util-defs.sh
initialise $*

### Python-specific parameters
parameters "python"

### installation of Python-specific tools
message "installing tools"
sudo apt-get install git
sudo apt-get install python-setuptools
sudo easy_install Pygments
sudo easy_install jinja
sudo easy_install sphinx

pre_build

### Python-specific build steps

message "preparing to build documents"
mkdir -p ${CODE_DIR}datasift/doc/_static ; stop_on_error
cp -v ${GH_PAGES_DIR}doc-tools/Makefile ${CODE_DIR}datasift/doc ; stop_on_error
cp -v ${GH_PAGES_DIR}doc-tools/conf.py ${CODE_DIR}datasift/doc ; stop_on_error
cp -v ${GH_PAGES_DIR}doc-tools/index.rst ${CODE_DIR}datasift/doc ; stop_on_error

(
	message "building documents"
	cd ${CODE_DIR}datasift/doc ; stop_on_error
	export PYTHONPATH="${PYTHONPATH}:${CODE_DIR}"
	make html ; stop_on_error
) || error "stopped parent"
(
	message "copying documents"
	cd ${GH_PAGES_DIR} ; stop_on_error
	cp -a "${CODE_DIR}datasift/doc/_build/html/*" . ; stop_on_error
) || error "stopped parent"

(
	cd ${GH_PAGES_DIR} ; stop_on_error
	git add *
) || error "stopped parent"

post_build

finalise
