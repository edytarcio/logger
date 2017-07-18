# -*- coding: utf-8 -*-
import subprocess
from setuptools import setup, find_packages
from nfce import __version__

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

def sys_config():
    subprocess.call("sudo mkdir -p /var/log/logg",shell=True)
    subprocess.call("sudo mkdir -p /usr/local/share/logg",shell=True)
    subprocess.call("sudo chmod -R 777 /var/log/logg 1>/dev/null 2>/dev/null",shell=True)
    subprocess.call("sudo chmod -R 777 /usr/local/share/logg 1>/dev/null 2>/dev/null",shell=True)
    #subprocess.call("sudo useradd -m -d /home/nfce -s /bin/bash -g sudo nfce 1>/dev/null 2>/dev/null",shell=True)



sys_config()

__date__ = '20170704'


setup(
    name='logg',
    version=__version__,
    description='Loggs Monitoring',
    long_description=readme,
    url='https://',
    license=license,
    install_requires=[],
    packages=find_packages(exclude=('tests', 'docs')),
    data_files = [('/etc/init/', ['logger/loggserver.conf']),
        ],
    package_data={'logger': ['loggserver.conf', 'loggserver.service'],
        },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        ],
    scripts=['bin/loggserver',
        ],
)
