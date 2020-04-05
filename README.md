![Here should be logo :D](assets/logo.png?raw=true "distorme logo")

# distort --me
> CLI utility for augmentation and preprocessing images.
>
---
## Table of Contents
- [Installation](#installation)
- [Installation from source](#installation-from-source)
- [Usage](#usage)
- [Features](#features)
- [License](#license)

---
## Installation
```shell
$ pip install distortme
```

## Installation from source
> Install <a href=https://github.com/python-poetry/poetry>poetry</a> to build package
```shell 
$ pip install poetry
``` 

### Clone

> Clone repo to your local machine
```shell 
$ git clone https://github.com/rahowa/distortme.git
```

### Setup

> Now install package to local enviroment with poetry

```shell
$ cd distortme
$ poetry install
```
> Check installation 

```shell
$ distortme --help
```

---
## Features
- Get info about certain dataset (`distortme info`)
- Unpack any archive with one command (`distortme unpack`)
- Perform augmentations for images before training (`distortme augs`)
- Sort by folders images with certain descriptor in name (`distortme split`)
- Convert segmentation masks to RLE-encoding and back (`distortme torle`, `distortme fromrle`)
- Compress dataset to HDF5 format and decompress back (`distortme tohd5`, `distortme fromhd5`)
- Allows to download most popular datasets to given folder without any code (`distortme download`)
- Create labels for `Object detection`, `Face detection` and `Classification` tasks for your custom dataset (`distortme label`)
## Usage

---
## Created with
<a href="https://github.com/albumentations-team/albumentations" target="_blank"><img src="https://albumentations.readthedocs.io/en/latest/_static/logo.png" width="100"/></a>
<a href="https://typer.tiangolo.com/"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" width="100"/></a>
<a href="https://python-poetry.org/"><img src="https://python-poetry.org/images/logo-origami.svg" width="50"/></a>

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
