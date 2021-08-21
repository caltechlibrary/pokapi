# Pokapi<img width="11%" align="right" src="https://github.com/caltechlibrary/pokapi/raw/main/.graphics/pokapi-icon.png">


Pokapi (_Python Okapi Interface_)  is a Python package for getting basic data from using the [Okapi API](https://github.com/folio-org/okapi/blob/master/doc/guide.md) of a [FOLIO](https://www.folio.org) ILS server.

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://choosealicense.com/licenses/bsd-3-clause)
[![Latest release](https://img.shields.io/github/v/release/caltechlibrary/template.svg?style=flat-square&color=b44e88)](https://github.com/caltechlibrary/template/releases)
<!---
[![DOI](https://data.caltech.edu/badge/201106666.svg)](https://data.caltech.edu/badge/latestdoi/201106666)
-->

## Table of contents

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Known issues and limitations](#known-issues-and-limitations)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [License](#license)
* [Authors and history](#authors-and-history)
* [Acknowledgments](#authors-and-acknowledgments)


## Introduction

The [FOLIO](https://www.folio.org) platform is an [integrated library system](https://en.wikipedia.org/wiki/Integrated_library_system).  The Caltech Library uses a hosted solution by [EBSCO](https://www.ebsco.com) for its [library catalog](https://www.library.caltech.edu/libsearch).   To make writing interfaces and automation scripts in Python easier, the Caltech Library [Digital Library Development team](https://www.library.caltech.edu/staff?&field_directory_department%5B0%5D=754) developed Pokapi (_Python Okapi Interface_, a Python package that provides an object-oriented interface to accessing in a FOLIO instance via the [Okapi API](https://github.com/folio-org/okapi/blob/master/doc/guide.md).


## Installation

The instructions below assume you have a Python interpreter installed on your computer; if that's not the case, please first [install Python version 3](INSTALL-Python3.md) and familiarize yourself with running Python programs on your system.

On **Linux**, **macOS**, and **Windows** operating systems, you should be able to install `pokapi` with [`pip`](https://pip.pypa.io/en/stable/installing/).  To install `pokapi` from the [Python package repository (PyPI)](https://pypi.org), run the following command:
```
python3 -m pip install pokapi
```

As an alternative to getting it from [PyPI](https://pypi.org), you can use `pip` to install `pokapi` directly from GitHub, like this:
```sh
python3 -m pip install git+https://github.com/caltechlibrary/pokapi.git
```
 

## Usage

... _forthcoming_ ...


## Known issues and limitations

... _forthcoming_ ...


## Getting help

If you find an issue, please submit it in [the GitHub issue tracker](https://github.com/caltechlibrary/pokapi/issues) for this repository.


## Contributing

We would be happy to receive your help and participation with enhancing Topi!  Please visit the [guidelines for contributing](CONTRIBUTING.md) for some tips on getting started.


## License

Software produced by the Caltech Library is Copyright © 2021 California Institute of Technology.  This software is freely distributed under a BSD/MIT type license.  Please see the [LICENSE](LICENSE) file for more information.


## Acknowledgments

This work was funded by the California Institute of Technology Library.

Pokapi makes use of numerous open-source packages, without which Pokapi could not have been developed.  I want to acknowledge this debt.  In alphabetical order, the packages are:

* [commonpy](https://github.com/caltechlibrary/commonpy) &ndash; a collection of commonly-useful Python functions
* [ipdb](https://github.com/gotcha/ipdb) &ndash; the IPython debugger
* [setuptools](https://github.com/pypa/setuptools) &ndash; library for `setup.py`
* [sidetrack](https://github.com/caltechlibrary/sidetrack) &ndash; simple debug logging/tracing package

<div align="center">
  <br>
  <a href="https://www.caltech.edu">
    <img width="100" height="100" src="https://raw.githubusercontent.com/caltechlibrary/template/main/.graphics/caltech-round.png">
  </a>
</div>
