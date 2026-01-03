from setuptools import setup, find_packages

setup(
    name="app",
    version="0.1.0",
    description="Grocery App List Manager",
    author="Uriah Erter",
    package_dir={'': "src"},
    packages=find_packages(where="sc=rc"),
    entry_points={"console_scripts": ["app=app.app_launch:main"]},
    install_requires=[],
    python_requires=">=3.7",
)
