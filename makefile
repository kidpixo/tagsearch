#see Makefiles in python projects https://krzysztofzuraw.com/blog/2016/makefiles-in-python-projects.html
.DEFAULT_GOAL := install_package

###############################################################
# remeber to activate the appropiate virtualenviroment first! #
###############################################################
# basic build targets

install_package : ## install the package from setup.py via setuptools first running build_ext
	python setup.py install --verbose

install_develop :  ## install the package from setup.py via setuptools as development 
	python setup.py -q develop --verbose

###############################################################
# cleaning

clean-pyc: ## remove all pyc, pyo and __pycache__
	find . -name '*.pyc' -exec rm -rf {} +
	find . -name '*.pyo' -exec rm -rf {} +
	find . -name '__pycache__'  -exec rm -rf {} +

clean-build: ## clean all build products
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

###############################################################
# testing

test: clean-pyc ## run clean-pyc and test
	py.test --verbose --color=yes

help: ## Show this help. Only double comments will show up!
	@grep -h "## " $(MAKEFILE_LIST) | grep -v grep | sort  

