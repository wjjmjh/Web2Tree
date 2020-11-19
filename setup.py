from setuptools import setup, find_packages

setup(
    name="Web2Tree",
    version="0.0",
    description="An elegant way to hack front ends.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["anytree"],
    extras_require={"dev": [
        "anytree",
        "pytest",
        "tox",
        "black",
        "isort",
    ]},
)
