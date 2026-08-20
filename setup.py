from setuptools import setup, find_packages

setup(
    name="mama-lang",
    version="2.0.0",
    description="Mama Language - An intuitive Bengali keyword-based programming language interpreter",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="Nabil Reza",
    url="https://github.com/nabilreza23/Mama-Language",
    py_modules=["mama"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "mama=mama:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
