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
    version=version,
    packages=find_packages(),
    install_requires=[
        'pyramid',
    ],
    extras_require=dict(
        tests=tests_require,
    ),
    tests_require=tests_require,
)
