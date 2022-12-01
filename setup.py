# the instruction to do when pip installing
# set up
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(name='eCommerce',
      description='eCommerce Model (recommender)',
      packages=find_packages(),
      install_requirements =requirements,
      url='https://github.com/sailormoonvicky/eCommerce')
