import sys
import setuptools
try:
    import Adafruit_GPIO
except ImportError:
    sys.stdout.write('This package requires the Adafruit_Python_GPIO library to be installed. '
                      'See https://github.com/adafruit/Adafruit_Python_GPIO for installation instructions.')
    sys.exit(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="APA102_Pi",
    version="2018.1",
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
    platforms=("Raspbian Stretch")
)