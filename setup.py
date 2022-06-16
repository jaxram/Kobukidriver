import setuptools

with open("README.rst","r") as rfile:
    long_description=rfile.read()

setuptools.setup(
    name="kobukidriver",
    version='0.0.7',
    
    author="Parthasarathi,Ram sankar,Ganesh",
    author_email="parthasarathi_s@tce.edu,ramsankarcsr@gmail.com,ganeshma2015@tce.edu",
    description="A simple python driver  for Kobuki mobile robot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Topic :: Communications",
        "Topic :: Software Development",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        #"Development Status::5 - Production/Stable",
        
    ],
    python_requires=">=3.6",
    py_modules=["kobukidriver"],
    #package_dir={'':'kobukidriver'},
    install_requires=['pyserial'],
    

)
