from setuptools import find_packages, setup # type: ignore

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="instabase-foundation",
    version="0.0.3",
    author="Instabase",
    author_email="support@instabase.com",
    description="Foundation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/instabase/foundation",
    packages=find_packages('py'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_dir={'': 'py'},
    install_requires=[
        'mypy==0.790',
    ]
)
