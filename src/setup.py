#!/bin/env python3
from setuptools import setup

setup(
    name="img2pdf",
    version="1.1",
    description="Merge images into one pdf file including useful optiıns via command line.",
    author="Elagoht",
    author_email="furkanbaytekin@gmail.com",
    url="https://github.com/Elagoht/img2pdf",
    install_requires=[
        "fonttools>=>4.38.0",
        "fpdf2>=2.6.0",
        "Pillow>=9.3.0",
        "python-magic>=0.4.27",
        # "python-magic-bin==0.4.14", for Windows
    ],
    entry_points={
        "console_scripts":[
            "img2pdf+ = img2pdf.main:main"
        ]
    }
)
