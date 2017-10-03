import re
from setuptools import setup


install_requires = [
    'django>=1.10,<1.12',
    'reportlab>=3.4,<3.5',
    'beautifulsoup4>=4.6,<4.7',
]

tests_require = [
    'flake8',
]

with open('README.rst') as fh:
    long_description = re.sub(
        '^.. start-no-pypi.*^.. end-no-pypi', '', fh.read(), flags=re.M | re.S)

setup(
    name='django-pdf-model',
    version='0.0.1',
    author='Tomasz Knapik',
    author_email='tmkn@tmkn.uk',
    url='http://tmkn.uk',
    install_requires=install_requires,
    tests_require=tests_require,
    packages=['django_pdf'],
    include_package_data=True,
    license='BSD-2',
    long_description=long_description
)
