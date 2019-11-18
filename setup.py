import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='latexmk-pipe',
    version='0.1',
    scripts=['latexmk-pipe'] ,
    author="Christophe Garion",
    author_email="tofgarion@runbox.com",
    description="A simple python-script in the spirit of rubber_pipe.py to be able to use latexmk with pipes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tofgarion/latexmk-pipe",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
