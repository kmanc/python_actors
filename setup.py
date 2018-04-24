import os
from setuptools import setup


# Utility function to read the README.md file.
def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name="pythonactors",
    version="0.0.1",
    author="Kevin Conley",
    author_email="kmanc@comcast.net",
    description="Actor implementation in Python",
    license='MIT',
    keywords="Python, Actor, Concurrency, Parallelism",
    url="https://github.com/kmanc/python_actors",
    packages=['actors'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: Release",
        "Topic :: Utilities"
    ],

    setup_requires=[
        'pytest-runner',
    ],
    tests_require=['pytest']
)
