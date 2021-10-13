from setuptools import setup, find_packages

setup(
    name="myclient",
    version="1.0.0",
    entry_points={
        "console_scripts": [
            "myclient=myclient.main:main",
            "myserver=myserver.main:main",
        ],
    },
    install_requires=[],
    packages=find_packages(exclude=["tests", "tests.*"]),
)
