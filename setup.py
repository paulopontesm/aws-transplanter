from setuptools import find_packages, setup

with open(".version") as fh:
    version = fh.read()

with open("README.md") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="aws_transplanter",
    version=version,
    description="Explore AWS Organization structure",
    author="pmartins.dev",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email="paulo@pmartins.dev",
    scripts=["bin/aws_transplanter"],
    url="https://github.com/paulopontesm/aws_transplanter",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: System :: Networking",
        "Topic :: Other/Nonlisted Topic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    keywords="aws security Amazon",
    packages=find_packages(exclude=["test", "venv"]),
    install_requires=requirements,
)
