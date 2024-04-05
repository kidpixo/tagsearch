# -*- coding: utf-8 -*-
# # # pylint: disable=C0111,W0511
from setuptools import setup, find_packages

# setup the installation
setup(
    name='tagsearch',
    version='0.0.1',
    description='',
    url='',
    author="Mario D'Amore",
    author_email='kidpixo@gmail.com',
    license='MIT',
    # list : https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=(
        [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
            ]
    ),
    keywords='yaml frontmatter search',
    scripts=['tagsearch/tagsearch_script'],
    entry_points={ 
        "console_scripts": [ "tagsearch = tagsearch.main:main" ]
        },
    # TODO: Update this as we add dependencies
    # use setup.py + requirements.tx trick, see
    # setup.py vs requirements.txt
    # https://caremad.io/posts/2013/07/setup-vs-requirement/
    install_requires=[
        "docopt",
        "PyYAML",
        "python-frontmatter",
        "tinydb"
    ],
    # },
    # zip_safe=False,
    # MANIFEST.in declare what to include and here we declare to do that.
    packages=find_packages(),
    include_package_data=True,
)
