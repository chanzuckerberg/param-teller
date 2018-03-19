from setuptools import setup

setup(
    name='param_teller',
    version='0.0.1',
    description='Library to retrieve parameters security from AWS parameter store.',
    url='http://github.com/chanzuckerberg/param_teller',
    author='Tiago Carvalho',
    author_email='tcarvalho@chanzuckerberg.com',
    license='MIT',
    packages=['param_teller'], install_requires=['boto3'])
