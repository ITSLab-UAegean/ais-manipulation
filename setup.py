"""
Package setup.py
"""
from pathlib import Path
import setuptools


# reading long description from file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Load packages from requirements.txt
with open(Path('./', "requirements.txt"), "r",encoding='utf-8') as file:
    REQUIREMENTS = [ln.strip() for ln in file.readlines()]

# calling the setup function
setuptools.setup(
    name="ais_manipulation",
    version="0.1.0",
    description="Different functions to process and visualize AIS tracks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url='',
    author="Intelligent Transportation Systems, University of the Aegean.",
    author_email="",
    license="CC BY-NC-SA 4.0",
    package_dir={"": "src"},
    packages=setuptools.find_packages(
        where="src", include=["ais_manipulation", "ais_manipulation.*", "ais_manipulation.utils", "ais_manipulation.utils.*"]
    ),
    classifiers=[
        "Development Status :: 4 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS ",
        "License :: CC BY-NC-SA 4.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=REQUIREMENTS,
    keywords="AIS density map",
    python_requires=">=3.8",

)
