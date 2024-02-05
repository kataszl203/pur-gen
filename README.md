# PURGE - polyurethane fragments generator
![image](https://github.com/kataszl203/oligomer_webapp/assets/40094884/d0721108-889d-4258-a42d-891c39f91c00)

Used packages:

RDKit https://www.rdkit.org/docs/index.html

Pybel https://openbabel.org/docs/dev/UseTheLibrary/Python_Pybel.html

Dash Python https://dash.plotly.com/

## Dependencies for Debian/Ubuntu
### Libraries needed to run the script
```
# apt update && apt -y install --no-install-recommends\
                python3\
                python3-pip\
                librdkit1\
                rdkit-data

$ pip install matplotlib dash dash-html-components dash-core-components dash-daq openbabel-wheel rdkit

```
### Running the web application locally
```
$/usr/bin/python app.py
```

### Running with docker

go to the project directory and use following commands

build (with image name `purge`):
```
docker build -t purge .
```

run (with forwarding app on local port 8080, ctrl-c to stop):
```
docker run --rm -it -p 8080:8080 purge
```

