from setuptools import setup
from setuptools import find_packages

setup(
    name="server_sms_proj",
    version="0.1",
    author="Gabriel Bulz",
    url='https://github.com/GabrelBulz/sms_project',
    description='Server ,api and db for handling metrics',
    install_requires=['pika', 'flask', 'sqlalchemy', 'pandas'],
    packages=find_packages()
)
