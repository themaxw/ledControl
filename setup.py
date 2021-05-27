from setuptools import setup, find_packages

setup(
    name="ledControl",
    version="0.1",
    packages=find_packages(exclude=("venv")),
    include_package_data=True,
    # TODO requirements
    # install_requires=["Click", "pytest", "toml", "spidev", "colorlog"],
)
