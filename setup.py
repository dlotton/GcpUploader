from setuptools import setup


def requirements(path):
    with open(path) as f:
        return f.read().splitlines()


setup(
    name="garmin-uploader",
    version=open("VERSION").read().replace('\n', ''),
    author="Bastien Abadie",
    author_email="bastien@nextcairn.com",
    description="A tool to upload FIT, GPX, and TCX files"
                "to the Garmin Connect web site.",
    url="https://github.com/La0/garmin-uploader",
    license="GPL",
    keywords="GARMIN CONNECT GPS TCX GPX FIT UPLOAD UPLOADER",
    packages=['garmin_uploader'],
    install_requires=requirements('requirements.txt'),
    tests_require=requirements('requirements-tests.txt'),
    entry_points={
        'console_scripts': [
            'gupload = garmin_uploader.cli:main',
        ]
    },
    package_data={
        'garmin_uploader': ['*.txt'],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Topic :: Utilities",
    ],
)
