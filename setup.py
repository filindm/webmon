from setuptools import setup
import os


with open('requirements.txt', 'r') as f:
    requirements = [line for line in f]

setup(
    name="webmon",
    version="0.9",
    zip_safe=False,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "webmon = webmon.app:main",
        ],
    },
    author="Dmitry Filin",
    license="Apache 2.0",
    platforms=["POSIX", "MacOS"],
    description="Webmon - tool to monitor website availability",
    url="https://github.com/filindm/webmon/",
)
