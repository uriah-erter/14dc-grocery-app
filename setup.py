from setuptools import find_packages, setup

setup(
    # distribution name (can be different from import/package name)
    name="grocery-app",
    version="0.1.0",
    description="Grocery App List Manager",
    author="Uriah Erter",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": [
            "app=app.app_launch:main",
        ]
    },
    python_requires=">=3.10",
)
