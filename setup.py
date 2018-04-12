import os
from setuptools import setup

# Utility function to read the README.md file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "actors",
    version = "0.0.1",
    author = "your name",
    author_email = "yname@riotgames.com ",
    description = ("Example Project"),
    keywords = "Python, Example, Template",
    url = "https://github.com/kmanc/python_actors",
    packages=['actors'],
    #scripts=[
    #    'bin/start.py'
    #],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities"
    ],
    #   Development Status:
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable

    setup_requires=[
        'pytest-runner',
    ],
    tests_require=['pytest', 'pytest-env', 'mock']
)
