from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="dre-scraper",
    version="0.1",
    author="Luis Tavares, Marcio Duarte, Joao Renato Pinto",
    python_requires=">=3.6",
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=required,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
