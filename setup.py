from setuptools import setup, find_packages

setup(
    name="geojson2osm",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "xmltodict",
        "pytest"
    ],
    author="Kshitijraj Sharma",
    author_email="skshitizraj@gmail.com",
    description="A Python package to convert GeoJSON data to OSM XML format",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kshitijrajsharma/geojson2osm",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    license="MIT",
    license_file="LICENSE",
)
