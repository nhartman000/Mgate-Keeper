from setuptools import setup, find_packages

setup(
    name='mgate-keeper',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'openai',
        'google-generativeai',
        'python-dotenv',
    ],
)