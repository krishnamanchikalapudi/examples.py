#  Package and distribution management

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="src", # Replace with your own username
    version="0.0.1",
    author="Krishna Manchikalapudi",
    author_email="Krishna.Manchikalapudi@yahoo.com",
    description="Machine Learning App",
    url="https://github.com/krishnamanchikalapudi/examples.py/MachineLearning",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)