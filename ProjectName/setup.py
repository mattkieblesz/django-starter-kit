#!/usr/bin/env python
import os
import os.path
import sys

from distutils.command.build import build as BuildCommand
from setuptools import setup, find_packages
from setuptools.command.sdist import sdist as SDistCommand
from setuptools.command.develop import develop as DevelopCommand

ROOT = os.path.realpath(os.path.join(os.path.dirname(sys.modules['__main__'].__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))

VERSION = '0.0.1.dev'

dev_requires = [
    'flake8>=3.2.1',
    'pycodestyle>=2.2',
    'ipdb',
]

tests_require = [
    'pytest-cov>=2.4.0',
    'pytest-timeout>=1.2.0',
    'pytest-xdist>=1.15.0',
]

install_requires = [
    'click>=6.6',
    'Django>=1.10,<1.11',
    'django-debug-toolbar>=1.6.0',
    'django-ordered-model>=1.3.0',
    'django-redis>=4.6.0',
    'django-semanticui-form>=0.0.1',
    'django-user-accounts>=2.0.0',
    'simplejson>=3.10.0',

    'exam>=0.10.6',
    'pytest>=3.0.5',
    'pytest-django>=3.1.2',
    'pytest-html>=1.12.0',
    'PyYAML>=3.12',
    'structlog==16.1.0',
    'psycopg2==2.6.2',
    'uwsgi>2.0.0,<2.1.0',
]

cmdclass = {
    'sdist': SDistCommand,
    'build': BuildCommand,
    'develop': DevelopCommand,
}

setup(
    name='<% project_name %>',
    version=VERSION,
    author='Noone',
    author_email='noone@noland.no',
    description='Collaboration platform.',
    long_description=open(os.path.join(ROOT, 'README.md')).read(),
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'dev': dev_requires,
        'tests': tests_require,
    },
    cmdclass=cmdclass,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            '<% project_name %> = <% project_name %>.runner:main',
        ],
        'flake8.extension': [],
    },
)
