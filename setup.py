from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

version = '0.0.0'
try:
    import pyramid_handy
    version = pyramid_handy.__version__
except ImportError:
    pass

tests_require = [
    'webtest',
    'pytest',
    'pytest-cov',
    'pytest-xdist',
    'pytest-capturelog',
]

setup(
    name='pyramid-handy',
    description='Some handy stuff for Pyramid web framework',
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    keywords='pyramid',
    author='Victor Lin',
    author_email='hello@victorlin.me',
    url='https://github.com/victorlin/pyramid-handy',
    license='MIT',
    version=version,
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pyramid',
        'future',
    ],
    extras_require=dict(
        tests=tests_require,
    ),
    tests_require=tests_require,
)
