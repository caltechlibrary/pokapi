#!/usr/bin/env python3

from   decouple import config
import os
import pytest
import sys
import warnings
import uritemplate

try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

from pokapi import Folio, FolioRecord

# Decouple version 3.4 has an issue with using a deprecated method from
# ConfigParser. There's a PR in limbo at
# https://github.com/henriquebastos/python-decouple/pull/93
# Until the issue is fixed, let's do this.
warnings.filterwarnings("ignore", category = DeprecationWarning)

# These can be set as environment variables or written in a file called
# settings.ini in this directory.
okapi_url     = config('OKAPI_URL')
okapi_token   = config('OKAPI_TOKEN')
tenant_id     = config('TENANT_ID')

# We can't go on without these values
if not all([okapi_url, okapi_token, tenant_id]):
    raise RuntimeError('Missing value(s) of needed configuration variables')

# This Folio interface object is used throughout the rest of this file.
folio = Folio(okapi_url     = okapi_url,
              okapi_token   = okapi_token,
              tenant_id     = tenant_id,
              an_prefix     = 'clc')


def test_folio_different_ids():
    item1 = folio.record(barcode = "35047019531631")
    item2 = folio.record(instance_id = "1fedf5f3-b631-4d34-8d40-e022f70ab232")
    assert item1.id == item2.id
    assert item1.accession_number == item2.accession_number
    assert item1.accession_number == "clc.1fedf5f3.b631.4d34.8d40.e022f70ab232"
    assert item1.title == item2.title
    assert item1.author == item2.author
    assert item1.year == item2.year
    assert item1.publisher == item2.publisher
    assert item1.isbn_issn == item2.isbn_issn


def test_folio_field_values1():
    r = folio.record(barcode = "35047019531631")
    assert r.id == "1fedf5f3-b631-4d34-8d40-e022f70ab232"
    assert r.title == "The bad doctor"
    assert r.year == "2015"
    assert r.author == "Ian Williams"
    assert r.isbn_issn == "9780271067544"
    assert r.publisher == "The Pennsylvania State University Press"


def test_folio_field_values2():
    r = folio.record(accession_number = "clc.3d7bea51.8ed5.4b82.9a93.87f3b4e42374")
    assert r.id == "3d7bea51-8ed5-4b82-9a93-87f3b4e42374"
    assert r.title == "Journal of environmental psychology [electronic resource]"
    assert r.year == ""
    assert r.isbn_issn == "1522-9610"
    assert r.publisher == "Academic Press"


def test_folio_field_bad_values():
    r = folio.record(accession_number = "35047019077825")
    assert r == FolioRecord()
    r = folio.record(barcode = "")
    assert r == FolioRecord()


def test_folio_field_values3():
    r = folio.record(barcode = "35047019547967")
    assert r.author == "Eric R. Kandel ... [et al.] ; art editor, Sarah Mack"
    assert r.details_page == ""
    assert r.edition == "5th ed"
    assert r.id == "01d1d7e2-fcd8-4880-9820-0bba86778e39"
    assert r.isbn_issn == "0071390111"
    assert r.publisher == "McGraw-Hill"
    assert r.title == "Principles of neural science"
    assert r.year == "2013"


def test_folio_field_values4():
    r = folio.record(barcode = "35047019466119")
    assert r.author == "Bruce Alberts, Alexander Johnson, Julian Lewis, David Morgan, Martin Raff, Keith Roberts, Peter Walter ; with problems by John Wilson, Tim Hunt"
    assert r.details_page == ""
    assert r.edition == "Sixth edition"
    assert r.id == "307560df-3464-41fe-89df-4b09f65d7c3b"
    assert r.isbn_issn == "9780815344322"

