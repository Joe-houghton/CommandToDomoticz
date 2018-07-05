from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CommandToDomoticz",
    version="0.9.0",
    author="Joe Houghton",
    author_email="github_joe_Houghton@outlook.com",
    description="Control Domoticz via Commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Joe-houghton/CommandToDomoticz",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    
    install_requires=['logging', 'json', 'requests'],
)
