#!/usr/bin/env python3

import os
import pytest
import sys

try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

from decouple import config

from pokapi import Folio, FolioRecord

# These can be set as environment variables or written in a file called
# settings.ini in this directory.
okapi_url   = config('OKAPI_URL')
okapi_token = config('OKAPI_TOKEN')
tenant_id   = config('TENANT_ID')

# We can't go on without these values
if not all([okapi_url, okapi_token, tenant_id]):
    raise RuntimeError('Missing value(s) of needed configuration variables')

# This Folio interface object is used throughout the rest of this file.
folio = Folio(okapi_url = okapi_url,
              okapi_token = okapi_token,
              tenant_id = tenant_id)


def test_folio_different_ids():
    item1 = folio.record(barcode = "35047019531631")
    item2 = folio.record(instance_id = "1fedf5f3-b631-4d34-8d40-e022f70ab232")
    assert item1.id == item2.id
    assert item1.title == item2.title
    assert item1.author == item2.author
    assert item1.year == item2.year
    assert item1.publisher == item2.publisher
    assert item1.details_page == item2.details_page
    assert item1.isbn_issn == item2.isbn_issn


def test_folio_field_values1():
    r = folio.record(barcode = "35047019531631")
    assert r.id == "1fedf5f3-b631-4d34-8d40-e022f70ab232"
    assert r.title == "The bad doctor"
    assert r.year == "2015"
    assert r.author == "Williams, Ian"
    assert r.isbn_issn == "9780271067544"
    assert r.publisher == "The Pennsylvania State University Press"


def test_folio_field_values2():
    r = folio.record(accession_number = "clc.3d7bea51.8ed5.4b82.9a93.87f3b4e42374")
    assert r.id == "3d7bea51-8ed5-4b82-9a93-87f3b4e42374"
    assert r.title == "Journal of environmental psychology [electronic resource]"
    assert r.year == ""
    assert r.isbn_issn == "1522-9610"
    assert r.publisher == "Academic Press"
