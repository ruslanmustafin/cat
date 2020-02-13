import setuptools


setuptools.setup(
    name="cat", 
    version="0.0.1",
    author="Ruslan Mustafin",
    author_email="ruslan.s.mustafin@gmail.com",
    description="Compensair automatic translator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        #"License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'fire==0.2.1',
        'tqdm==4.40.2',
        'jinja2==2.10.3',
        'googletrans==2.4.0'
    ],
    python_requires='>=3.6',
)