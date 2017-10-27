from setuptools import setup

setup(
    name='falcon_ask',
    version='0.0.1',
    description='Toolkit for writing Amazon Alexa skills in your Falcon app',
    author='Philamer Sune',
    url='https://github.com/pvsune/falcon_ask',
    classifiers=[
        'Development Status :: 1 - Development/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 3.5',
        'Topic :: Home Automation',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    packages=['falcon_ask'],
    license='ISC',
    test_requires=['tox'],
    install_requires=[
        'pyOpenssl==17.3.0'
    ]
)
