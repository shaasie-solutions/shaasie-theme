from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = [
        line.strip()
        for line in f.readlines()
        if line.strip() and not line.strip().startswith("#")
    ]

from customize_erpnext import __version__ as version

setup(
    name="customize_erpnext",
    version=version,
    description="Custom desk themes, print styles, and print formats for ERPNext — Cairo font, RTL/LTR, clean install/uninstall",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Shaasie Solutions",
    author_email="support@shaasie.com",
    license="MIT",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
    python_requires=">=3.10",
)
