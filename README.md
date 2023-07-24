# oligomer_webapp
Web application for the tool oligomer.
![image](https://github.com/kataszl203/oligomer_webapp/assets/40094884/133d98c3-1fa5-4b2e-b78b-c147e4763247)

Used packages:

RDKit https://www.rdkit.org/docs/index.html

Pybel https://openbabel.org/docs/dev/UseTheLibrary/Python_Pybel.html

Shiny for Python https://shiny.rstudio.com/py/

## Dependencies for Debian/Ubuntu
### Libraries needed to run the script
```
$apt update
$apt -y install --no-install-recommends\
                build-essential\
                ca-certificates\
                cmake\
                git\
                zlib1g-dev\
                libcairo2-dev\
                libboost-dev\
                libboost-program-options-dev\
                libboost-iostreams-dev\
                libboost-regex-dev\
                rapidjson-dev\
                python3-dev\
                libbz2-dev\
                libeigen3-dev\
                libxml2-dev\
                swig\
                lzma\
                python3-rdkit\
                python3-pip\
                librdkit1\
                rdkit-data\
                wget
$pip install matplotlib
$pip install shiny
```
### Build patched openbabel
```
$chmod +x ./build_openbabel.sh
$./build_openbabel.sh
```
### Running the web application locally
```
$/usr/bin/python -m shiny run --reload app.py
```
