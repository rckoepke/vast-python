from setuptools import setup, find_packages

setup(
    name='vast',
    version='0.1.0',
    install_requires=['requests', 'pandas', 'argh'],
    url='https://github.com/vast-ai/vast-python',
    license='MIT',
    author='andrewchallis',
    author_email='andrewchallis@hotmail.co.uk',
    description='Vast.ai commandline access',
    packages=find_packages(),
    entry_points={
      'console_scripts': [
          'vast=vast.cli:vast',
          'vast-ai=vast.cli:vast_ai'
          ]
      }
)
