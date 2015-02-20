#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'colorama>=0.3.3',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='checkocr',
    version='0.1.0',
    description="",
    long_description=readme,
    author="Chris Developer",
    author_email='chris@chrisdeveloper.com',
    url='https://github.com/lendenmc/checkocr',
    packages=[
        'checkocr',
    ],
    package_dir={'checkocr':
                 'checkocr'},
    include_package_data=True,
    install_requires=requirements,
    license="GPL v3",
    zip_safe=False,
    keywords='checkocr',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
