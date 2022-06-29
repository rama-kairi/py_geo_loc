from setuptools import find_packages, setup

setup(
    name="py_geo_loc",
    packages=find_packages(),
    version="1.0.0",
    description="A Python Package to get the latitude and longitude of a location",
    author="Ramananda Kairi",
    license="MIT",
    author_email="ramanandakairi@gmail.com",
    install_requires=["requests"],
)
