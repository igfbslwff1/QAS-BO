from setuptools import setup, find_packages

setup(
    name='QAS-BO',
    version='1.0',
    packages=find_packages(),
    install_requires=[line.strip() for line in open("requirements.txt", "r")],
)
