#!/usr/bin/env python

from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

PACKAGE = 'riotgen'


def get_long_description():
    # Get the long description from the README file
    with open('README.rst', encoding='utf-8') as f:
        return f.read()


def get_version():
    """Get the version from package __init__.py file."""
    with open(path.join(PACKAGE, '__init__.py'), encoding='utf-8') as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


setup(
    name=PACKAGE,
    version=get_version(),

    description='riotgen: generator for RIOT application/driver/board code',
    long_description=get_long_description(),
    long_description_content_type='text/x-rst',

    url='https://github.com/aabadie/riot-generator',

    author='Alexandre Abadie',
    author_email='alexandre.abadie@inria.fr',

    license='',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
    ],

    keywords='generator code',
    platforms='any',
    packages=[PACKAGE],
    include_package_data=True,
    package_dir={
        'riotgen': 'riotgen'
    },
    package_data={
        'riotgen': [
            'templates/*/*',
        ]
    },
    install_requires=[
        'click',
        'Jinja2',
    ],
    entry_points={
        'console_scripts': [
            '{}=riotgen:cli'.format(PACKAGE),
        ],
    },
)
