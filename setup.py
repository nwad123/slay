from setuptools import setup

setup(
    name='slay',
    version='0.1.0',
    py_modules=['slay'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'slay = slay:cli',
        ],
    },
)
