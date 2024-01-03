# PURge - polyurethane fragments generator
![image](https://github.com/kataszl203/oligomer_webapp/assets/40094884/d0721108-889d-4258-a42d-891c39f91c00)

Used packages:

RDKit https://www.rdkit.org/docs/index.html

Pybel https://openbabel.org/docs/dev/UseTheLibrary/Python_Pybel.html

Dash Python https://dash.plotly.com/

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
$pip install dash dash-html-components dash-core-components dash-daq
```
### Build patched openbabel
```
$chmod +x ./build_openbabel.sh
$./build_openbabel.sh
```
### Running the web application locally
```
$/usr/bin/python app.py
```
