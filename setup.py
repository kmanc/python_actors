from setuptools import setup


setup(
    name="py_actors",
    version="0.0.6",
    author="Kevin Conley",
    author_email="kmanc@comcast.net",
    description="Actor implementation in Python",
    license='MIT',
    keywords="Python, Actor, Concurrency, Parallelism",
    url="https://github.com/kmanc/py_actors",
    packages=['py_actors'],
    long_description='A package designed to abstract parts of the actor model so that a developer can write clean, '
                     'actor-driven Python code. See documentation at https://kmanc.github.io/python_actors/',
    python_requires='>=3.6',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities"
    ],

    setup_requires=[
        'pytest-runner',
    ],
    tests_require=['pytest']
)
