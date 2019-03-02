import setuptools

with open("Readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="game-starter",
    version="1.0.0",
    author="Daniel Bailey",
    author_email="",
    description="Decides when to start a game, based on who's holding a button.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danieljabailey/GameStarter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
