from setuptools import setup
from setuptools import find_packages

setup(
    name="client_sms",
    version="0.1",
    author="Gabriel Bulz",
    url='https://github.com/GabrelBulz/sms_project',
    description='Client for sending metrics to a server',
    install_requires=['pika', 'psutil'],
    packages=find_packages()
)
