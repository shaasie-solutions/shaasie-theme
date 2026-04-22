from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = [
        line.strip()
        for line in f.readlines()
        if line.strip() and not line.strip().startswith("#")
    ]

from shaasie_theme import __version__ as version

setup(
    name="shaasie_theme",
    version=version,
    description="Cairo font and print style for ERPNext — clean install and uninstall",
    author="Shaasie Solutions",
    author_email="support@shaasie.com",
    license="MIT",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
