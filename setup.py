from setuptools import find_packages, setup

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="vinext",
    version="0.1.0",
    description="Vietnamese Language Pack for Frappe / ERPNext",
    author="1nguoi.com",
    author_email="hello@1nguoi.com",
    url="https://github.com/mrhuychien/vinext",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
    license="GPL-3.0",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
)
