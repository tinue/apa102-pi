import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="APA102_Pi",
    version="2019.3",
    author="Martin Erzberger",
    author_email="martin@erzberger.ch",
    description="Driver for APA102 LEDs on a Raspberry Pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tinue/APA102_Pi",
    python_requires='>3',
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Intended Audience :: Education",
        "Operating System :: POSIX :: Linux",
        "Topic :: Education",
        "Topic :: System :: Hardware :: Hardware Drivers",
    ),
    install_requires=["Adafruit-GPIO"],
    platforms=("Raspbian Stretch")
)