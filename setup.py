import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apa102-pi",
    version="2.4.1",
    author="Martin Erzberger",
    author_email="martin@erzberger.ch",
    description="Driver for APA102 LEDs on a Raspberry Pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tinue/apa102-pi",
    python_requires='>3',
    packages=setuptools.find_packages(),
    license='GPLv2',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Intended Audience :: Education",
        "Operating System :: POSIX :: Linux",
        "Topic :: Education",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=["adafruit-circuitpython-bitbangio",
                      "adafruit-circuitpython-busdevice"],
    platforms=["Raspbian Buster", "Raspberry Pi"]
)
