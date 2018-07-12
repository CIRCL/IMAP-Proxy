#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='imapproxy',
    version='1.0.0',
    author='Xavier Schul',
    author_email='schul.x@hotmail.com',
    maintainer='Xavier Schul',
    url='https://github.com/CIRCL/IMAP-Proxy',
    description='IMAP Proxy to sanitize attachments and share threats to MISP',
    packages=['imapproxy'],
    scripts=['bin/start.py', 'bin/test_proxy.py', 'bin/test_pycircleanmail.py'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Security'
    ]
)