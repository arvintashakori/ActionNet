from io import open
from os import path
from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# get reqs
def requirements():
    list_requirements = []
    with open('requirements.txt') as f:
        for line in f:
            list_requirements.append(line.rstrip())
    return list_requirements

setup(
      name='FairFrost',
      version='1.0.0',
      description='FairFrost: A Hypernetwork-based Freezing Algorithm for Fair and Self Aware Personalized Federated Learning',
      url='hhttps://github.com/arvintashakori/ActionNet',
      author='Arvin Tashakori',
      license='All rights reserved for Arvin Tashakori 2022-2023',
      author_email='arvin@ece.ubc.ca',
      packages=find_packages(exclude=['']),
      python_requires='>=3.8',
      install_requires=requirements()
)
