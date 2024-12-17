# PUR-GEN - polyurethane fragments generator

PUR-GEN (https://pur-gen.polsl.pl/) is a chemoinformatics online tool, which generates single structures or libraries of polyurethane (PUR) fragments.

Generated structures can be further used in computational analyses such as molecular docking, see:

[PUR-GEN: A Web Server for Automated Generation of Polyurethane Fragment Libraries, K. Szleper, M. Cebula, O. Kovalenko, A. Góra, A. Raczyńska, Computational and Structural Biotechnology Journal, 2024](https://doi.org/10.1016/j.csbj.2024.12.004)

<p align="center">
<img src="https://github.com/user-attachments/assets/0e51cd82-8dd7-427d-b2ea-b14d23d387b3" alt="graphical-abstract-v2" width="600"/>
</p>

## Running with Docker

To build and run the application using Docker, navigate to the project directory and execute the following commands:

### 1. Build the Docker Image
Build the Docker image with the name `pur-gen`:

```
docker build -t pur-gen .
```
### 2. Run the Docker Container
Run the container and forward the application to your local port 8080:
```
docker run --rm -it -p 8080:8080 pur-gen
```
**Note**: Press CTRL+C to stop the container.


## Running the Web Application Locally

### 1. Install Python Dependencies
After cloning the repository, install the Python dependencies using `requirements.txt`:
```
pip install -r requirements.txt
```
### 2. Run Application
```
$/usr/bin/python app.py
```


## Used packages:
The project utilizes the following libraries:

- [RDKit](https://www.rdkit.org/docs/index.html) - A toolkit for cheminformatics used to perform reactions.
- [Pybel](https://openbabel.org/docs/dev/UseTheLibrary/Python_Pybel.html) - A Python wrapper for Open Babel to generate 3D conformers.
- [Dash Python](https://dash.plotly.com/) - A framework for building interactive web applications in Python.
