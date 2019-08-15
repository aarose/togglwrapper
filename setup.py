from os import path
from setuptools import setup


here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()
    f.close()

with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().split('\n')
    f.close()


with open(path.join(here, 'test_requirements.txt')) as f:
    test_requirements = f.read().split('\n')
    f.close()


setup(
    name='togglwrapper',
    version='1.2.0',
    short_description="Library to easily interface with Toggl's API.",
    long_description=long_description,
    url='https://github.com/aarose/togglwrapper',
    author='aarose (Anarosa Paredes)',
    author_email='hello@aarose.red',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='toggl timetracking API wrapper',

    packages=['togglwrapper'],
    package_data={'': ['LICENSE', 'NOTICE']},

    # List run-time dependencies here.
    install_requires=requirements,

    # Development dependencies. Install using :
    extras_require={
        'dev': test_requirements,
    },
)
