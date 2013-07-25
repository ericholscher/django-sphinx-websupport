import codecs
try:
    from setuptools import setup, find_packages
    extra_setup = dict(
        install_requires = ['django'],
        )
except ImportError:
    from distutils.core import setup
    extra_setup = {}

setup(
    name='django-sphinx-websupport',
    version='1.2.3',
    author='Eric Holscher',
    author_email='eric@ericholscher.com',
    url='http://github.com/ericholscher/django-sphinx-websupport',
    license='BSD',
    description='Django backend for Sphinx Websupport package.',
    package_dir={'': '.'},
    packages=find_packages('.'),
    long_description=codecs.open("README.rst", "r", "utf-8").read(),
    **extra_setup
)
