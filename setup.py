from setuptools import find_packages
from setuptools import setup

setup(
    name="mars-rover",
    version="0.1",
    py_modules=["src/cli"],
    include_package_data=True,
    install_requires=["click"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points="""
        [console_scripts]
        mars-rover=cli:cli
    """,
)
