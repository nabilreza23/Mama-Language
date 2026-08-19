from setuptools import setup

setup(
    name="mama-lang",
    version="1.0.0",
    author="Nabil Reza",
    description="The easiest and coolest programming language in the world!",
    py_modules=["mama"],
    entry_points={
        "console_scripts": [
            "mama=mama:main",
        ],
    },
    python_requires=">=3.8",
)
