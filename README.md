# Pokapi<img width="11%" align="right" src="https://github.com/caltechlibrary/pokapi/raw/main/.graphics/pokapi-icon.png">

Pokapi (_Python Okapi Interface_)  is a Python package for getting basic data from a [FOLIO](https://www.folio.org) LSP server using the [Okapi API](https://github.com/folio-org/okapi/blob/master/doc/guide.md).

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://choosealicense.com/licenses/bsd-3-clause)
[![Latest release](https://img.shields.io/github/v/release/caltechlibrary/pokapi.svg?style=flat-square&color=b44e88)](https://github.com/caltechlibrary/pokapi/releases)
[![DOI](https://img.shields.io/badge/dynamic/json.svg?label=DOI&style=flat-square&colorA=gray&colorB=navy&query=$.metadata.doi&uri=https://data.caltech.edu/api/record/2108)](https://data.caltech.edu/records/2108)
[![Python](https://img.shields.io/badge/Python-3.6+-brightgreen.svg?style=flat-square)](http://shields.io)
[![PyPI](https://img.shields.io/pypi/v/pokapi.svg?style=flat-square&color=orange)](https://pypi.org/project/pokapi/)


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

The [FOLIO](https://www.folio.org) platform is a [library services platform](https://www.niso.org/sites/default/files/stories/2017-09/FE_Grant_Future_Library_Systems_%20isqv24no4.pdf).  The Caltech Library uses a hosted solution by [EBSCO](https://www.ebsco.com) for its [library catalog](https://www.library.caltech.edu/libsearch).   To make writing interfaces and automation scripts in Python easier, the Caltech Library [Digital Library Development team](https://www.library.caltech.edu/staff?&field_directory_department%5B0%5D=754) are developing Pokapi (_Python Okapi Interface_), a Python package that provides an object-oriented interface to accessing in a FOLIO record data via the [Okapi API](https://github.com/folio-org/okapi/blob/master/doc/guide.md).


## Installation

The instructions below assume you have a Python interpreter installed on your computer; if that's not the case, please first [install Python version 3](INSTALL-Python3.md) and familiarize yourself with running Python programs on your system.

On **Linux**, **macOS**, and **Windows** operating systems, you should be able to install `pokapi` with [`pip`](https://pip.pypa.io/en/stable/installing/).  To install `pokapi` from the [Python package repository (PyPI)](https://pypi.org), run the following command:
```sh
python3 -m pip install pokapi
```

As an alternative to getting it from [PyPI](https://pypi.org), you can use `pip` to install `pokapi` directly from GitHub, like this:
```sh
python3 -m pip install git+https://github.com/caltechlibrary/pokapi.git
```
 

## Usage

The use of Pokapi is straightfoward. First, callers must create one instance of a `Folio` object that defines various aspects of how to communicate with their FOLIO/Okapi system. Then, callers can use the `record(...)` method on that `Folio` object to get objects that represent records in their FOLIO system. The method only requires an identifier, which can be a FOLIO instance identifier, an item barcode, or an EDS accession number. More details about all of this are provided below.


### The `Folio` interface object

To use Pokapi, first create a `Folio` object with parameters that define certain things Pokapi can't get on its own. These are: the the Okapi URL for your instance, an Okapi API token, a tenant id, the prefix that appears in front of your accession numbers, and a template for creating URLs that go to the Detailed Record page for an item in EDS.  Assuming that these values are stored in separate variables, the following code will create a `Folio` object:
```python
from pokapi import Folio

folio = Folio(okapi_url = the_okapi_url,
              okapi_token = the_okapi_token,
              tenant_id = the_tenant_id,
              an_prefix = the_accession_number_prefix,
              page_template = the_detailed_record_url_template)
```

As an example of a prefix for accession numbers, for Caltech the prefix is the `clc` part of an accession number such as `clc.025d49d5.735a.4d79.8889.c5895ac65fd2`.  The "page template" needs to be a URL that contains the character string `{accession_number}` somewhere within it; this character string will be replaced with an accession number to generate the final URL for the details page of an item returned by the `record(...)` method described below.  An example of a page template for Caltech is the following:

```
https://caltech.idm.oclc.org/login?url=https://search.ebscohost.com/login.aspx?direct=true&db=cat08655a&site=eds-live&scope=site&AN={accession_number}
```


### The `record(...)` method

The `Folio` class has only one method on it currently: `record(...)`. This method contacts the FOLIO server to obtain data and returns a `FolioRecord` object with the data stored in fields. The following fields are implemented at this time:

| Field           | Type   | Meaning |
|-----------------|--------|---------|
| `id`            | string | FOLIO instance record identifier |
| `details_page`  | string | URL for _Detailed Record_ page in EDS |
| `title`         | string | Title of the work |
| `author`        | string | Author; multiple authors are separated by "and" |
| `publisher`     | string | Publisher |
| `year`          | string | Year of publication |
| `edition`       | string | the edition of the work (if any) |
| `isbn_issn`     | string | ISBN or ISSN |

The method `Folio.record(...)` can take any one of the following mutually-exclusive keyword arguments to identify the record to be retrieved:

* `barcode`: retrieve the record corresponding to the given item barcode
* `instance_id`: retrieve the record having the given FOLIO instance identifier
* `accession_number`: retrieve the record corresponding to the accession number in EDS

Here is an example of using the method:

```python
r = folio.record(barcode = "35047019531631")
assert r.id == "1fedf5f3-b631-4d34-8d40-e022f70ab232"
assert r.title == "The bad doctor"
assert r.year == "2015"
assert r.author == "Williams, Ian"
assert r.isbn_issn == "9780271067544"
assert r.publisher == "The Pennsylvania State University Press"
```


## Known issues and limitations

The following are known limitations at this time:

* If a record has multiple publishers, only the first publisher name is retrieved.
* The title is extracted from the instance record's `title` field, but because (at least in our catalog) the title contains both a title and author info, Pokapi has to use heuristics to extract out just the title from the string. The heuristics might fail in some cases, especially if your installation of FOLIO uses different conventions for formatting the `title` field.


## Getting help

If you find an issue, please submit it in [the GitHub issue tracker](https://github.com/caltechlibrary/pokapi/issues) for this repository.


## Contributing

We would be happy to receive your help and participation with enhancing Pokapi!  Please visit the [guidelines for contributing](CONTRIBUTING.md) for some tips on getting started.


## License

Software produced by the Caltech Library is Copyright © 2021 California Institute of Technology.  This software is freely distributed under a BSD/MIT type license.  Please see the [LICENSE](LICENSE) file for more information.


## Acknowledgments

This work was funded by the California Institute of Technology Library.

Pokapi makes use of numerous open-source packages, without which Pokapi could not have been developed.  I want to acknowledge this debt.  In alphabetical order, the packages are:

* [CommonPy](https://github.com/caltechlibrary/commonpy) &ndash; a collection of commonly-useful Python functions
* [ipdb](https://github.com/gotcha/ipdb) &ndash; the IPython debugger
* [lxml](https://lxml.de) &ndash; an XML parsing library for Python
* [Python Decouple](https://github.com/henriquebastos/python-decouple/) &ndash; a high-level configuration file interface
* [setuptools](https://github.com/pypa/setuptools) &ndash; library for `setup.py`
* [uritemplate](https://github.com/python-hyper/uritemplate) &ndash; URI template parsing per RFC&nbsp;6570
* [validators](https://github.com/kvesteri/validators) &ndash; Python data validation for Humans
* [Sidetrack](https://github.com/caltechlibrary/sidetrack) &ndash; simple debug logging/tracing package

<div align="center">
  <br>
  <a href="https://www.caltech.edu">
    <img width="100" height="100" src="https://raw.githubusercontent.com/caltechlibrary/pokapi/main/.graphics/caltech-round.png">
  </a>
</div>
